#!/usr/bin/env python3
"""
Alternative Simple HTTP Server for MPD Streaming
Uses basic HTTP server without proxy functionality
"""

import http.server
import socketserver
import webbrowser
import threading
import time
import os

class SimpleCORSHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, HEAD')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('Cache-Control', 'no-cache')
        super().end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()
    
    def log_message(self, format, *args):
        print(f"📄 {args[0]} - {args[1]}")

def start_simple_server(port=8000):
    """Start a simple HTTP server without proxy functionality"""
    try:
        # Change to the directory containing the HTML files
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        
        handler = SimpleCORSHandler
        
        with socketserver.TCPServer(("", port), handler) as httpd:
            print(f"🚀 Simple CORS Server running at http://localhost:{port}")
            print(f"📁 Serving files from: {os.getcwd()}")
            print(f"🌐 Open: http://localhost:{port}/mpd-player.html")
            print("🛑 Press Ctrl+C to stop")
            print()
            print("📋 Available files:")
            for file in os.listdir('.'):
                if file.endswith('.html'):
                    print(f"   • http://localhost:{port}/{file}")
            print()
            
            # Auto-open browser
            def open_browser():
                time.sleep(1)
                if os.path.exists('mpd-player-cors-fixed.html'):
                    webbrowser.open(f'http://localhost:{port}/mpd-player-cors-fixed.html')
                elif os.path.exists('mpd-player.html'):
                    webbrowser.open(f'http://localhost:{port}/mpd-player.html')
            
            browser_thread = threading.Thread(target=open_browser)
            browser_thread.daemon = True
            browser_thread.start()
            
            httpd.serve_forever()
            
    except OSError as e:
        if e.errno == 48 or "Address already in use" in str(e):
            print(f"❌ Port {port} is busy. Trying {port + 1}...")
            start_simple_server(port + 1)
        else:
            print(f"❌ Server error: {e}")
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")

if __name__ == "__main__":
    print("🎬 MPD Player - Simple HTTP Server")
    print("=" * 40)
    start_simple_server()
