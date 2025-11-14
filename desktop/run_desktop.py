#!/usr/bin/env python3
"""
Standalone desktop assistant launcher - no working directory issues
"""
import sys
import os

# Ensure we're in the right directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
sys.path.insert(0, script_dir)

# Now import and run
if __name__ == '__main__':
    from desktop_assistant import main
    print(f"Starting AARI Desktop Assistant...")
    print(f"Working directory: {os.getcwd()}")
    main()
