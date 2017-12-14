from jinja2 import Environment, FileSystemLoader
from webob import Request, Response

items = [
  'app.js',
  'react.js',
  'leaflet.js',
  'D3.js',
  'moment.js',
  'math.js',
  'main.css',
  'bootstrap.css',
  'normalize.css',
]
js = []
css = []

for item in items:
  dividedOne, dividedTwo = item.split('.')
  if dividedTwo == 'js':
    js.append(item)
  elif dividedTwo == 'css':
    css.append(item)

class WsgiTopBottomMiddleware(object):
  def __init__(self, app):
    self.app = app

  def __call__(self, environ, start_response):
    response = self.app(environ, start_response).decode()

    if response.find('<head>' and '<body>') > -1:
      beforehead, head = response.split('<head>')
      datahead, afterhead = head.split('</head>')
      beforebody, body = afterhead.split('<body>')
      databody, afterbody = body.split('</body>')
      data = '<head>' + datahead + '</head>' + '<body>' + databody +'</body>'
      yield (beforehead + data + afterbody).encode() 
    else:
      yield (response).encode()

def app(environ, start_response):
  response_code = '200 OK'
  response_type = ('Content-Type', 'text/HTML')
  start_response(response_code, [response_type])
  return ''''''

app = WsgiTopBottomMiddleware(app)

request = Request.blank('/index.html')

# request = Request.blank('/about/aboutme.html')

env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('index.html')
print(template.render(scripts=js, styles=css))

# env = Environment(loader=FileSystemLoader('.'))
# template = env.get_template('about/aboutme.html')
# print(template.render(scripts=js, styles=css))

print(request.get_response(app))
