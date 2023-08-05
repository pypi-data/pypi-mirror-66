# -*- coding: utf-8 -*-
"""
Created on Sat Oct 26 04:26:20 2019

@author: yoelr
"""
from .units_of_measure import chemical_units_of_measure, definitions, types
from ..utils import var_with_units, get_obj_values, repr_kwargs
from .documenter import autodoc_functor
from inspect import signature

__all__ = ("Functor",  "TFunctor", "TPFunctor", "TIntegralFunctor",
           "functor", 'H', 'S', 'V', 'Cn', 'mu', 'kappa', 'sigma', 'delta', 'epsilon',
           'Psat', 'Hvap', 'display_asfunctor', 'functor_lookalike',
           'functor_matching_params', 'functor_base_and_params',)

RegisteredArgs = set()
RegisteredFunctors = []

# %% Utilities

def functor_name(functor):
    return functor.__name__ if hasattr(functor, "__name__") else type(functor).__name__

def display_asfunctor(functor, var=None, name=None, show_var=True):
    name = name or functor_name(functor)
    info = f"{name}{str(signature(functor)).replace('self, ', '')}"
    var = var or (functor.var if hasattr(functor, 'var') else None)
    if var:
        if show_var:
            info += f" -> " + var_with_units(var, chemical_units_of_measure)
        else:
            name, *_ = var.split('.')
            u = chemical_units_of_measure.get(name)
            if u: info += f" -> {u}"
    return info

def functor_lookalike(cls):
    cls.__repr__ = Functor.__repr__
    cls.__str__ = Functor.__str__
    return cls

def functor_matching_params(params):
    length = len
    N_total = length(params)
    for base in RegisteredFunctors:
        args = base._args
        N = length(args)
        if N > N_total: continue
        if args == params[:N]: return base
    raise ValueError("could not match function signature to registered functors")

def functor_base_and_params(function):
    params = tuple(signature(function).parameters)
    base = functor_matching_params(params)
    return base, params[len(base._args):]


# %% Decorator
  
def functor(f=None, var=None, wrap=None, **autodoc):
    """
    Decorate a function of temperature, or both temperature and pressure as a Functor subclass.
    
    Parameters
    ----------
    f : function(T, *args) or function(T, P, *args)
        Function that calculate a thermodynamic property based on temperature,
        or both temperature and pressure.
    var : str, optional
        Name of variable returned (useful for bookkeeping).
    wrap : function
        Should return a dictionary of arguments to pass to the fist function argument.
    **autodoc : 
        Options to autodoc Functor subclass. By default, Functor subclass is not automatically documented.
    
    Notes
    -----
    The functor decorator checks the signature of the function to find the 
    names of the parameters that should be stored as data. 
    
    Examples
    --------
	Create a functor of temperature that returns the vapor pressure
	in Pascal:
	
    >>> # Describe the return value with `var`.
    >>> # Thermosteam's chemical units of measure are always assumed.
    >>> @functor(var='Psat')
    ... def Antoine(T, a, b, c):
    ...     return 10.0**(a - b / (T + c))
    >>> f = Antoine(a=10.116, b=1687.5, c=-42.98)
    >>> f
    Functor: Antoine(T, P=None) -> Psat [Pa]
     a: 10.116
     b: 1687.5
     c: -42.98
    >>> f(T=373.15)
    101047.25357066597
    
    
    """
    if f:
        base, params = functor_base_and_params(f)
        dct = {'__slots__': (),
               'function': staticmethod(f),
               'params': params,
               'var': var}
        cls = type(f.__name__, (base,), dct)
        cls._autodoc_ = autodoc
        if wrap: cls.wrapper(wrap, **autodoc)
        elif autodoc: autodoc_functor(cls, **autodoc)
        cls.__module__ = f.__module__
        return cls
    else:
        return lambda f: functor(f, var, wrap, **autodoc)


# %% Decorators
    
class FunctorFactory:
    __slots__ = ('var',)
   
    def __init__(self, var):
        self.var = var
    
    def __call__(self, function=None, wrap=None, **autodoc):
        return functor(function, self.var, wrap, **autodoc)
    
    def s(self, function=None, wrap=None, **autodoc):
        return functor(function, self.var + '.s', wrap, **autodoc)
    
    def l(self, function=None, wrap=None, **autodoc):
        return functor(function, self.var + '.l',  wrap, **autodoc)
    
    def g(self, function=None, wrap=None, **autodoc):
        return functor(function, self.var + '.g', wrap, **autodoc)
    
    def __repr__(self):
        return f"{type(self).__name__}({repr(self.var)})"
    
