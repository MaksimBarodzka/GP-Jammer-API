import http.client
import json
import time
from urllib.parse import urlencode

# Copy userAlias from GET /sdrs. Copy base from GET /interferences.
BASE = r"C:\Users\User\AppData\Local\GPSPATRON\GP-Jammer\Python data"

conn = http.client.HTTPConnection("localhost:5000")
json_headers = {"Content-Type": "application/json"}

# 1. List connected devices
conn.request("GET", "/gp-jammer/api/v1/sdrs")
response = conn.getresponse()
print("GET /sdrs", response.status)
print(response.read().decode())
print()

# 2. Device details
conn.request("GET", "/gp-jammer/api/v1/sdrs/SDR-1")
response = conn.getresponse()
print("GET SDR-1", response.status)
print(response.read().decode())
print()

conn.request("GET", "/gp-jammer/api/v1/sdrs/SDR-2")
response = conn.getresponse()
print("GET SDR-2", response.status)
print(response.read().decode())
print()

conn.request("GET", "/gp-jammer/api/v1/sdrs/SDR-3")
response = conn.getresponse()
print("GET SDR-3", response.status)
print(response.read().decode())
print()

# 3. Device settings
conn.request("GET", "/gp-jammer/api/v1/sdrs/SDR-1/settings")
response = conn.getresponse()
print("GET settings SDR-1", response.status)
print(response.read().decode())
print()

conn.request("GET", "/gp-jammer/api/v1/sdrs/SDR-2/settings")
response = conn.getresponse()
print("GET settings SDR-2", response.status)
print(response.read().decode())
print()

conn.request("GET", "/gp-jammer/api/v1/sdrs/SDR-3/settings")
response = conn.getresponse()
print("GET settings SDR-3", response.status)
print(response.read().decode())
print()

# 4. Update settings on one device
body = json.dumps({
    "IQ_rate": 40e6,
    "center_frequency": 1575.42e6,
    "gain": -45,
})
conn.request(
    "PUT",
    "/gp-jammer/api/v1/sdrs/SDR-1/settings",
    body=body,
    headers=json_headers,
)
response = conn.getresponse()
print("PUT settings SDR-1", response.status)
print(response.read().decode())
print()

# 5. Interference library
conn.request("GET", "/gp-jammer/api/v1/interferences")
response = conn.getresponse()
print("GET /interferences", response.status)
print(response.read().decode())
print()

# 6. Interference parameters (read-only)
query = urlencode({"base": BASE, "name": r"Basic Modulations\CHIRP"})
conn.request("GET", "/gp-jammer/api/v1/interferences/info?" + query)
response = conn.getresponse()
print("INFO CHIRP", response.status)
print(response.read().decode())
print()

query = urlencode({"base": BASE, "name": r"Basic Modulations\AWGN"})
conn.request("GET", "/gp-jammer/api/v1/interferences/info?" + query)
response = conn.getresponse()
print("INFO AWGN", response.status)
print(response.read().decode())
print()

query = urlencode({"base": BASE, "name": r"Basic Modulations\CW"})
conn.request("GET", "/gp-jammer/api/v1/interferences/info?" + query)
response = conn.getresponse()
print("INFO CW", response.status)
print(response.read().decode())
print()

# 7. Apply CHIRP on SDR-1, AWGN on SDR-2, CW on SDR-3
# Apply can take several seconds.
query = urlencode({"base": BASE, "name": r"Basic Modulations\CHIRP"})
body = json.dumps({
    "center_frequency": 1575.42e6,
    "IQ_rate": 40e6,
    "sweep_span": 20e6,
    "sweep_period": 10e-6,
})
conn.request(
    "POST",
    "/gp-jammer/api/v1/sdrs/SDR-1/interference?" + query,
    body=body,
    headers=json_headers,
)
response = conn.getresponse()
print("POST interference SDR-1 CHIRP", response.status)
print(response.read().decode())
print()

query = urlencode({"base": BASE, "name": r"Basic Modulations\AWGN"})
body = json.dumps({
    "center_frequency": 1575.42e6,
    "IQ_rate": 40e6,
    "noise_bandwidth": 10e6,
    "signal_duration": 0.005,
})
conn.request(
    "POST",
    "/gp-jammer/api/v1/sdrs/SDR-2/interference?" + query,
    body=body,
    headers=json_headers,
)
response = conn.getresponse()
print("POST interference SDR-2 AWGN", response.status)
print(response.read().decode())
print()

query = urlencode({"base": BASE, "name": r"Basic Modulations\CW"})
body = json.dumps({
    "center_frequency": 1575.42e6,
    "IQ_rate": 10e6,
})
conn.request(
    "POST",
    "/gp-jammer/api/v1/sdrs/SDR-3/interference?" + query,
    body=body,
    headers=json_headers,
)
response = conn.getresponse()
print("POST interference SDR-3 CW", response.status)
print(response.read().decode())
print()

# 8. Start all three
conn.request("POST", "/gp-jammer/api/v1/sdrs/SDR-1/start")
response = conn.getresponse()
print("START SDR-1", response.status)
print(response.read().decode())
print()

conn.request("POST", "/gp-jammer/api/v1/sdrs/SDR-2/start")
response = conn.getresponse()
print("START SDR-2", response.status)
print(response.read().decode())
print()

conn.request("POST", "/gp-jammer/api/v1/sdrs/SDR-3/start")
response = conn.getresponse()
print("START SDR-3", response.status)
print(response.read().decode())
print()

print("Waiting 20 seconds before stop...")
time.sleep(20)

# 9. Stop all three
conn.request("POST", "/gp-jammer/api/v1/sdrs/SDR-1/stop")
response = conn.getresponse()
print("STOP SDR-1", response.status)
print(response.read().decode())
print()

conn.request("POST", "/gp-jammer/api/v1/sdrs/SDR-2/stop")
response = conn.getresponse()
print("STOP SDR-2", response.status)
print(response.read().decode())
print()

conn.request("POST", "/gp-jammer/api/v1/sdrs/SDR-3/stop")
response = conn.getresponse()
print("STOP SDR-3", response.status)
print(response.read().decode())
print()

# 10. Generation logs
conn.request("GET", "/gp-jammer/api/v1/logs/gen")
response = conn.getresponse()
print("GET /logs/gen", response.status)
print(response.read().decode())

conn.close()
