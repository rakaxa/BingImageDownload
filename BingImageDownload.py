#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import urllib
if sys.version[0] == '3':
  import requests
  from requests.auth import HTTPBasicAuth
else:
  import urllib2
import os
import re
import json
import time
import random

########################################
# 画像を取得して保存する
########################################
def get_image(url,  count, ext, dirname):
  match = re.search('(.*?)[/?:*<>|].*$', ext)
  if match:
    ext = match.group(1)
  if sys.version[0] == '3':
    filename = os.path.normpath(dirname + "/" + ("%03d" % (count)) + ext)
  else:
    filename = os.path.normpath(unicode(dirname, 'shift-jis') + "/" + ("%03d" % (count)) + ext)
  try:
    if sys.version[0] == '3':
      req = urllib.request.Request(url)
    else:
      req = urllib2.Request(url)
    req.add_header("User-agent", 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)')
    if sys.version[0] == '3':
      response = urllib.request.urlopen(req)
    else:
      response = urllib2.urlopen(req)
  except:
    print(str(count) + ": Download Error!!")
    try:
      print("URL : " + url)
    except:
      print("The URL cannot be displayed.")
    return
  try:
    f = open(filename, "wb")
    f.write(response.read())
    f.close()
    print(str(count) + ": Success!!")
  except:
    print(str(count) + ": FileWrite Error!!")
    print("Filename : " + filename)
  return

def main():
  ########################################
  # ユーザ名/パスワードは標準入力から
  ########################################
  user     = sys.stdin.readline().strip()
  password = sys.stdin.readline().strip()

  ########################################
  # URLの組み立て
  # キーワードはUTF-8でエンコード
  ########################################
  url = 'https://api.datamarket.azure.com/Bing/Search/v1/Image?Query=%27'
  if sys.version[0] == '3':
    # python3の場合、UTF-8にエンコード(※Windowsの場合)
    url += urllib.parse.quote_plus(sys.argv[1], encoding="utf-8")
  else:
    # python2の場合、Shift-JIS -> Unicode -> UTF-8の順に変換(※Windowsの場合)
    url += urllib.quote(unicode(sys.argv[1], 'shift-jis').encode('utf-8'))
  url += '%27&ImageFilters=%27Size%3ALarge%27&$format=json'

  ########################################
  # 出力ディレクトリ作成
  ########################################
  if not os.path.exists(sys.argv[1]):
    os.mkdir(sys.argv[1])

  ########################################
  # BASIC認証にてAPIへアクセス
  ########################################
  if sys.version[0] == '3':
    results = requests.get(url, auth=HTTPBasicAuth(user, password))
  else:
    mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    mgr.add_password(None, 'api.datamarket.azure.com', user, password)
    handler = urllib2.HTTPBasicAuthHandler(mgr)
    urllib2.install_opener(urllib2.build_opener(handler))
    results = urllib2.urlopen(url).read()

  ########################################
  # 結果をJSONに変換し、ImageURLを取得
  ########################################
  if sys.version[0] == '3':
    bing_data = json.loads(results.text)
  else:
    bing_data = json.loads(results)
  count = 0
  if 'results' in bing_data['d']:
    for datum in bing_data['d']['results']:
      imgurl = datum['MediaUrl']
      match = re.search('.*(\..*?)$', imgurl)
      if match:
        get_image(imgurl, count, match.group(1), sys.argv[1])
        count += 1
        time.sleep(random.randint(1, 10))
  else:
    print("search result no data.")

if __name__ == "__main__":
  sys.exit(main())
