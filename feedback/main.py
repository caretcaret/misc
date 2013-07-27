from bottle import route, run, static_file, template, error

@route('/')
def landing():
  return "Hello World!"

@route('/static/<filename>')
def server_static(filename):
  return static_file(filename, root='./static')

@route('/first', method='POST')
def submit_first():
  request.json
  return None

@error(404)
def error404(error):
 return "404 File Not Found"

run(host='localhost', port=8080, debug=True)

