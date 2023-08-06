import json
import re
import json_api_doc
from dpath import util
from .route_parser import parse_route_for_path

class EnhancedRequest:
  def __init__(self, event, route):
    def fetch_header(header_name):
      header_name = header_name.lower()
      actual_key = next((header for header in event['headers'].keys() if header_name == header.lower()), None)
      if actual_key is None:
        return None
      return (actual_key, event['headers'][actual_key])
    def fetch_header_value(header_name, return_string=False):
      result = fetch_header(header_name)
      if result is not None:
        return result[1]
      if return_string:
        return ''
      return None

    def cleanup_query_params(query_params):
      cleaned_params = {}
      PATTERN = r'\[([^\]\[]*?)\]$'
      for key, value in query_params.items():
        key = re.sub(r'\[\]$', '', key)
        pieces = []
        while True:
          matcher = re.search(PATTERN, key)
          if matcher is None:
            break
          pieces.insert(0, matcher.group(1))
          key = re.sub(PATTERN, '', key)
        pieces.insert(0, key)
        util.new(cleaned_params, pieces, value)
      return cleaned_params

    self._event = event
    self._route = route
    self._body = {}
    self._data = {}

    params = {}
    query_params = {}
    if event['queryStringParameters']:
      query_params = {**event['queryStringParameters']}
    if event['multiValueQueryStringParameters']:
      query_params = {**query_params, **event['multiValueQueryStringParameters']}

    params = {**params, **cleanup_query_params(query_params), **event['pathParameters']}
    if event['body']:
      params['raw_body'] = event['body']
      params['parsed_body'] = {}
      if re.search('json', fetch_header_value('content-type', return_string=True), re.IGNORECASE):
        try:
          parsed_body = json.loads(event['body'])
          params['parsed_body'] = {**parsed_body}
          params = {**params, **parsed_body}
          self._body = parsed_body
          if 'jsonapi' in route and route['jsonapi'] and 'data' in self._body:
            try:
              self._data = json_api_doc.deserialize(self._body)
            except AttributeError:
              self._data = {}
        except json.JSONDecodeError:
          pass

    params = {**params, **parse_route_for_path(route['route'], event['pathParameters'].get('proxy', ''), sparse=False)}
    self._params = params
  
  @property
  def params(self):
    return self._params

  @property
  def body(self):
    return self._body

  @property
  def data(self):
    return self._data

  @property
  def event(self):
    return self._event

  @property
  def route(self):
    return self._route