import json
import re
from functools import partial
from .singleton import Singleton
from .route_parser import parse_route_for_path
from .enhanced_request import EnhancedRequest

class RouteHolder(metaclass=Singleton):
  def __init__(self):
    self._routes = {}

  def _hoist_request(self, route, event, *, respondent):
    enhanced_request = EnhancedRequest(event, route)
    for before_action in route['before_actions']:
      before_action(enhanced_request, respondent=respondent)
      if respondent.return_immediately:
        break

    if respondent.return_immediately or respondent.has_errors:
      return

    return route['function'](enhanced_request, respondent=respondent)

  def _evaluate_route(self, path, http_method, route):
    if route['http_method'] != 'ANY' and route['http_method'] != http_method:
      return False
    
    if parse_route_for_path(route['route'], path) is None:
      return False
    return True

  def find_best_route(self, path, http_method):
    path_evaluator = partial(self._evaluate_route, path, http_method)
    valid_routes = sorted(filter(path_evaluator, self.routes), key=lambda x: -x['route'].count('/'))
    if valid_routes:
      return partial(self._hoist_request, valid_routes[0])
    return None

  def add_route_partial(self, func, route=None, http_method=None, jsonapi=None, append_before_action=None):
    key = '{}-{}'.format(func.__module__, func.__name__)
    if not key in self._routes:
      self._routes[key] = {'http_method': 'ANY', 'before_actions': []}

    self._routes[key]['function'] = func
    if route is not None:
      self._routes[key]['route'] = route
    if http_method is not None:
      self._routes[key]['http_method'] = http_method
    if jsonapi is not None:
      self._routes[key]['jsonapi'] = True
    if append_before_action is not None:
      self._routes[key]['before_actions'].append(append_before_action)

  @property
  def routes(self):
    return self._routes.values()