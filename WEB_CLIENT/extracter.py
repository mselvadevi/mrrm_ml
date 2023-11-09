import  TCPClient
import json,os
from flask import Flask,request,jsonify
server = Flask(__name__)

@server.route("/kpo/hello", methods=['GET','POST'])
def hello():
    return "<h1 style='color:blue'>Hello There welcome!</h1>"

@server.route('/kpo/parse', methods=['POST'])
def parse_json_transcript():
    try:
        content_type = request.headers.get('Content-Type')
        print("IS:",request.content_type)
        
        if (request.content_type.startswith('application/json')):
            print(f'content_type is {request.content_type}')
            try:
                content = request.json 
                # print(f'content:{content} and type is:{type(content)}')
                content_json = json.dumps(content)
                # print(f'content_json:{content_json}')
                print(f'Sending to model infernce server')
                _reponse = TCPClient.submit_request(content) #process_request(content)
                print(f'Received results from tcp client-server model server')
                print("_reponse:",len(_reponse),type(_reponse),_reponse,sep=" # ")
                return _reponse
            except Exception as e:
                print("####### Exception occured#####:",e)
                error = e
                return jsonify({
                      "message":"success",
                      "status": 400,
                      "data": "Input is not in JSON/ transcripts key not found in input",
                      "error": str(error)
                    })

        elif (request.content_type.startswith('multipart/form-data; boundary=')):
            print(f'content_type is {request.content_type}')         
            uploaded_json_file = request.files['file']   
            location = f'{os.sep}MODELS{os.sep}KPO'
            source_json_inference = f'{location}{os.sep}SOURCE_INFERENCE'
            uploaded_json_file.save(os.path.join(source_json_inference, uploaded_json_file.filename))
            return jsonify({
                      "message":"success",
                      "status": 200,
                      "data": "Json File Stored in Inference Directory",
                      "file_name":uploaded_json_file.filename,
                      "path": source_json_inference
                    })            

    except KeyError  as e:
        return jsonify({'message':"Could not process request", 'status': 500, 'exception' : e})
    
    except Exception as e:
        print (e)
        return jsonify({'message':"Could not process request", 'status': 400, 'exception' : e})


if __name__ == "__main__":
   server.run(host='0.0.0.0',port=9002, debug=True)
