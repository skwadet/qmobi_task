from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import logging
import sys

#logger settings
log = logging.getLogger()
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
handler.setLevel(logging.INFO)
log.addHandler(handler)
log.setLevel(logging.INFO)

#It's main class that doing all stuff
class Server(BaseHTTPRequestHandler):
    
    #This service needs only POST method,so we can deny all GETs
    def do_GET(self):
        self.send_response(405)
        log.error("GET / HTTP/1.1 405 - Method Not Allowed")
        self.end_headers()
        self.wfile.write(json.dumps({ 
            'error': '405 - GET Method Not Allowed'
        }).encode())
        
    #POST method, we need to pass there only "value_in": "<value>" in application/json CT
    def do_POST(self):
        
        #Parse CT and CL
        content_type = str(self.headers['Content-Type'])
        content_length = int(self.headers['Content-Length'])
        
        #Here check CT in POST and return JSON with error if CT is not valid
        if content_type != 'application/json' or content_length == 0:
            self.send_response(400)
            log.error("POST / HTTP/1.1 400 - Invalid request")
            self.end_headers()
            self.wfile.write(json.dumps({
                'error': '400 - Bad Request'
            }).encode())
        else:
            
            #Now can load JSON and check it for value entry
            message = json.loads(self.rfile.read(content_length))
            if 'value_in' not in message or len(message['value_in']) == 0:
                self.send_response(400)
                log.error("POST / HTTP/1.1 400 - 'value_in' in JSON not found or = 0")
                self.end_headers()
                self.wfile.write(json.dumps({
                    'error': '400 - Bad Request'
                }).encode())
                
            #Check value above zero
            elif float(message['value_in']) > 0:
                new = Server.count(float(message['value_in']))
                self.send_response(200)
                self.end_headers()
                self.wfile.write(json.dumps({
                    'currency': 'RUB',
                    'value_in': "%.2f" % float(message['value_in']),
                    'value_out': "%.2f" % new,
                }).encode())
                
            #If it = or < zero, then 400 responce
            else:
                self.send_response(400)
                log.error("POST / HTTP/1.1 400 - 'value_in' is < 0")
                self.end_headers()
                self.wfile.write(json.dumps({
                    'error': '400 - Bad Rsequest'
                }).encode())
                
    #This method translates to RUV currency 
    @staticmethod
    def count(in_currency):
        new_currency = in_currency * 72
        return new_currency
    
#Run server
if __name__ == '__main__':
    host = sys.argv[1]
    port = int(sys.argv[2])
    print(host, port)
    httpd = HTTPServer((host, port), Server)
    httpd.serve_forever()
