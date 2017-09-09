#!/usr/local/bin/python3.5
import json
def parse (results):
  return json.dumps({
    'items': list(map(parse_item, results))
  })

def parse_item (item) :
  return {
    'uid': item['html_url'],
    'title': item['full_name'],
    'subtitle': item['html_url'],
    'type': 'url',
    'arg': item['html_url']
  }
