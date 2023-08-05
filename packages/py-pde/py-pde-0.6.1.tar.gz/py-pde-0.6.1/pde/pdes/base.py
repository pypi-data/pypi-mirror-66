"""
Base classes
   
.. codeauthor:: David Zwicker <david.zwicker@ds.mpg.de> 
"""

from abc import ABCMeta, abstractmethod
import logging
from typing import Callable, Optional, TYPE_CHECKING  # @UnusedImport

import numpy as np

from ..fields.base import FieldBase
from ..trackers.base import TrackerCollectionDataType
from ..tools.numba import jit


if TYPE_CHECKING:
    from ..solvers.controller import TRangeType  # @UnusedImport



class PDEBase(metaclass=ABCMeta):
    """ base class for solving partial differential equations
    
    Attributes:
        check_implementation (bool):
            Flag determining whether (some) numba-compiled functions should be
            checked against their numpy counter-parts. This can help with
            implementing a correct compiled version for a PDE class.
        explicit_time_dependence (bool):
            Flag indicating whether the right hand side of the PDE has an
            explicit time dependence.
    """

    check_implementation: bool = True
    explicit_time_dependence: Optional[bool] = None


    def __init__(self, noise: float = 0):
        """
        Args:
            noise (float):
                Magnitude of the additive Gaussian white noise that is supported
                by default. If set to zero, a determinitics partial differential
                equation will be solved. If another noise structure is required
                the respective methods need to be overwritten.
        """
        self._logger = logging.getLogger(self.__class__.__name__)
        self.noise = noise


    @property
    def is_sde(self) -> bool:
        """ flag indicating whether this is a stochastic differential equation
        
        The :class:`BasePDF` class supports additive Gaussian white noise, whose
        magnitude is controlled by the `noise` property. In this case, `is_sde`
        is `True` if `self.noise != 0`.
        """
        # check for self.noise, in case __init__ is not called in a subclass
        return hasattr(self, 'noise') and self.noise != 0


    @abstractmethod
    def evolution_rate(self, field: FieldBase, t: float = 0) \
        -> FieldBase: pass


    def _make_pde_rhs_numba(self, state: FieldBase) -> Callable:
        """ create a compiled function for evaluating the right hand side """
        raise NotImplementedError


    def make_pde_rhs(self, state: FieldBase, backend: str = 'auto') -> Callable:
        """ return a function for evaluating the right hand side of the PDE
        
        Args:
            state (:class:`~pde.fields.FieldBase`):
                An example for the state from which the grid and other
                information can be extracted
            backend (str): Determines how the function is created. Accepted 
                values are 'python` and 'numba'. Alternatively, 'auto' lets the
                code decide for the most optimal backend.
                
        Returns:
            Function determining the right hand side of the PDE
        """
        if backend == 'auto':
            try:
                rhs = self._make_pde_rhs_numba(state)
            except NotImplementedError:
                backend = 'numpy'
            else:
                rhs._backend = 'numba'  # type: ignore
            
        if backend == 'numba':
            rhs = self._make_pde_rhs_numba(state)
            rhs._backend = 'numba'  # type: ignore
                
        elif backend == 'numpy':
            state = state.copy()
            
            def evolution_rate_numpy(state_data, t: float):
                """ evaluate the rhs given only a state without the grid """
                state.data = state_data
                return self.evolution_rate(state, t).data
        
            rhs = evolution_rate_numpy
            rhs._backend = 'numpy'  # type: ignore
            
        elif backend != 'auto':
            raise ValueError(f'Unknown backend `{backend}`')
        
        if (self.check_implementation and
                rhs._backend == 'numba'):  # type: ignore
            # compare the numba implementation to the numpy implementation
            expected = self.evolution_rate(state.copy()).data
            test_state = state.copy()
            result = rhs(test_state.data, 0)
            if not np.allclose(result, expected):
                raise RuntimeError('The numba compiled implementation of the '
                                   'right hand side is not compatible with '
                                   'the numpy implementation.')
        
        return rhs
            
            
    def noise_realization(self, state: FieldBase, t: float = 0) -> FieldBase:
        """ returns a realization for the noise
        
        Args:
            state (:class:`~pde.fields.ScalarField`):
                The scalar field describing the concentration distribution
            t (float): The current time point
            
        Returns:
            :class:`~pde.fields.ScalarField`:
            Scalar field describing the evolution rate of the PDE 
        """
        if self.noise:
            data = np.random.normal(scale=self.noise, size=state.data.shape)
            return state.copy(data=data, label='Noise realization')
        else:
            return state.copy(data=0, label='Noise realization')

       
    def _make_noise_realization_numba(self, state: FieldBase) -> Callable:            
        """ return a function for evaluating the noise term of the PDE
        
        Args:
            state (:class:`~pde.fields.FieldBase`):
                An example for the state from which the grid and other
                information can be extracted
                
        Returns:
            Function determining the right hand side of the PDE
        """
        if self.noise:        
            noise_strength = float(self.noise)
            data_shape = state.data.shape
            
            @jit
            def noise_realization(state_data: np.ndarray, t: float):
                """ compiled helper function returning a noise realization """ 
                return noise_strength * np.random.randn(*data_shape)
            
        else:
            @jit
            def noise_realization(state_data: np.ndarray, t: float):
                """ compiled helper function returning a noise realization """ 
                return None
        
        return noise_realization  # type: ignore    
            
       
    def _make_sde_rhs_numba(self, state: FieldBase) -> Callable:            
        """ return a function for evaluating the noise term of the PDE
        
        Args:
            state (:class:`~pde.fields.FieldBase`):
                An example for the state from which the grid and other
                information can be extracted
                
        Returns:
            Function determining the right hand side of the PDE
        """
        evolution_rate = self._make_pde_rhs_numba(state)
        noise_realization = self._make_noise_realization_numba(state)
        
        @jit
        def sde_rhs(state_data: np.ndarray, t: float):
            """ compiled helper function returning a noise realization """ 
            return (evolution_rate(state_data, t),
                    noise_realization(state_data, t))
        
        return sde_rhs  # type: ignore    
    
                        
    def make_sde_rhs(self, state: FieldBase, backend: str = 'auto') \
            -> Callable:
        """ return a function for evaluating the right hand side of the SDE
        
        Args:
            state (:class:`~pde.fields.FieldBase`):
                An example for the state from which the grid and other
                information can be extracted
            backend (str): Determines how the function is created. Accepted 
                values are 'python` and 'numba'. Alternatively, 'auto' lets the
                code decide for the most optimal backend.
                
        Returns:
            Function determining the deterministic part of the right hand side
            of the PDE together with a noise realization.
        """
        if backend == 'auto':
            try:
                sde_rhs = self._make_sde_rhs_numba(state)
            except NotImplementedError:
                backend = 'numpy'
            else:
                sde_rhs._backend = 'numba'  # type: ignore
                return sde_rhs
             
        if backend == 'numba':
            sde_rhs = self._make_sde_rhs_numba(state)
            sde_rhs._backend = 'numba'  # type: ignore
                
        elif backend == 'numpy':
            state = state.copy()
            
            def sde_rhs(state_data, t: float):
                """ evaluate the rhs given only a state without the grid """
                state.data = state_data
                return (self.evolution_rate(state, t).data,
                        self.noise_realization(state, t).data)
        
            sde_rhs._backend = 'numpy'  # type: ignore
            
        else:
            raise ValueError(f'Unknown backend `{backend}`')
        
        return sde_rhs
            

    def solve(self, state: FieldBase,
              t_range: "TRangeType",
              dt: float = None,
              tracker: TrackerCollectionDataType = ['progress', 'consistency'],
              method: str = 'auto',
              **kwargs):
        """ convenience method for solving the partial differential equation 
        
        The method constructs a suitable solver
        (:class:`~pde.solvers.base.SolverBase`) and controller
        (:class:`~pde.controller.Controller`) to advance the state over the
        temporal range specified by `t_range`. To obtain full flexibility, it is
        advisable to construct these classes explicitly. 

        Args:
            state (:class:`~pde.fields.base.FieldBase`):
                The initial state (which also defines the grid)
            t_range (float or tuple):
                Sets the time range for which the PDE is solved. If only a
                single value `t_end` is given, the time range is assumed to be 
                `[0, t_end]`.
            dt (float):
                Time step of the chosen stepping scheme. If `None`, a default
                value based on the stepper will be chosen.
            tracker:
                Defines a tracker that process the state of the simulation at
                fixed time intervals. Multiple trackers can be specified as a
                list. The default value is ['progress', 'consistency'], which
                displays a progress bar and checks the state for consistency,
                aborting the simulation when not-a-number values appear.
            method (:class:`~pde.solvers.base.SolverBase` or str):
                Specifies a method for solving the differential equation. This
                can either be an instance of
                :class:`~pde.solvers.base.SolverBase` or a descriptive name
                like 'explicit' or 'scipy'. The valid names are given by
                :meth:`pde.solvers.base.SolverBase.registered_solvers`.
            **kwargs:
                Additional keyword arguments are forwarded to the solver class
                
        Returns:
            :class:`~pde.fields.base.FieldBase`:
            The state at the final time point.
        """
        from ..solvers.base import SolverBase
        
        if method == 'auto':
            method = 'scipy' if dt is None else 'explicit'
        
        # create solver
        if callable(method):
            solver = method(pde=self, **kwargs)
            if not isinstance(solver, SolverBase):
                self._logger.warn('Solver is not an instance of `SolverBase`. '
                                  'Specified wrong method?')
        else:
            solver = SolverBase.from_name(method, pde=self, **kwargs)
        
        # create controller
        from ..solvers import Controller
        controller = Controller(solver, t_range=t_range, tracker=tracker)
        
        # run the simulation
        return controller.run(state, dt)
                