H, S, Cn, V, kappa, mu, Psat, Hvap, sigma, delta, epsilon = [FunctorFactory(i) for i in
                                                             ('H', 'S', 'Cn', 'V', 'kappa',
                                                              'mu', 'Psat', 'Hvap',
                                                              'sigma', 'delta', 'epsilon')]


# %% Functors

class Functor: 
    __slots__ = ('function_kwargs', '_data')
    definitions = definitions
    types = types
    
    def __init_subclass__(cls, args=None, before=None, after=None):
        if args and not hasattr(cls, 'function'):
            args = tuple(args)
            assert args not in RegisteredArgs, f"abstract functor with args={args} already implemented"
            if before:
                index = RegisteredFunctors.index(before)
            elif after:
                index = RegisteredFunctors.index(after) + 1
            else:
                index = 0
            RegisteredFunctors.insert(index, cls)
            RegisteredArgs.add(args)
            cls._args = args
    
    def __init__(self, *args, **kwargs):
        for i, j in zip(self.params, args): kwargs[i] = j
        self.set_data(kwargs)
    
    def _load_data(self, data):
        self.function_kwargs = self.wrap(**data) if hasattr(self, 'wrap') else data
    
    def get_data(self):
        return self._data.copy()
    
    def set_data(self, data):
        self._data = data
        self._load_data(data)
    
    def update_data(self, **kwargs):
        data = self._data
        data.update(kwargs)
        self._load_data(data)
    
    @classmethod
    def from_other(cls, other):
        self = cls.__new__(cls)
        self._data = other._data
        self.function_kwargs = other.function_kwargs
        return self
    
    @classmethod
    def from_args(cls, data):
        self = cls.__new__(cls)
        self.set_data(dict(zip(self.params, data)))
        return self
    
    @classmethod
    def from_kwargs(cls, data):
        self = cls.__new__(cls)
        self.set_data(data)
        return self
    
    @classmethod
    def from_obj(cls, data):
        self = cls.__new__(cls)
        self.set_data(dict(zip(self.params, get_obj_values(data, self.params))))
        return self
    
    @classmethod
    def wrapper(cls, wrap=None, **autodoc):
        if wrap:
            cls.params = tuple(signature(wrap).parameters)
            cls.wrap = staticmethod(wrap)
            autodoc_options = autodoc or cls._autodoc_
            if autodoc_options: autodoc_functor(cls, **autodoc_options)
            return cls
        else:
            return lambda wrap: cls.wrapper(wrap, **autodoc)
    
    def _object_info(self):
        return f"{type(self).__name__}({repr_kwargs(self.get_data(), start='')})"
    
    def _functor_info(self):
        info = f"Functor: {display_asfunctor(self)}"
        data = self._data
        for key, value in data.items():
            if callable(value):
                value = display_asfunctor(value, show_var=False)
                info += f"\n {key}: {value}"
                continue
            try:
                info += f"\n {key}: {value:.5g}"
            except:
                info += f"\n {key}: {value}"
            else:
                key, *_ = key.split('_')
                u = chemical_units_of_measure.get(key)
                if u: info += ' ' + str(u)
        return info
    
    def __str__(self):
        return display_asfunctor(self)
    
    def __repr__(self):
        return f"<{self}>"
    
    def _example_info(self, **kwargs):
        obj_info = self._object_info()
        f_info = self._functor_info()
        f_info.replace('\n', 4*' ')
        value = self(**kwargs)
        call_sig = repr_kwargs(kwargs, start="")
        return (f">>> f = {obj_info}\n"
                f">>> f\n"
                f"{f_info}\n"
                f">>> f({call_sig})\n"
                f"{value}")
    
    def _show_example(self, **kwargs):
        print(self._example_info(**kwargs))
    
    def show(self, format='functor'):
        if format == 'object':
            info = self._object_info()
        elif format == 'functor':
            info = self._functor_info()
        else:
            raise ValueError(f"format must be either 'functor' or 'object', not {repr(format)}")
        print(info)
        
    _ipython_display_ = show


class TFunctor(Functor, args=('T',)):
    __slots__ = ()
    kind = "functor of temperature (T; in K)"
    def __call__(self, T, P=None):
        return self.function(T, **self.function_kwargs)


class TIntegralFunctor(Functor, args=('Ta', 'Tb')):
    __slots__ = ()
    kind = "temperature integral functor (Ta to Tb; in K)"
    def __call__(self, Ta, Tb, P=None):
        return self.function(Ta, Tb, **self.function_kwargs)


class TPFunctor(Functor, args=('T', 'P')):
    __slots__ = ()
    kind = "functor of temperature (T; in K) and pressure (P; in Pa)"
    def __call__(self, T, P):
        return self.function(T, P, **self.function_kwargs)


    
    
    