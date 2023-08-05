import socket
import json
from solution_efe_config import configConstants

CLIENT_DOCUMENT=configConstants.CLIENTS['document']

def documentServiceDocumentById(data):
    try:
        event = {'event':'document-service-document-by-id','data': data}
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((CLIENT_DOCUMENT['host'], CLIENT_DOCUMENT['port']))
            sock.sendall(bytes(json.dumps(event) + "\n", "utf-8"))
            received = str(sock.recv(1024), "utf-8")
        response=json.loads(received)
        return response
    except Exception as e:
        return {'code': 500,'status': False,'data':str(e)}