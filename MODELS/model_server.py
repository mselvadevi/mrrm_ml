#!/usr/bin/env python
# coding: utf-8



import json, os

from datetime import datetime
date_time_ =  datetime.now().strftime('%d-%m-%Y') 
LOG_DIR=None
print(LOG_DIR,date_time_)


import socketserver
import pickle
import inference


# In[ ]:
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
        print(type(self.data), sep="#")
        request_dict = json.loads(self.data)
        print(f"request_dict:{request_dict.keys()}")
        config = { 'category' : True, 'segmenter' : True,'spacy_' : True,'qa':False}
        if isinstance(request_dict,dict):
            config = request_dict.get('config')
            my_pages = request_dict.get('pages')
            print(f'ThreadedTCPRequestHandler:,{type(my_pages)}' )
            step_size = round(int(len(my_pages)/10))
            if step_size <=0 or step_size > len(my_pages) :  step_size =  len(my_pages)
            # config['step_size'] = step_size
            # result_dict_list = inference.batch_json(my_pages ,**config)
            result_dict_list = inference.process_pages(my_pages,**config)
            #print(result_dict_list)
            # self.request.sendall(pickle.dumps(result_dict_list))
            #result_dict_list = "welcome"
            self.wfile.write(bytes(json.dumps(result_dict_list)+ "\n", "utf-8"))
            print(f"\t\t\t################ Served to IP Address:{self.client_address[0]} ################")            
        elif isinstance(request_dict,list):
            my_pages = request_dict
            step_size = round(int(len(my_pages)/10))
            # if step_size <= 0: step_size= len(my_pages)
            # config['step_size'] = step_size
            # result_dict_list = inference.batch_json(json.loads(self.data) ,**config)
            result_dict_list = inference.process_pages(my_pages,**config)
            #print(result_dict_list)
            # self.request.sendall(pickle.dumps(result_dict_list))
            #result_dict_list = "welcome"
            self.wfile.write(bytes(json.dumps(result_dict_list)+ "\n", "utf-8"))
            print(f"\t\t\t################ Served to IP Address:{self.client_address[0]} ################")            
        else:
            result_dict_list = {'response':"No input was there in request"}
            self.wfile.write(bytes(json.dumps(result_dict_list)+ "\n", "utf-8"))         






if __name__ == "__main__":
    import sys,os
    print(f'Command line args {len(sys.argv)} and SEND_PORT {os.environ.get("SEND_PORT")}')
    if os.environ.get('SEND_PORT'):
        HOST = ''
        PORT = os.environ.get('SEND_PORT') #sys.argv[1], sys.argv[2]
    else:
        HOST, PORT = '', 6000
    # HOST, PORT = os.environ.get('LISTEN_HOST'), int(os.environ.get('LISTEN_PORT'))
    print(f'HOST:{HOST} and PORT:{PORT}')

    print(f'----------------------- Starting batch Processing in background Thread--------------------')
    import threading
    batch_thread = threading.Thread(target = inference.process_dir)
    batch_thread.start()

    print(f'----------------------- Starting SFTP Processing in background Thread--------------------')    
    sftp_thread = threading.Thread(target = inference.batch_files_put_pull,args=["/DEV"])
    sftp_thread.start()    
    
    # Create the server, binding to localhost on port 9999
    
    # with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
    print(f'############ Starting  MODEL INFERENCE SERVICES ################')
    with ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        print(f'Listening at {HOST} and {PORT}')
        server.serve_forever()



