from functools import wraps
from .route_holder import RouteHolder

def jsonapi(reject_if_no_data=False):
  def decorator_wrapper(func):
    holder = RouteHolder()
    if reject_if_no_data:
      def check_no_data(req, respondent):
        if not req.data:
          print('JSON API Not parsed properly. Parsed Body is |{}|'.format(req.body))
          print('Original event is |{}|'.format(req.event))
          respondent.add_error({
            'code': 'invalid_jsonapi',
            'title': 'Body is not valid JSONAPI'
          })
      holder.add_route_partial(func, jsonapi=True, append_before_action=check_no_data)
    else:
      holder.add_route_partial(func, jsonapi=True)

    @wraps(func)
    def func_wrapper(*args, **kwArgs):
      return func(*args, **kwArgs)
    return func_wrapper
  return decorator_wrapper
