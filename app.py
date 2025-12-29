import os
from flask import Flask, request

app = Flask(__name__)

# [[ YOUR PRIVATE SOSIX SCRIPT ]]
MY_LUASCRIPT = r"""
print("Sonix Hub: Securely Executed")
-- Paste your full Sosix Lua code here
"""

@app.route('/')
def health():
    return "Status: Operational", 200

@app.route('/Blocker', methods=['GET'])
def load():
    # Check the 'User-Agent'
    ua = request.headers.get('User-Agent', '').lower()
    
    # If the request comes from a Browser (Chrome, Safari, etc.)
    browsers = ['mozilla', 'chrome', 'safari', 'edge', 'opera', 'mobile']
    
    if any(b in ua for b in browsers):
        # This makes it look like the page doesn't exist to a normal person
        return "404 Not Found: The requested URL was not found on the server.", 404

    # If it's NOT a browser (like a Roblox Executor), send the script
    return MY_LUASCRIPT, 200, {'Content-Type': 'text/plain'}

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
