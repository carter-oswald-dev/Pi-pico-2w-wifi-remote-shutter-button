import network
import socket
import time
from machine import Pin

# -- Pin setup --
shutter = Pin(0, Pin.OUT, value=1)

# -- WiFi Access Point --
AP_SSID = "PicoShutter"

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(ssid=AP_SSID, security=0)

while not ap.active():
    time.sleep(0.1)

print("Access point active")
print("SSID:", AP_SSID)
print("IP:", ap.ifconfig()[0])

# -- Web page HTML --
HTML = """\
HTTP/1.0 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Pico Shutter</title>
  <style>
    body {
      background: #111;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 100vh;
      margin: 0;
      font-family: sans-serif;
    }
    h1 {
      color: #fff;
      font-size: 1.4em;
      margin-bottom: 40px;
    }
    button {
      background: #fff;
      border: none;
      border-radius: 50%;
      width: 180px;
      height: 180px;
      font-size: 1.1em;
      font-weight: bold;
      color: #111;
      cursor: pointer;
      box-shadow: 0 0 0 8px #444;
    }
    button:active {
      background: #ddd;
    }
    #status {
      color: #aaa;
      margin-top: 30px;
      font-size: 0.9em;
    }
  </style>
</head>
<body>
  <h1>Pico Shutter</h1>
  <button onclick="shoot()">SHUTTER</button>
  <p id="status">Ready</p>
  <script>
    function shoot() {
      document.getElementById('status').innerText = 'Firing...';
      fetch('/shutter').then(() => {
        document.getElementById('status').innerText = 'Done!';
        setTimeout(() => {
          document.getElementById('status').innerText = 'Ready';
        }, 1000);
      });
    }
  </script>
</body>
</html>
"""

SHUTTER_RESP = """\
HTTP/1.0 200 OK
Content-Type: text/plain

ok
"""

def fire_shutter():
    shutter.value(0)
    time.sleep_ms(100)
    shutter.value(1)
    print("Shutter fired")

# -- Web server --
addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(5)
print("Listening on port 80 ...")

while True:
    try:
        conn, addr = s.accept()
        request = conn.recv(1024).decode()
        if "/shutter" in request:
            fire_shutter()
            conn.send(SHUTTER_RESP)
        else:
            conn.send(HTML)
        conn.close()
    except Exception as e:
        print("Error: " + str(e))
        try:
            conn.close()
        except:
            pass
