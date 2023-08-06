import os
from .route_holder import RouteHolder
from .response_handler import ResponseHandler

def all_subclasses(cls):
  return set(cls.__subclasses__()).union(
    [s for c in cls.__subclasses__() for s in all_subclasses(c)]
  )

class RequestHandler:
  def __init__(self, context):
    self.context = context
    self.router = RouteHolder()
    self.respondent = ResponseHandler()

  def _find_best_route(self, event):
    path = event['pathParameters'].get('proxy', '')
    http_method = event['httpMethod']
    return self.router.find_best_route(path, http_method)

  def _format_response(self, result):
    # Move this to the respondent
    return result

  def handle(self, event):
    best_handler = self._find_best_route(event)
    if best_handler:
      result = best_handler(event, respondent=self.respondent)
      if result:
        self.respondent.set_body(result)
    else:
      self.respondent.set_status(404)

    return self.respondent.response