import json
from deepmerge import always_merger

class ResponseHandler:
  def __init__(self):
    self._status_code = 204
    self._response_body = ""
    self._headers = {}
    self._cookies = {}
    self._errors = []
    self._return_immediately = False

  @property
  def return_immediately(self):
    return self._return_immediately

  @property
  def has_errors(self):
    return len(self._errors) > 0
  
  @property
  def _set_cookie_headers(self):
    def format_cookie(kvpack):
      key, value_dict = kvpack
      pieces = ['{}={}'.format(key, value_dict['value'])]
      for opt in value_dict:
        if opt.lower() in ['expires', 'max-age', 'domain', 'path', 'samesite']:
          pieces.append('{}={}'.format(opt, value_dict[opt]))
        if opt.lower() in ['secure', 'httponly']:
          if value_dict[opt]:
            pieces.append(opt)
      return '; '.join(pieces)

    return list(map(format_cookie, self._cookies.items()))

  @property
  def status_code(self):
    if self._errors:
      return 400
    if self._response_body and self._status_code == 204:
      return 200
    return self._status_code

  @property
  def response(self):
    hsh = {
      "statusCode": self.status_code
    }
    if self._errors:
      hsh["body"] = ', '.join(map(lambda x: x.get('title', x.get('code', 'Unknown')), self._errors))
    elif self._response_body:
      hsh["body"] = self._response_body

    if self._headers:
      hsh["headers"] = self._headers
    if self._cookies:
      hsh["multiValueHeaders"] = {
        'Set-Cookie': self._set_cookie_headers
      }
    return hsh

  def set_status(self, status):
    if isinstance(status, int):
      self._status_code = status

  def set_body(self, body):
    if isinstance(body, dict):
      self.set_json(body)
    else:
      self._response_body = body

  def set_json(self, body):
    self._response_body = json.dumps(body)
    self._headers['content-type'] = 'application/json'

  def merge_json(self, body):
    cur_json = {}
    try:
      cur_json = json.loads(self._response_body)
    except json.JSONDecodeError:
      cur_json = {}
    new_json = always_merger.merge(cur_json, body)
    self.set_json(new_json)

  def add_error(self, error):
    self._errors.append(error)

  def set_cookie(self, key, value, **options):
    self._cookies[key] = {
      'value': value,
      **options
    }

  def set_return_immediately(self):
    self._return_immediately = True