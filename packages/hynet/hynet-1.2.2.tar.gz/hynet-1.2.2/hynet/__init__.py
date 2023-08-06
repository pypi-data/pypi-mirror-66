#pylint: disable=wrong-import-position,invalid-name
"""
*hynet:* An optimal power flow framework for hybrid AC/DC power systems.

For more information, please refer to ``README.md``, which is provided
alongside *hynet*, as well as the docstrings of the individual classes and
functions. The variables below are set up during package initialization.

Parameters
----------
AVAILABLE_SOLVERS : list
    List of classes for all solvers available on the current system.
__version__ : str
    *hynet* version.
"""

__version__ = '1.2.2'  # Update the version in setup.py and conf.py as well

import sys as _sys

if _sys.version_info < (3, 5):
    raise ImportError('hynet requires Python 3.5 or higher.')

import hynet.config as config

from hynet.types_ import (hynet_id_,
                          hynet_int_,
                          hynet_float_,
                          hynet_complex_,
                          hynet_eps,
                          BusType,
                          BranchType,
                          InjectorType,
                          SolverType,
                          SolverStatus)

from hynet.data.connection import connect, DBConnection
from hynet.data.interface import (get_scenario_info,
                                  load_scenario,
                                  save_scenario,
                                  initialize_database,
                                  remove_scenarios,
                                  copy_scenarios)
from hynet.data.import_ import import_matpower_test_case

from hynet.scenario.capability import HalfSpace, CapRegion, ConverterCapRegion
from hynet.scenario.cost import PWLFunction
from hynet.scenario.representation import Scenario

from hynet.system.model import SystemModel
from hynet.system.result import SystemResult
from hynet.system.calc import calc, select_solver
from hynet.system.initial_point import (InitialPointGenerator,
                                        RelaxationInitialPointGenerator)

from hynet.opf.model import OPFModel
from hynet.opf.result import OPFResult
from hynet.opf.calc import calc_opf
from hynet.opf.initial_point import CopperPlateInitialPointGenerator

from hynet.loadability.model import LoadabilityModel
from hynet.loadability.result import LoadabilityResult
from hynet.loadability.calc import calc_loadability

from hynet.qcqp.problem import QCQP, QCQPPoint
from hynet.qcqp.result import QCQPResult
from hynet.qcqp.rank1approx import (Rank1Approximator,
                                    GraphTraversalRank1Approximator,
                                    LeastSquaresRank1Approximator)

import hynet.solver as solver
from hynet.solver import AVAILABLE_SOLVERS

from hynet.test.installation import test_installation

from hynet.opf.visual import (show_lmp_profile,
                              show_voltage_profile,
                              show_branch_flow_profile,
                              show_ampacity_dual_profile,
                              show_converter_flow_profile,
                              show_dispatch_profile,
                              show_power_balance_error,
                              show_branch_reconstruction_error)

from hynet.utilities.base import Timer

from hynet.distributed.server import (start_optimization_server,
                                      OptimizationServer,
                                      OptimizationJob)
from hynet.distributed.client import start_optimization_client

from hynet.expansion.conversion import (convert_transformer_to_b2b_converter,
                                        convert_ac_line_to_hvdc_system)
from hynet.expansion.selection import get_islanding_branches
