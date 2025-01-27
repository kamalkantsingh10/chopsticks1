from http.server import HTTPServer, BaseHTTPRequestHandler
import subprocess

class CameraHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=frame')
        self.end_headers()
        cmd = ['libcamera-vid', '-n', '-t', '0', '--inline', '--codec', 'mjpeg', '-o', '-']
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        try:
            while True:
                self.wfile.write(b'--frame\r\n')
                self.send_header('Content-type', 'image/jpeg')
                self.end_headers()
                frame = p.stdout.read(4096)
                if not frame:
                    break
                self.wfile.write(frame)
        except:
            p.kill()

server = HTTPServer(('0.0.0.0', 8080), CameraHandler)
server.serve_forever()