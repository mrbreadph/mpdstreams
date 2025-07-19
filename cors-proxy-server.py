#!/usr/bin/env python3
"""
Simple CORS Proxy Server for MPD Streaming
Solves CORS issues when accessing MPD streams from local HTML files
"""

import http.server
import socketserver
import urllib.request
import urllib.parse
from urllib.error import URLError, HTTPError
import sys
import threading
import webbrowser
import time
import ssl

class CORSProxyHandler(http.server.SimpleHTTPRequestHandler):
    
    def end_headers(self):
        # Always add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, HEAD')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('Access-Control-Max-Age', '86400')
        super().end_headers()
    
    def do_OPTIONS(self):
        # Handle preflight requests
        self.send_response(200)
        self.end_headers()
    
    def do_GET(self):
        if self.path.startswith('/proxy/'):
            self.handle_proxy_request()
        else:
            super().do_GET()
    
    def do_POST(self):
        if self.path.startswith('/proxy/'):
            self.handle_proxy_request()
        else:
            super().do_POST()
    
    def handle_proxy_request(self):
        try:
            # Extract target URL
            target_url = self.path[7:]  # Remove '/proxy/' prefix
            
            if not target_url.startswith(('http://', 'https://')):
                self.send_error(400, 'Invalid URL format')
                return
            
            print(f"🔄 Proxying: {target_url}")
            
            # Prepare headers
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            # Copy relevant headers from original request
            for header in ['Accept', 'Accept-Language', 'Accept-Encoding']:
                if header in self.headers:
                    headers[header] = self.headers[header]
            
            # Create SSL context that doesn't verify certificates (for problematic servers)
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            
            # Create request
            req = urllib.request.Request(target_url, headers=headers)
            
            # Make request with SSL context
            try:
                response = urllib.request.urlopen(req, timeout=30, context=ssl_context)
            except Exception as e:
                # Try without SSL context for HTTP URLs
                response = urllib.request.urlopen(req, timeout=30)
            
            # Send response
            self.send_response(response.getcode())
            
            # Copy important headers
            for header, value in response.headers.items():
                if header.lower() not in ['connection', 'transfer-encoding']:
                    self.send_header(header, value)
            
            self.end_headers()
            
            # Stream the response
            while True:
                chunk = response.read(8192)
                if not chunk:
                    break
                try:
                    self.wfile.write(chunk)
                except (BrokenPipeError, ConnectionResetError):
                    break
            
            response.close()
            print(f"✅ Successfully proxied: {target_url}")
            
        except HTTPError as e:
            print(f"❌ HTTP Error {e.code}: {e.reason} for {target_url}")
            self.send_error(e.code, f"Upstream server error: {e.reason}")
            
        except URLError as e:
            print(f"❌ URL Error: {e.reason} for {target_url}")
            self.send_error(502, f"Connection error: {e.reason}")
            
        except Exception as e:
            print(f"❌ Proxy error: {str(e)} for {target_url}")
            self.send_error(500, f"Proxy error: {str(e)}")
    
    def log_message(self, format, *args):
        # Suppress default logging for cleaner output
        return

def start_server(port=8000):
    """Start the CORS proxy server"""
    try:
        with socketserver.TCPServer(("", port), CORSProxyHandler) as httpd:
            print(f"🚀 CORS Proxy Server running at http://localhost:{port}")
            print(f"📁 Serving files from: {httpd.server_address}")
            print(f"🌐 Open your browser and go to: http://localhost:{port}/mpd-player-cors-fixed.html")
            print(f"🔧 Proxy endpoint: http://localhost:{port}/proxy/[URL]")
            print("🛑 Press Ctrl+C to stop the server")
            
            # Auto-open browser after a short delay
            def open_browser():
                time.sleep(2)
                webbrowser.open(f'http://localhost:{port}/mpd-player-cors-fixed.html')
            
            browser_thread = threading.Thread(target=open_browser)
            browser_thread.daemon = True
            browser_thread.start()
            
            httpd.serve_forever()
            
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"❌ Port {port} is already in use. Trying port {port + 1}...")
            start_server(port + 1)
        else:
            print(f"❌ Error starting server: {e}")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        sys.exit(0)

if __name__ == "__main__":
    print("🎬 MPD Stream Player - CORS Proxy Server")
    print("=" * 50)
    start_server()
