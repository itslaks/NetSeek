from flask import Flask, request, jsonify, render_template
import socket
import re
import requests

app = Flask(__name__)

def is_valid_domain(domain):
    # Regular expression to check the validity of a domain name
    regex = re.compile(
        r'^(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)$', re.IGNORECASE)
    return re.match(regex, domain) is not None

def get_ip_address(domain):
    try:
        ip_address = socket.gethostbyname(domain)
        return ip_address
    except socket.gaierror:
        return None

def get_ip_info(ip_address, api_key):
    # Constructing URL for IPinfo API request
    url = f"https://ipinfo.io/{ip_address}/json?token={api_key}"
    response = requests.get(url)
    return response.json()

@app.route('/')
def index():
    # Render the index.html template
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    # Receive POST data containing 'domain' key
    data = request.get_json()
    domain = data.get('domain', '').strip()
    
    # Handle URLs with protocols included
    if domain.startswith("http://") or domain.startswith("https://"):
        domain = domain.split("//")[-1].split("/")[0].split('?')[0]
    
    if is_valid_domain(domain):
        # Get IP address corresponding to the domain
        ip_address = get_ip_address(domain)
        if ip_address:
            # Replace 'your_ipinfo_api_key' with your actual IPinfo API key
            api_key = "8e6847c71ee1d7"
            # Get detailed information about the IP address
            ip_info = get_ip_info(ip_address, api_key)
            return jsonify({
                "message": f"The IP address of {domain} is {ip_address}",
                "ip_info": ip_info
            })
        else:
            return jsonify({"message": f"Could not retrieve the IP address for {domain}"}), 400
    else:
        return jsonify({"message": "Invalid URL or domain. Please enter a valid website URL or domain name."}), 400

if __name__ == '__main__':
    # Run the Flask application in debug mode
    app.run(debug=True)
