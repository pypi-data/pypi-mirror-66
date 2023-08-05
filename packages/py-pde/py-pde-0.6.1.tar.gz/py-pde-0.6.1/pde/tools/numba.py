'''
Helper functions for just-in-time compilation with numba

.. codeauthor:: David Zwicker <david.zwicker@ds.mpg.de>
'''

import logging
import os
import warnings
from functools import wraps
from typing import Callable, Dict, Any, Optional, Tuple, TypeVar

import numpy as np
import numba as nb  # lgtm [py/import-and-import-from]

from ..tools.misc import decorator_arguments



# global settings for numba
NUMBA_PARALLEL = True   # enable parallel numba
NUMBA_FASTMATH = True   # enable fastmath switch (ignores NaNs!)
NUMBA_DEBUG = False     # enable additional debug information
    
    
# numba version as a list of integers
NUMBA_VERSION = [int(v) for v in nb.__version__.split('.')[:2]]
 
 
 
TFunc = TypeVar('TFunc')

    

def numba_environment() -> Dict[str, Any]:
    """ return information about the numba setup used
    
    Returns:
        (dict) information about the numba setup
    """
    # determine whether Nvidia Cuda is available
    try:
        from numba import cuda
        cuda_available = cuda.is_available()
    except ImportError:
        cuda_available = False

    # determine whether AMD ROC is available
    try:
        from numba import roc
        roc_available = roc.is_available()
    except ImportError:
        roc_available = False
    
    # determine threading layer
    try:
        threading_layer = nb.threading_layer()
    except ValueError:
        # threading layer was not initialized, so compile a mock function 
        @nb.jit('i8()', parallel=True)
        def f():
            s = 0
            for i in nb.prange(4):
                s += i
            return s
        f()
        try:
            threading_layer = nb.threading_layer()
        except ValueError:  # cannot initialize threading
            threading_layer = None
    except AttributeError:   # old numba version
        threading_layer = None
        
    return {'version': nb.__version__,
            'parallel': NUMBA_PARALLEL,
            'fastmath': NUMBA_FASTMATH,
            'debug': NUMBA_DEBUG,
            'using_svml': nb.config.USING_SVML,
            'threading_layer': threading_layer,
            'omp_num_threads': os.environ.get('OMP_NUM_THREADS'),
            'mkl_num_threads': os.environ.get('MKL_NUM_THREADS'),
            'num_threads': nb.config.NUMBA_NUM_THREADS,
            'num_threads_default': nb.config.NUMBA_DEFAULT_NUM_THREADS,
            'cuda_available': cuda_available,
            'roc_available': roc_available}
    
    
    
def _numba_get_signature(parallel: bool = False, **kwargs) -> Dict[str, Any]:
    """ return arguments for the :func:`nb.jit` with default values
    
    Args:
        parallel (bool): Allow parallel compilation of the function
        **kwargs: Additional arguments to `nb.jit`
        
    Returns:
        dict: Keyword arguments that can directly be used in :func:`nb.jit`
    """
    kwargs.setdefault('nopython', True)
    kwargs.setdefault('fastmath', NUMBA_FASTMATH)
    kwargs.setdefault('debug', NUMBA_DEBUG)
    
    # make sure parallel numba is only enabled in restricted cases 
    kwargs['parallel'] = parallel and NUMBA_PARALLEL
    return kwargs
    


if nb.config.DISABLE_JIT:    
    # use work-around for https://github.com/numba/numba/issues/4759
    def flat_idx(arr, i):
        """ helper function allowing indexing of scalars as if they arrays """
        if np.isscalar(arr):
            return arr
        else:
            return arr.flat[i]
else:
    # compiled version that specializes correctly
    @nb.generated_jit(nopython=True)
    def flat_idx(arr, i):
        """ helper function allowing indexing of scalars as if they arrays """
        if isinstance(arr, (nb.types.Integer, nb.types.Float)):
            return lambda arr, i: arr
        else:
            return lambda arr, i: arr.flat[i]

    
    
@decorator_arguments
def jit(function: TFunc,
        signature=None,
        parallel: bool = False, **kwargs) -> TFunc:
    """ apply nb.jit with predefined arguments
    
    Args:
        signature: Signature of the function to compile
        parallel (bool): Allow parallel compilation of the function
        **kwargs: Additional arguments to `nb.jit`
        
    Returns:
        Function that will be compiled using numba
    """
    if isinstance(function, nb.dispatcher.Dispatcher):
        # function is already jited
        return function  # type: ignore
    
    jit_kwargs = _numba_get_signature(parallel, **kwargs)
    name = function.__name__  # type: ignore
    logging.getLogger(__name__).info('Compile `%s` with parallel=%s',
                                     name, jit_kwargs['parallel'])
    return nb.jit(signature, **jit_kwargs)(function)  # type: ignore


        
