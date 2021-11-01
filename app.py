from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os

HOST = '127.0.0.1'
PORT = 8080

# Create database file
if not os.path.exists('db.json'):
    with open('db.json', "w+") as db:
        db.write('{\n}')

# Read database file
with open('db.json', "r") as db:
    storage_file = json.load(db)

# Subclass Base HTTP Request Handler and define request methods
class ImplementedHTTPRequestHandler(BaseHTTPRequestHandler):

    # Set basic headers for the response
    def _set_headers(self, status_code: int):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/json')
        self.end_headers()

    # Get content from request
    def _get_content(self):
        length = int(self.headers['Content-Length'])
        content_bytes = self.rfile.read(length)
        content = str(content_bytes).strip('b\'').replace('\\n','').replace('\\t','')
        return content
    
    # GET
    def do_GET(self):
        # Get POST body
        request_content = self._get_content()

        # Read database
        with open('db.json', 'r') as db:
            json_data = json.load(db)

        # If key in database
        if request_content in json_data:
            value = json_data.get(request_content)
            self._set_headers(200)
            self.wfile.write(json.dumps(value).encode())
        else:
            self._set_headers(404)

    # POST
    def do_POST(self):
        # Get POST body
        request_content = self._get_content()

        # Read database
        with open('db.json', 'r') as db:
            json_data = json.load(db)

        # If key in database already
        if request_content in json_data:
            self._set_headers(409)
        # Create new entry
        else:
            json_data[request_content] = ""
            with open("db.json", "w") as file:
                json.dump(json_data, file, indent = 4, sort_keys=True)
            self._set_headers(201)

    # PUT
    def do_PUT(self):
        # Get POST body
        request_content = self._get_content()
        request_dict = json.loads(request_content)
        request_key = list(request_dict.keys())[0]

        # Read database
        with open('db.json', 'r') as db:
            json_data = json.load(db)

        # Update if key in database
        if request_key in json_data:
            json_data.update(request_dict)
            with open("db.json", "w") as file:
                json.dump(json_data, file, indent = 4, sort_keys=True)
            self._set_headers(200)
        else:
            self._set_headers(404)

    # DELETE
    def do_DELETE(self):
        # Get POST body
        request_content = self._get_content()

        # Read database
        with open('db.json', 'r') as db:
            json_data = json.load(db)

        # If key in database
        if request_content in json_data:
            json_data.pop(request_content, None)
            with open("db.json", "w") as file:
                json.dump(json_data, file, indent = 4, sort_keys=True)
                self._set_headers(200)
        else:
            self._set_headers(404)


# Initialize HTTP Server
http_server = HTTPServer((HOST, PORT), ImplementedHTTPRequestHandler)
print(f'Serving HTTP server on {HOST=} and {PORT=}')
http_server.serve_forever()