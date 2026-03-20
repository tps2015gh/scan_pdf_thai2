import http.server
import socketserver
import os
import sys

# Set the port for the web server
PORT = 8001  # Using a different port to avoid conflict with serve_md.py

# Define the path to the HTML file you want to serve
HTML_FILE_PATH = os.path.join("HTMLFile", "howtorun.html")

class HTMLHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Only serve the specific HTML file
        if self.path == '/' or self.path == '/howtorun.html':
            self.serve_specific_html()
        else:
            # For any other requests, return 404
            self.send_error(404, "File Not Found")

    def serve_specific_html(self):
        if not os.path.exists(HTML_FILE_PATH):
            self.send_error(404, "HTML file not found: " + HTML_FILE_PATH)
            return

        try:
            with open(HTML_FILE_PATH, 'rb') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_error(500, "Error serving HTML file: " + str(e))


if __name__ == "__main__":
    # Change the current working directory to the script's directory
    # so that HTML_FILE_PATH is resolved correctly relative to the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    server_address = ("", PORT)
    try:
        with socketserver.TCPServer(server_address, HTMLHandler) as httpd:
            print("\n[🚀] HTML Server started at: http://localhost:" + str(PORT))
            print("[i] Serving: " + HTML_FILE_PATH)
            print("[i] Open this link in your browser: http://localhost:" + str(PORT))
            print("[i] Press Ctrl+C to stop the server.")
            httpd.serve_forever()
    except Exception as e:
        print("\n[!] Error starting server: " + str(e))
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n[👋] Server stopping...")