@decorator_arguments
def jit_allocate_out(func: Callable,
                     parallel: bool = False,
                     out_shape: Optional[Tuple[int, ...]] = None,
                     num_args: int = 1,
                     **kwargs) -> Callable:
    """ Decorator that compiles a function with allocating an output array. 
    
    This decorator compiles a function that takes the arguments `arr` and
    `out`. The point of this function is to make the `out` array optional by 
    supplying an empty array of the same shape as `arr` if necessary. This is
    implemented efficiently by using :func:`nb.generated_jit`. 
    
    Args:
        func: The function to be compiled
        parallel (bool): Determines whether the function is jitted with
            parallel=True.
        out_shape (tuple): Determines the shape of the `out` array. If omitted,
            the same shape as the input array is used.
        num_args (int, optional): Determines the number of input arguments of
            the function.
        **kwargs: Additional arguments to `nb.jit`
            
    Returns:
        The decorated function
    """
    # TODO: Remove `num_args` and use inspection on `func` instead
    
    # we need to cast `parallel` to bool since np.bool is not supported by jit
    parallel = bool(parallel)
    
    if nb.config.DISABLE_JIT:
        # jitting is disabled => return generic python function
        
        if num_args == 1:
            def f_arg1_with_allocated_out(arr, out=None):
                """ helper function allocating output array """
                if out is None:
                    if out_shape is None:
                        out = np.empty_like(arr)
                    else:
                        out = np.empty(out_shape)
                return func(arr, out)
            
            return f_arg1_with_allocated_out
            
        elif num_args == 2:
            def f_arg2_with_allocated_out(a, b, out=None):
                """ helper function allocating output array """
                if out is None:
                    assert a.shape == b.shape
                    if out_shape is None:
                        out = np.empty_like(a)
                    else:
                        out = np.empty(out_shape)
                return func(a, b, out)
            
            return f_arg2_with_allocated_out
            
        else:
            raise NotImplementedError('Only 1 or 2 arguments are supported')
            
        
    else:
        # jitting is enabled => return specific compiled functions
        jit_kwargs = _numba_get_signature(parallel=False, **kwargs)
        register_jitable = nb.extending.register_jitable
        logging.getLogger(__name__).info('Compile `%s` with parallel=%s',
                                         func.__name__, jit_kwargs['parallel'])
    
        if num_args == 1:
            @nb.generated_jit(**jit_kwargs)
            @wraps(func)
            def wrapper(arr, out=None):
                """ wrapper deciding whether the underlying function is called
                with or without `out`. This uses :func:`nb.generated_jit` to
                compile different versions of the same function
                """
                if isinstance(arr, nb.types.Number):
                    # simple scalar call -> do not need to allocate anything
                    raise RuntimeError('Functions defined with an `out` '
                                       'keyword should not be called with '
                                       'scalar quantities.')
                    
                if not isinstance(arr, nb.types.Array):
                    raise RuntimeError('Compiled functions need to be called '
                                       'with numpy arrays, not type '
                                       f'{arr.__class__.__name__}')
                
                if isinstance(out, (nb.types.NoneType, nb.types.Omitted)):
                    # function is called without `out`
                    f_jit = register_jitable(parallel=parallel)(func)
                    
                    if out_shape is None:
                        # we have to obtain the shape of `out` from `arr` 
                        def f_with_allocated_out(arr, out):
                            """ helper function allocating output array """
                            return f_jit(arr, out=np.empty_like(arr))
        
                    else:
                        # the shape of `out` is given by `out_shape` 
                        def f_with_allocated_out(arr, out):
                            """ helper function allocating output array """
                            return f_jit(arr, out=np.empty(out_shape))
        
                    return f_with_allocated_out
                
                else:
                    # function is called with `out` argument
                    return func    
            
        elif num_args == 2:
            @nb.generated_jit(**jit_kwargs)
            @wraps(func)
            def wrapper(a, b, out=None):
                """ wrapper deciding whether the underlying function is called
                with or without `out`. This uses nb.generated_jit to compile
                different versions of the same function. """
                if isinstance(a, nb.types.Number):
                    # simple scalar call -> do not need to allocate anything
                    raise RuntimeError('Functions defined with an `out` '
                                       'keyword should not be called with '
                                       'scalar quantities')
                
                elif isinstance(out, (nb.types.NoneType, nb.types.Omitted)):
                    # function is called without `out`
                    f_jit = register_jitable(parallel=parallel)(func)
                    
                    if out_shape is None:  
                        # we have to obtain the shape of `out` from `a` 
                        def f_with_allocated_out(a, b, out):
                            """ helper function allocating output array """
                            return f_jit(a, b, out=np.empty_like(a))
        
                    else:
                        # the shape of `out` is given by `out_shape` 
                        def f_with_allocated_out(a, b, out):
                            """ helper function allocating output array """
                            return f_jit(a, b, out=np.empty(out_shape))
        
                    return f_with_allocated_out
                
                else:
                    # function is called with `out` argument
                    return func   
                
        else:
            raise NotImplementedError('Only 1 or 2 arguments are supported')
                 
        return wrapper  # type: ignore
    
    

if NUMBA_VERSION < [0, 45]:
    warnings.warn('Your numba version is outdated. Please install at least '
                  'version 0.45.')
