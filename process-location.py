from flask import Flask, request, render_template
import requests
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    # Get the visitor's IP address
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get('User-Agent')

    try:
        geo = requests.get(f"http://ip-api.com/json/{ip}").json()
        city = geo.get('city')
        region = geo.get('regionName')
        country = geo.get('country')
        lat = geo.get('lat')
        lon = geo.get('lon')
    except:
        city = region = country = lat = lon = "Unknown"

    log_entry = (
        f"\n----- Visitor Logged -----\n"
        f"Time: {datetime.now()}\n"
        f"IP: {ip}\n"
        f"Location: {city}, {region}, {country}\n"
        f"Coordinates: {lat}, {lon}\n"
        f"User-Agent: {user_agent}\n"
        "---------------------------\n"
    )

    print(log_entry, flush=True)


    return render_template("index.html")

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
