#!/usr/local/bin/python3.5
import sys
from constant import default_token_file

def write ():
  with open(default_token_file, 'w+') as f:
    print(sys.argv[1])
    f.write(sys.argv[1]);

if __name__ == '__main__':
  write()
