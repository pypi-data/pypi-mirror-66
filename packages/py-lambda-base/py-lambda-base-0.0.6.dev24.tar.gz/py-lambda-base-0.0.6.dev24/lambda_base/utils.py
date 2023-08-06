import json_api_doc

def fetch_header_from_event(event, header_name):
  header_name = header_name.lower()
  actual_key = next((header for header in event['headers'].keys() if header_name == header.lower()), None)
  if actual_key is None:
    return None
  return (actual_key, event['headers'][actual_key])
def fetch_header_value_from_event(event, header_name, return_string=False):
  result = fetch_header_from_event(event, header_name)
  if result is not None:
    return result[1]
  if return_string:
    return ''
  return None

def jsonapi_serialize(data):
  result = {}
  if isinstance(data, map):
    data = list(data)

  if isinstance(data, list):
    result = json_api_doc.serialize(
      data=data,
      meta={
        'total': len(data)
      }
    )
    if 'data' not in result:
      result['data'] = []
  else:
    result = json_api_doc.serialize(
      data=data,
      meta={
        'total': 1
      }
    )
    
  return result