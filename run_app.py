#!/usr/bin/env python3
"""
Launcher script for Policy Navigator with React frontend
"""

import subprocess
import sys
import os
import time
import threading
from pathlib import Path

def run_backend():
    """Run Flask API server"""
    print("🚀 Starting Policy Navigator API server...")
    subprocess.run([sys.executable, "api_server.py"])

def run_frontend():
    """Run React development server"""
    print("🌐 Starting React frontend...")
    frontend_dir = Path("frontend")
    
    if not (frontend_dir / "node_modules").exists():
        print("📦 Installing React dependencies...")
        subprocess.run(["npm", "install"], cwd=frontend_dir, check=True)
    
    subprocess.run(["npm", "start"], cwd=frontend_dir)

def main():
    """Main launcher"""
    print("🏛️  Policy Navigator - Full Stack Application")
    print("=" * 50)
    
    # Check if frontend directory exists
    if not Path("frontend").exists():
        print("❌ Frontend directory not found. Please run this from the project root.")
        return
    
    # Start backend in a separate thread
    backend_thread = threading.Thread(target=run_backend, daemon=True)
    backend_thread.start()
    
    # Wait a moment for backend to start
    time.sleep(3)
    
    # Start frontend
    try:
        run_frontend()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down Policy Navigator...")
        sys.exit(0)

if __name__ == "__main__":
    main()