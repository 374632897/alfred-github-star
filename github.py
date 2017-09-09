#!/usr/local/bin/python3.5
# -*- coding:utf-8 -*-
from urllib import request
import json
import sys
import re
from alfred_format import parse
from constant import default_repo_file, default_token_file

base_uri = 'https://api.github.com/users/'
default_user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
required_fields = [
  'html_url',
  'full_name'
];

class GitHub:
  page = 1
  token = None
  username = None
  repos = []

  def __init__ (self, username):
    self.username = str(username)
    if not self.validate_token():
      return
    if not self.read_repos():
      self.fetch()

  def validate_token (self):
    try:
      with open(default_token_file, 'r') as f:
        token = f.read()
        self.token = token.strip()
        return token
    except IOError:
      return False

  def get_user_starred_uri (self):
    uri = base_uri + self.username + '/' + 'starred?per_page=100&page=' + str(self.page)
    self.page += 1
    return uri

  def add_header (self, request):
    request.add_header('user-agent', default_user_agent)
    request.add_header('Authorization', 'token ' + self.token.replace('\n', ''))
    return request

  def read_repos (self):
    try:
      with open (default_repo_file) as f:
        self.repos = json.loads(f.read())
        if len(self.repos) == 0:
          return False
        return True
    except:
      return False

  def filter (self, query):
    output = []

    default_title = u'更多详细结果， 请前往网页查看'
    default_link = 'https://github.com/' + str(self.username) + '?tab=stars';

    if not self.token:
      output.append({
        'full_name': '请先使用s-token 来绑定 token',
        'html_url': 'https://github.com/settings/tokens'
      })
      return output

    results = list(filter(lambda item: re.search(query, item['full_name']), self.repos));

    if len(results) != 0:
      for result in results:
        output.append(result)
    else:
      default_title = u'找不到结果， 请使用网页查询'
      output.append({ 'full_name': default_title, 'html_url': default_link })
    return output

  def filter_fields (self, repos):
    def key_filter (item) :
      new_obj = {}
      for field in required_fields:
        new_obj[field] = item[field]
      return new_obj

    return list(map(key_filter, repos));

  def write_repos (self):
    with open(default_repo_file, 'w') as f:
      f.write(json.dumps(self.filter_fields(self.repos)))

  def update (self):
    self.repos = [];
    self.fetch()

  def fetch (self):
    req = request.Request(self.get_user_starred_uri())
    self.add_header(req)
    with request.urlopen(req) as f:
      repos = json.loads(f.read().decode('utf-8'))
      self.repos += repos
      if len(repos) == 100:
        self.fetch()
      else:
        self.write_repos()


github = GitHub('374632897')
def main ():
  print(parse(github.filter(sys.argv[1])))

if __name__ == '__main__':
  main()
