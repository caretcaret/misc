#!/usr/bin/python

from bs4 import BeautifulSoup
import urllib.request
import re
from collections import defaultdict
import sqlite3
import time

conn = sqlite3.connect('data.db')

c = conn.cursor()

"""
c.execute('''CREATE TABLE arenas (id integer, winner integer,
  p1 text, s1 integer, w1 integer, o1 integer, c1 integer, f11 integer, f12 integer, f13 integer, f14 integer,
  p2 text, s2 integer, w2 integer, o2 integer, c2 integer, f21 integer, f22 integer, f23 integer, f24 integer,
  p3 text, s3 integer, w3 integer, o3 integer, c3 integer, f31 integer, f32 integer, f33 integer, f34 integer,
  p4 text, s4 integer, w4 integer, o4 integer, c4 integer, f41 integer, f42 integer, f43 integer, f44 integer)''')

conn.commit()
"""

def data_for(day=3575):
  url = 'http://foodclub.daqtools.info/index.php?requestday=' + str(day)
  html = urllib.request.urlopen(url)
  bs = BeautifulSoup(html)
  table = bs.find_all('table')[0]
  data = defaultdict(list)
  row = 0
  col = -1
  for tr in table.find_all('tr'):
    for td in table.find_all('td'):
      if 'rowspan' not in td.attrs and row < 21:
        col += 1
        if 'class' in td.attrs:
          if 'winner' in td.attrs['class'] or 'loser' in td.attrs['class']:
            row += 1
            col = 0
            data['pirates'].append(td.string)

          if 'loser' in td.attrs['class']:
            data['winner'].append(0)
          if 'winner' in td.attrs['class']:
            data['winner'].append(1)

        if col == 3:
          data['strengths'].append(int(td.string))
        if col == 4:
          data['weights'].append(int(td.string))
        if col == 5:
          data['opening'].append(int(td.string.split(':')[0]))
        if col == 6:
          data['closing'].append(int(td.string.split(':')[0]))
        if col == 8:
          string = re.sub(r'[\+\-\(\)=]', ' ', td.string)
          data['food_adjust'].append([int(x) for x in string.split()][:4])
  return data

def insert_data(day, data):
  for i in range(5):
    try:
      winner = data['winner'].index(1, 4*i, 4*i+4) - 4*i
      arena = (day, winner)
      for j in range(4):
        arena += (data['pirates'][4*i+j], data['strengths'][4*i+j], data['weights'][4*i+j], data['opening'][4*i+j], data['closing'][4*i+j])
        arena += tuple(data['food_adjust'][4*i+j])
      c.execute("INSERT INTO arenas VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", arena)
    except Exception as e:
      print(e)
  
  conn.commit()

# main loop
for i in range(3575, 5174+1):
  try:
    print('Getting day ' + str(i))
    time.sleep(1)
    d = data_for(i)
    print('Got ' + str(d))
    dd = insert_data(i, d)
    print('Inserted.')
  except Exception as e:
    print(e)