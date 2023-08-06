"""
PICOS-based solver for the *hynet*-specific QCQP problem (SD and SOC relaxation).
"""

import logging
import abc

import picos as pic
import numpy as np
import cvxopt

from hynet.types_ import hynet_float_, SolverType, SolverStatus
from hynet.utilities.base import Timer
from hynet.utilities.cvxopt import scipy2cvxopt
from hynet.qcqp.solver import SolverInterface
from hynet.qcqp.problem import QCQPPoint
from hynet.qcqp.result import QCQPResult

_log = logging.getLogger(__name__)


def parse_status(status):
    """Parse the PICOS status into a ``SolverStatus``."""
    # REMARK: According to the source code of PICOS 2.0.8, the solution status
    # in Problem.status corresponds to Solution.claimedStatus, which is the
    # Solution.primalStatus if the latter equals Solution.dualStatus or
    # a string "primal [primalStatus] and dual [dualStatus]" if they do not
    # agree. Apparently, the primalStatus and dualStatus is set to one of the
    # SS_* constants in picos/modeling/solution.py.
    if status.upper() == 'OPTIMAL':
        return SolverStatus.SOLVED
    if status.upper() == 'PREMATURE':
        return SolverStatus.INACCURATE
    if status.upper() == 'INFEASIBLE':
        return SolverStatus.INFEASIBLE
    return SolverStatus.FAILED


