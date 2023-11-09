
import auto_nn
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class ThreadedTCPRequestHandler(socketserver.StreamRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        print(f"\n\n\t\t\t################ Request from IP Address:{self.client_address[0]} ################")
        # self.request is the TCP socket connected to the client
        self.data =  self.rfile.readline()
        
        # request = pickle.loads(b''.join(chunk))
        print(type(self.data), self.data,sep="#")
        result_dict_list = auto_nn.process_pages(json.loads(self.data) )
        #print(result_dict_list)
        # self.request.sendall(pickle.dumps(result_dict_list))
        #result_dict_list = "welcome"
        self.wfile.write(bytes(json.dumps(result_dict_list)+ "\n", "utf-8"))
        print(f"\t\t\t################ Served to IP Address:{self.client_address[0]} ################")


print("here")

    
if __name__ == "__main__":

    HOST, PORT = '', 5000
    #HOST, PORT = os.environ.get('LISTEN_HOST'), int(os.environ.get('LISTEN_PORT'))
    print(f'HOST:{HOST} and PORT:{PORT}')

    # Create the server, binding to localhost on port 9999
    
    # with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
    with ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        print(f'Listening at {HOST} and {PORT}')
        server.serve_forever()    