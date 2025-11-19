"""
Boot and Verify App Startup
============================
Starts the Streamlit app and verifies it runs without errors.
"""

import subprocess
import sys
import time
import os
import signal
from pathlib import Path

def check_port(port=8501):
    """Check if port is in use"""
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', port))
        sock.close()
        return result == 0
    except:
        return False

def main():
    """Boot the app"""
    print("=" * 60)
    print("Booting Enterprise LangChain AI Workbench")
    print("=" * 60)
    
    # Check if already running
    if check_port(8501):
        print("App appears to be running on port 8501")
        print("Access at: http://localhost:8501")
        return 0
    
    # Verify imports first
    print("\n1. Verifying imports...")
    try:
        from agents import MultiAgentSystem
        from advanced_rag import AdvancedRAGSystem
        print("   OK: Core modules import successfully")
    except Exception as e:
        print(f"   FAIL: Import error: {e}")
        return 1
    
    # Check syntax
    print("\n2. Checking syntax...")
    try:
        with open('streamlit_app.py', 'r', encoding='utf-8') as f:
            compile(f.read(), 'streamlit_app.py', 'exec')
        print("   OK: Syntax valid")
    except SyntaxError as e:
        print(f"   FAIL: Syntax error: {e}")
        return 1
    
    # Start Streamlit
    print("\n3. Starting Streamlit app...")
    print("   This will open in your browser")
    print("   URL: http://localhost:8501")
    print("\n   Press Ctrl+C to stop the app")
    print("=" * 60)
    
    try:
        # Start Streamlit
        process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.port", "8501"
        ])
        
        # Wait a bit to see if it starts
        time.sleep(3)
        
        if process.poll() is None:
            print("\nSUCCESS: App started successfully!")
            print("=" * 60)
            print("\nApp is running at: http://localhost:8501")
            print("\nPress Ctrl+C to stop")
            
            # Wait for user interrupt
            try:
                process.wait()
            except KeyboardInterrupt:
                print("\n\nStopping app...")
                process.terminate()
                process.wait()
                print("App stopped")
            
            return 0
        else:
            print("FAIL: App process exited unexpectedly")
            return 1
            
    except FileNotFoundError:
        print("FAIL: Streamlit not found")
        print("Solution: Run 'python setup.py' to install dependencies")
        return 1
    except Exception as e:
        print(f"FAIL: Error starting app: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())