class SolverBase(SolverInterface):
    """Base class for PICOS-based solvers for a relaxation of the QCQP."""

    def __init__(self, solver_name='cvxopt', **kwds):
        super().__init__(**kwds)
        self.solver_name = solver_name

        if self.solver_name.upper() == 'CVXOPT':
            tolerance = 1e-6
            if 'abs_ipm_opt_tol' not in self.param:
                self.param['abs_ipm_opt_tol'] = tolerance
            if 'rel_ipm_opt_tol' not in self.param:
                self.param['rel_ipm_opt_tol'] = tolerance
            if 'rel_prim_fsb_tol' not in self.param:
                self.param['rel_prim_fsb_tol'] = 10 * tolerance
            if 'rel_dual_fsb_tol' not in self.param:
                self.param['rel_dual_fsb_tol'] = 10 * tolerance
            if 'max_iterations' not in self.param:
                self.param['max_iterations'] = 500

    @staticmethod
    @abc.abstractmethod
    def _add_voltage_matrix_constraints(prob, qcqp, x):
        """Add the SOC or PSD constraint(s) on the ``v_tld``-part of ``x``."""

    def solve(self, qcqp):
        """
        Solve the given QCQP via a relaxation using PICOS.

        The relaxation-specific constraints on the bus voltage matrix are
        added via the (abstract) method ``_add_voltage_matrix_constraints``,
        which must be implemented in a derived class.

        Parameters
        ----------
        qcqp : QCQP
            Specification of the quadratically-constrained quadratic problem.

        Returns
        -------
        result : QCQPResult
            Solution of the relaxed problem associated with the QCQP.
        """
        # We solve the following problem:
        #
        #  min   c^T x   s.t.   Ax == b,  Bx <= d,  x_lb <= x <= x_ub
        #   x                ...and SOC or PSD constraint(s) on v_tld-part of x
        #
        # For the following code, I used the PICOS documentation provided at
        # https://picos-api.gitlab.io/picos/api.html

        timer = Timer()
        # ------------------ generate data --------------------------
        (c, A, b, B, d, x_lb, x_ub) = qcqp.get_vectorization()

        # -------------------- size of the data ---------------------
        dim_x = c.shape[0]

        #  ----------- convert to CVXOPT sparse matrices ------------
        # The PICOS interface uses CVXOPT to deal with matrices
        c = scipy2cvxopt(c)
        A = scipy2cvxopt(A)
        B = scipy2cvxopt(B)

        # ---- convert the constants into params of the problem -----
        c = pic.Constant('c', c)
        A = pic.Constant('A', A)
        b = pic.Constant('b', b)
        B = pic.Constant('B', B)
        d = pic.Constant('d', d)

        # ----- create a problem and the optimization variable ------
        prob = pic.Problem()
        x = pic.RealVariable('x', dim_x)

        # ------------------- add the constraints -------------------
        crt_Ax_b = prob.add_constraint(A * x == b)
        crt_Bx_d = prob.add_constraint(B * x <= d)

        # Add the specified lower and upper bounds
        #
        # REMARK: The bound constraints are not implemented with ``lower`` and
        # ``upper`` of ``add_variable`` as they (apparently) do not provide
        # the corresponding dual variables. Furthermore, as PICOS (apparently)
        # does not support variable indexing with index arrays, the cumbersome
        # approach below is pursued.
        def create_selection_matrix(idx):
            return cvxopt.spmatrix(np.ones(len(idx)),    # Coefficients
                                   np.arange(len(idx)),  # Row indices
                                   idx,                  # Column indices
                                   (len(idx), dim_x))    # Size

        idx_lb = np.where(~np.isnan(x_lb))[0]
        idx_ub = np.where(~np.isnan(x_ub))[0]

        S_lb = pic.Constant('S_lb', create_selection_matrix(idx_lb))
        S_ub = pic.Constant('S_ub', create_selection_matrix(idx_ub))

        x_lb = pic.Constant('x_lb', x_lb[idx_lb])
        x_ub = pic.Constant('x_ub', x_ub[idx_ub])

        crt_lb = prob.add_constraint(S_lb * x >= x_lb)
        crt_ub = prob.add_constraint(S_ub * x <= x_ub)

        # Add relaxation-specific constraints on the voltage matrix
        # (This method is overridden appropriately in derived classes)
        self._add_voltage_matrix_constraints(prob, qcqp, x)

        # -------------------- set the objective --------------------
        prob.set_objective('min', c|x)

        # ----------------- set the solver options ------------------
        prob.options.solver = self.solver_name
        prob.options.duals = True
        prob.options.verbosity = 1 if self.verbose else 0
        prob.options.update(**self.param)

        _log.debug(self.type.name + " ~ Modeling ({:.3f} sec.)"
                   .format(timer.interval()))

        # ----------- optimization and solution recovery ------------
        try:
            prob.solve()
        except pic.SolutionFailure as exception:
            # The documentation of these cases is quite shady, see
            # https://picos-api.gitlab.io/picos/api/picos.html#picos.Problem.solve
            # In case of CVXOPT, we observed that certified primal infeasibility
            # is categorized by PICOS as "Solver claims unknown solution for
            # infeasible problem." Correspondingly, we map these cases to
            # infeasibility and all others to a failure.
            if exception.code == 3:
                status = SolverStatus.INFEASIBLE
            else:
                status = SolverStatus.FAILED
        else:
            status = parse_status(prob.status)

        solver_time = timer.interval()
        _log.debug(self.type.name + " ~ Solver ({:.3f} sec.)"
                   .format(solver_time))

        if status in [SolverStatus.SOLVED, SolverStatus.INACCURATE]:
            # Convert the PICOS variable object into a NumPy array
            x = np.asarray(x.value).reshape(dim_x)

            (V, f, s, z) = qcqp.split_vectorization_optimizer(x)
            v = self.rank1approx(V, qcqp.edges, qcqp.roots)
            optimizer = QCQPPoint(v, f, s, z)

            dv_eq = np.asarray(crt_Ax_b.dual).reshape(-1)
            dv_ineq = np.asarray(crt_Bx_d.dual).reshape(-1)

            dv_lb = np.nan * np.ones(dim_x, dtype=hynet_float_)
            dv_lb[idx_lb] = np.asarray(crt_lb.dual).reshape(-1)
            dv_lb = qcqp.split_vectorization_bound_dual(dv_lb)

            dv_ub = np.nan * np.ones(dim_x, dtype=hynet_float_)
            dv_ub[idx_ub] = np.asarray(crt_ub.dual).reshape(-1)
            dv_ub = qcqp.split_vectorization_bound_dual(dv_ub)

            optimal_value = prob.value

            result = QCQPResult(qcqp, self, status, solver_time,
                                optimizer=optimizer,
                                V=V,
                                optimal_value=optimal_value,
                                dv_lb=dv_lb,
                                dv_ub=dv_ub,
                                dv_eq=dv_eq,
                                dv_ineq=dv_ineq)
        else:
            result = QCQPResult(qcqp, self, status, solver_time)

        _log.debug(self.type.name + " ~ Result creation ({:.3f} sec.)"
                   .format(timer.interval()))
        _log.debug(self.type.name + " ~ Total time for solver ({:.3f} sec.)"
                   .format(timer.total()))
        return result


