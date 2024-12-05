import http.server
import socketserver
import json
import protos.interface_pb2_grpc as interface2
import protos.interface_pb2 as interface
import grpc


class Handler(http.server.BaseHTTPRequestHandler):
	def do_GET(self):
		print(self.requestline)
		buffer = self.rfile
		print(json.loads(buffer.read(int(self.headers['Content-Length'])).decode("utf-8")))
		self.send_response(200)
		self.send_header('Content-Type', 'application/json')
		self.end_headers()
		responseBody = {
			'test': 'value'
		}
		self.wfile.write(json.dumps(responseBody).encode("utf-8"))


	def do_POST(self):
		print(self.requestline)
		buffer = self.rfile
		print(json.loads(buffer.read(int(self.headers['Content-Length'])).decode("utf-8")))
		self.send_response(200)
		self.send_header('Content-Type', 'application/json')
		self.end_headers()
		responseBody = {
			'test': 'value'
		}
		self.wfile.write(json.dumps(responseBody).encode("utf-8"))
	
		

PORT = 9999

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()

def run():
    with grpc.insecure_channel('localhost:9998') as channel:
        stub = interface2.InterfaceStub(channel)
        response = stub.TimerForTour(interface.SecondForTimerRequest(timeSecond=20))
        print("Greeter client received: " + response.message)