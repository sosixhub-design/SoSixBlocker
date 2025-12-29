from flask import Flask, os

app = Flask(__name__)

# =========================================================
# [[ 1. PASTE YOUR SCRIPT BELOW ]]
# Put your code between the triple quotes r""" ... """
# =========================================================
MY_LUASCRIPT = r"""
-- Paste your Lua script here
print("Sonix: Script Loaded Successfully!")

local ScreenGui = Instance.new("ScreenGui", game:GetService("CoreGui"))
local TextLabel = Instance.new("TextLabel", ScreenGui)
TextLabel.Size = UDim2.new(0, 200, 0, 50)
TextLabel.Position = UDim2.new(0.5, -100, 0.5, -25)
TextLabel.Text = "Sonix Precision Loaded"
"""
# =========================================================

@app.route('/')
def home():
    return "Sonix Loader: Online", 200

@app.route('/Blocker', methods=['GET'])
def load():
    # This serves the raw string directly to your game
    return MY_LUASCRIPT, 200, {'Content-Type': 'text/plain'}

if __name__ == '__main__':
    # Binds to Render's port
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
