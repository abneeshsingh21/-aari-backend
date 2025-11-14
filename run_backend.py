#!/usr/bin/env python3
"""
Standalone backend launcher - no working directory issues
"""
import sys
import os

# Ensure we're in the right directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
sys.path.insert(0, script_dir)

# Now import and run
if __name__ == '__main__':
    from app import app
    print(f"Starting AARI Backend Server...")
    print(f"Working directory: {os.getcwd()}")
    print(f"Running on http://0.0.0.0:5000")
    app.run(debug=False, host='0.0.0.0', port=5000, threaded=True)
