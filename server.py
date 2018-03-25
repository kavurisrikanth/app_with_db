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
			if self.path == '/' or self.path == '/?':
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
				self.wfile.write(bytes(outputHTML, 'utf-8'))
				print (outputHTML)
				return

			if self.path.startswith('/delete?'):
				pieces = self.path.split('?')
				attr = pieces[1]
				if attr == '':
					self.send_response(200)
					self.send_header('Content-type', 'text/html')
					self.end_headers()
					outputHTML = ''
					with open('delete.html', 'r') as indexFile:
						for line in indexFile:
							outputHTML += line
					indexFile.close()
					self.wfile.write(bytes(outputHTML, 'utf-8'))
					print (outputHTML)
					return
				else:
					data = attr.split('=')
					try:
						rem(data[1])
						self.send_response(200)
						self.send_header('Content-type', 'text/html')
						self.end_headers()
						outputHTML = ''
						outputHTML += '<html><head>'
						outputHTML += '<title>Delete success</title>'
						outputHTML += '<meta http-equiv="refresh" content="3;url=/" />'
						outputHTML += '</head><body style="align-content: center;">'
						outputHTML += '<h1 style="color: green;">Delete successful</h1>'
						outputHTML += '<h3>Redirecting you home...</h3>'
						outputHTML += '</body></html>'
						self.wfile.write(bytes(outputHTML, 'utf-8'))
						print (outputHTML)
						return
					except Exception as e:
						self.send_response(200)
						self.send_header('Content-type', 'text/html')
						self.end_headers()
						outputHTML = ''
						with open('del_failed.html', 'r') as indexFile:
							for line in indexFile:
								outputHTML += line
						indexFile.close()
						self.wfile.write(bytes(outputHTML, 'utf-8'))
						print (outputHTML)
						return

		except Exception as e:
			raise e
	
	def do_POST(self):
		try:
			self.send_response(301)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
			print ('ctype: ' + ctype)
			pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')
			if ctype == 'multipart/form-data':
				fields = cgi.parse_multipart(self.rfile, pdict)
				name = fields.get('name')
				email = fields.get('email')
				pwd = fields.get('pwd')
				ins(name[0].decode('utf-8'), email[0].decode('utf-8'), pwd[0].decode('utf-8'))
				outputHTML = ''
				with open('success.html', 'r') as indexFile:
					for line in indexFile:
						outputHTML += line
				indexFile.close()
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
		port = 8080
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
