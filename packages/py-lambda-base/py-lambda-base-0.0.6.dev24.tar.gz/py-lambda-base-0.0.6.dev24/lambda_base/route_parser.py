import re
import base64

"""
# Path Construction

* No leading or trailing slashes
* Each element can either be a raw string, or a url-capture group
* URL capture groups are surround by {}
* At present, the router does *NOT* support slurping route components (`{proxy+}` in API Gateway, e.g.), except as the last parameter
"""

def _decode(value):
  print('Full Decode received |{}|'.format(value))
  return base64.b16decode(value, casefold=True).decode()

_PROCESSORS = {
  'encoded': _decode,
  'piped': lambda x: x.split('|')
}

def parse_route_for_path(route_string, path, sparse=True):
  route_pieces = re.sub(r'/$', '', re.sub(r'^/', '', route_string.lower())).split('/')
  path_pieces = re.sub(r'/$', '', re.sub(r'^/', '', path.lower())).split('/')

  if len(route_pieces) > len(path_pieces):
    return None
  
  if not re.search(r'^\{.*\+\}$', route_pieces[-1]) and len(route_pieces) != len(path_pieces):
    return None

  path_params = {}
  for idx, route_elem in enumerate(route_pieces):
    match_obj = re.search(r'^\{(.*?)(\+*)\}$', route_elem)
    if match_obj:
      if match_obj.group(2) and idx == len(route_pieces) - 1: # Last element
        path_params[match_obj.group(1)] = '/'.join(path_pieces[idx:])
      else:
        path_params[match_obj.group(1)] = path_pieces[idx]
    else:
      if route_elem != path_pieces[idx]:
        return None
  if not sparse:
    parse_keys = list(filter(lambda x: ':' in x, path_params))
    for key in parse_keys:
      value = path_params[key]
      del path_params[key]
      pieces = key.split(':')
      new_key = pieces[0]
      for el in pieces[1:]:
        if el in _PROCESSORS:
          value = _PROCESSORS[el](value)
      path_params[new_key] = value

  return path_params