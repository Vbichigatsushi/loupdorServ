import http.server
import socketserver
import json
import protos.interface_pb2_grpc as interface2
import protos.interface_pb2 as interface
import grpc

def runInscription(HOST, PORT, clientName, clientIp, clientRole):
    with grpc.insecure_channel(f'{HOST}:{str(PORT)}') as channel:
        stub = interface2.LoupdorServiceStub(channel)
        response = stub.Inscrption(interface.InscriptionRequest(name=clientName, ip=clientIp, role=clientRole))
        return response.message

def runMove(HOST, PORT, clientIp, clientDirection):
    with grpc.insecure_channel(f'{HOST}:{str(PORT)}') as channel:
        stub = interface2.LoupdorServiceStub(channel)
        response = stub.Move(interface.MoveRequest(ip=clientIp, direction=clientDirection))
        return response.message

class Handler(http.server.BaseHTTPRequestHandler):
	def traitementGETnPOST(self):
		print(self.requestline)
		buffer = self.rfile
		variabeul = json.loads(buffer.read(int(self.headers['Content-Length'])).decode("utf-8"))
		print("données reçu => " + str(variabeul))
		self.send_response(200)
		self.send_header('Content-Type', 'application/json')
		self.end_headers()
		if ('name' in variabeul and 'role' in variabeul and 'order' in variabeul and variabeul['order'] == 'inscription'):
			try: 
				responseInsc = runInscription('172.25.1.15', 50051, variabeul['name'], str(self.client_address[0]) , variabeul['role'])
				responseBody = {
					'message': f'Bienvenue {variabeul["name"]} !',
					'roleAttributed': responseInsc
				}
				self.wfile.write(json.dumps(responseBody).encode("utf-8"))
			except Exception as inst:
				print(inst)
				responseBody = {
					'message': 'Client non inscrit une erreur s\'est produite !'
				}
				self.wfile.write(json.dumps(responseBody).encode("utf-8"))
		elif ('direction' in variabeul and 'order' in variabeul and variabeul['order'] == 'move'):
			try: 
				responseMv = runMove('172.25.1.15', 50051, str(self.client_address[0]) , variabeul['direction'])
				print(str(responseMv))
				responseBody = {
					'message': 'Mouvement effectué !',
					'gridVue': str(responseMv)
				}
				self.wfile.write(json.dumps(responseBody).encode("utf-8"))
			except Exception as inst:
				print(inst)
				responseBody = {
					'message': 'Mouvement non pris en compte !'
				}
				self.wfile.write(json.dumps(responseBody).encode("utf-8"))

	def do_GET(self):
		self.traitementGETnPOST()


	def do_POST(self):
		self.traitementGETnPOST()

PORT = 9999

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()