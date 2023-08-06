from functools import wraps
from .route_holder import RouteHolder

def route(route_string):
  def decorator_wrapper(func):
    holder = RouteHolder()
    holder.add_route_partial(func, route=route_string)

    @wraps(func)
    def func_wrapper(*args, **kwArgs):
      return func(*args, **kwArgs)
    return func_wrapper
  return decorator_wrapper
