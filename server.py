# This file controls the server.

from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
from database import *

class WebServerHandler(BaseHTTPRequestHandler):
	'''
	Handle GET requests.
	'''
	def do_GET(self):
		try:
			if self.path == '/':
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				outputHTML = ''
				with open('index.html', 'r') as indexFile:
					for line in indexFile:
						outputHTML += line
				indexFile.close()
				# outputHTML += '<html><body>'
				# outputHTML += '<h1 style="color: red; text-align: center;">Welcome</h1>'
				# outputHTML += '</body></html>'
				self.wfile.write(bytes(outputHTML, 'utf-8'))
				print (outputHTML)
				return

			if self.path.endswith('/register?'):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				outputHTML = ''
				with open('register.html', 'r') as indexFile:
					for line in indexFile:
						outputHTML += line
				indexFile.close()
				# outputHTML += '<html><body>'
				# outputHTML += '<h1 style="color: red; text-align: center;">Welcome</h1>'
				# outputHTML += '</body></html>'
				self.wfile.write(bytes(outputHTML, 'utf-8'))
				print (outputHTML)
				return
		except Exception as e:
			raise e
		

'''
The main function
'''
def main():
	try:
		port = 80
		server = HTTPServer(('', port), WebServerHandler)
		print ('Web server running on port %s' % port)
		engine = createDB()
		create_table(engine)
		server.serve_forever()
	except KeyboardInterrupt:
		print (' ^C entered. Stopping web server.')
		server.socket.close()

if __name__ == '__main__':
	main()
