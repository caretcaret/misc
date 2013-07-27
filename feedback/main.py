#!/usr/bin/env python
from bottle import route, run, static_file, template, error, default_app

@route('/')
def home():
  return server_static("index.html")

@route('/static/<filename>')
def server_static(filename):
  return static_file(filename, root='./static')

@route('/first', method='POST')
def submit_first():
  request.json
  return None

@error(404)
def error404(error):
 return "Dear user, This is a 404 Page Not Found. Sincerely, bottle.py <3"

if __name__ == "__main__":
  run(host='localhost', port=8080, debug=True, reloader=True)
else:
  application = default_app()

