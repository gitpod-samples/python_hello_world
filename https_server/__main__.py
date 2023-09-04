import ssl
import http.server
import socketserver
from art import text2art
from pathlib import Path
from .certgen import generate_cert_and_key

# Generate self-signed certificate and key
parent_directory = Path(__file__).parent
keyfile_path = f"{parent_directory}/key.pem"
certfile_path = f"{parent_directory}/cert.pem"
generate_cert_and_key(keyfile_path, certfile_path)

# Create an SSL context
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(
    keyfile=keyfile_path,
    certfile=certfile_path,
)


# A simple HTTP request handler
class SimpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        message = (
            "<pre>" + text2art("Hello from Gitpod, over TLS!", font="mini") + "</pre>"
        )
        self.wfile.write(message.encode("utf-8"))


# Create the socket server
host = "localhost"
port = 8080
with socketserver.TCPServer((host, port), SimpleHTTPRequestHandler) as httpd:
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
    print(f"Server started at https://{host}:{port}")
    httpd.serve_forever()
