from flask import Flask, request, jsonify, render_template
import socket
import re

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    data = request.get_json()
    domain = data.get('domain', '').strip()
    
    if domain.startswith("http://") or domain.startswith("https://"):
        domain = domain.split("//")[-1].split("/")[0].split('?')[0]
    
    if is_valid_domain(domain):
        ip_address = get_ip_address(domain)
        if ip_address:
            return jsonify({"message": f"The IP address of {domain} is {ip_address}"})
        else:
            return jsonify({"message": f"Could not retrieve the IP address for {domain}"}), 400
    else:
        return jsonify({"message": "Invalid URL or domain. Please enter a valid website URL or domain name."}), 400

if __name__ == '__main__':
    app.run(debug=True)
