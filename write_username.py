#!/usr/local/bin/python3.5
from constant import default_username, default_repo_file
from fs_util import writeTo, write, read
import sys
import os

if __name__ == '__main__':
  if os.path.exists(default_username) and read(default_username) == sys.argv[1]:
    print('Return')
  else:
    print('Update Username')
    writeTo(default_username)
    write(default_repo_file)