class SOCRSolver(SolverBase):
    """
    PICOS-based solver for a second-order cone relaxation of the QCQP.

    For information on solver-specific parameters, see e.g. [1, 2]_.
    To retrieve a list of available solvers, use

    >>> import picos
    >>> picos.available_solvers()

    By default, CVXOPT is selected. For appropriate performance in OPF
    calculations, its default parameters are adapted. Access the ``param``
    attribute of an object for their inspection.

    See Also
    --------
    hynet.qcqp.solver.SolverInterface : Abstract base class for QCQP solvers.

    References
    ----------
    .. [1] https://picos-api.gitlab.io/picos/api/picos.html#picos.Options
    .. [2] https://picos-api.gitlab.io/picos/tolerances.html
    """

    @property
    def name(self):
        return "PICOS + " + self.solver_name.upper()

    @property
    def type(self):
        return SolverType.SOCR

    def solve(self, qcqp):  # pylint: disable=useless-super-delegation
        """
        Solve the given QCQP via its second-order cone relaxation using PICOS.

        Parameters
        ----------
        qcqp : QCQP
            Specification of the quadratically-constrained quadratic problem.

        Returns
        -------
        result : QCQPResult
            Solution of the SOCR associated with the QCQP.
        """
        # We solve the following problem:
        #
        #  min   c^T x   s.t.   Ax == b,  Bx <= d,  x_lb <= x <= x_ub
        #   x                   ...and SOC constraints on v_tld-part of x
        return super().solve(qcqp)

    @staticmethod
    def _add_voltage_matrix_constraints(prob, qcqp, x):
        """Add the SOC constraints on the ``v_tld``-part of ``x``."""
        # Second-order cone constraints on V (cf. QCQP.get_vectorization)
        #
        # PSD constraint on 2x2 principal submatrix =>
        #  (a) diagonal is nonnegative -> ensured by LB on voltage mag.
        #  (b) determinant is nonnegative -> rotated SOC:
        #
        #               V_ij * conj(V_ij) <= V_ii * V_jj
        #                             <=>
        #          real(V_ij)^2 + imag(V_ij)^2 <= V_ii * V_jj
        #
        #      where i is the source bus and j is the destination bus
        #      of the considered edge. The latter is implemented below.
        #
        # Note that PICOS supports two types of SOC constraints:
        #  (1) Lorentz cone: abs(x) <= t;
        #  (2) Rotated SOC: abs(x)**2 <= t*u; t >=0
        dim_v = qcqp.dim_v
        K = qcqp.num_edges
        (e_src, e_dst) = qcqp.edges

        prob.add_list_of_constraints(
            [abs(x[(dim_v + k):(dim_v + k + K + 1):K])**2
             <= x[int(e_src[k])] * x[int(e_dst[k])]
             for k in range(K)])


class SDRSolver(SolverBase):
    """
    PICOS-based solver for a semidefinite relaxation of the QCQP.

    For information on solver-specific parameters, see e.g. [1, 2]_.
    To retrieve a list of available solvers, use

    >>> import picos
    >>> picos.available_solvers()

    By default, CVXOPT is selected. For appropriate performance in OPF
    calculations, its default parameters are adapted. Access the ``param``
    attribute of an object for their inspection.

    See Also
    --------
    hynet.qcqp.solver.SolverInterface : Abstract base class for QCQP solvers.

    References
    ----------
    .. [1] https://picos-api.gitlab.io/picos/api/picos.html#picos.Options
    .. [2] https://picos-api.gitlab.io/picos/tolerances.html
    """

    @property
    def name(self):
        return "PICOS + " + self.solver_name.upper()

    @property
    def type(self):
        return SolverType.SDR

    def solve(self, qcqp):  # pylint: disable=useless-super-delegation
        """
        Solve the given QCQP via its semidefinite relaxation using PICOS.

        Parameters
        ----------
        qcqp : QCQP
            Specification of the quadratically-constrained quadratic problem.

        Returns
        -------
        result : QCQPResult
            Solution of the SDR associated with the QCQP.
        """
        # We solve the following problem:
        #
        #  min   c^T x   s.t.   Ax == b,  Bx <= d,  x_lb <= x <= x_ub
        #   x                   ...and a PSD constraint on the v_tld-part of x
        return super().solve(qcqp)

    @staticmethod
    def _add_voltage_matrix_constraints(prob, qcqp, x):
        """Add the PSD constraint on the ``v_tld``-part of ``x``."""
        # PSD constraint on V
        #
        # Consider the splitting of the Hermitian matrix V into its
        # real and imaginary part, i.e., V = V_r + j*V_i. Then,
        #
        #       V is PSD    <=>    V_cr = [ V_r  -V_i ] is PSD
        #                                 [ V_i   V_r ]
        #
        # This code implements the real-valued equivalent of V >= 0,
        # i.e., V_cr >= 0. To this end, a semidefinite matrix variable
        # V_cr is added and all relevant elements are equated to v_tld.
        dim_v = qcqp.dim_v
        K = qcqp.num_edges
        (e_src, e_dst) = qcqp.edges

        assert np.all(e_src > e_dst)  # Sparsity pattern of lower-triangular part

        V_cr = pic.SymmetricVariable('V_cr', (2*dim_v, 2*dim_v))

        prob.add_constraint(V_cr >> 0)  # PSD

        for k in range(K):
            i = int(e_src[k])
            j = int(e_dst[k])
            prob.add_constraint(V_cr[i, j] == x[dim_v + k])
            prob.add_constraint(V_cr[i + dim_v, j + dim_v] == x[dim_v + k])
            prob.add_constraint(V_cr[i + dim_v, j] == x[dim_v + k + K])
            prob.add_constraint(V_cr[i, j + dim_v] == -x[dim_v + k + K])

        for i in range(dim_v):
            prob.add_constraint(V_cr[i, i] == x[i])
            prob.add_constraint(V_cr[i + dim_v, i + dim_v] == x[i])
            prob.add_constraint(V_cr[i + dim_v, i] == 0)
