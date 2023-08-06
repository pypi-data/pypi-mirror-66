import sys
from functools import wraps
from .route_holder import RouteHolder

module_obj = sys.modules[__name__]
VERBS = ['get', 'post', 'put', 'delete', 'patch', 'options', 'head']

for verb in VERBS:
  def make_me_a_method(inverb):
    def http_method_wrapper(func):
      holder = RouteHolder()
      holder.add_route_partial(func, http_method=inverb.upper())

      @wraps(func)
      def func_wrapper(*args, **kwArgs):
        return func(*args, **kwArgs)
      return func_wrapper
    return http_method_wrapper
  
  func_instance = make_me_a_method(verb)
  func_instance.__name__ = verb
  func_instance.__module__ = module_obj
  setattr(module_obj, verb, func_instance)
  
__all__ = VERBS