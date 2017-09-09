#!/usr/local/bin/python3.5
import sys
import json

def writeTo (filename):
  write(filename, content = sys.argv[1])
  print(sys.argv[1])

def write (filename, content = '', isJson = False):
  with open(filename, 'w+') as f:
    f.write(content if not isJson else json.dumps(content));

def read (filename, isJson = False):
  try:
    with open(filename) as f:
      content = f.read()
      return content if not isJson else json.loads(content)
  except:
    write(filename)
    read(filename)
    return False
