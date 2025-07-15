#!/usr/bin/env python3
"""
Startup script for Real Estate Deal Screener & Negotiation Copilot.
Provides easy commands to run the backend and frontend.
"""

import subprocess
import sys
import os
import time
import webbrowser
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import fastapi
        import streamlit
        import crewai
        import openai
        import plotly
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def start_backend():
    """Start the FastAPI backend server."""
    print("🚀 Starting FastAPI backend...")
    
    backend_path = Path("backend")
    if not backend_path.exists():
        print("❌ Backend directory not found")
        return False
    
    try:
        # Start backend server
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", 
            "backend.main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000",
            "--reload"
        ], cwd=".")
        
        print("✅ Backend server started at http://localhost:8000")
        print("📚 API documentation available at http://localhost:8000/docs")
        
        return process
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        return False

def start_frontend():
    """Start the Streamlit frontend."""
    print("🎨 Starting Streamlit frontend...")
    
    frontend_path = Path("frontend")
    if not frontend_path.exists():
        print("❌ Frontend directory not found")
        return False
    
    try:
        # Start frontend server
        process = subprocess.Popen([
            sys.executable, "-m", "streamlit", 
            "run", "frontend/app.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ], cwd=".")
        
        print("✅ Frontend server started at http://localhost:8501")
        
        # Open browser after a short delay
        time.sleep(3)
        webbrowser.open("http://localhost:8501")
        
        return process
    except Exception as e:
        print(f"❌ Error starting frontend: {e}")
        return False

def main():
    """Main function to start the application."""
    print("🏠 Real Estate Deal Screener & Negotiation Copilot")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Check for environment variables
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: OPENAI_API_KEY not set")
        print("   Create a .env file with your OpenAI API key:")
        print("   OPENAI_API_KEY=your_api_key_here")
        print("   The app will work with mock data without the API key")
    
    print("\nChoose an option:")
    print("1. Start Backend Only")
    print("2. Start Frontend Only")
    print("3. Start Both (Backend + Frontend)")
    print("4. Exit")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        process = start_backend()
        if process:
            try:
                print("\n🔄 Backend running... Press Ctrl+C to stop")
                process.wait()
            except KeyboardInterrupt:
                print("\n🛑 Stopping backend...")
                process.terminate()
    
    elif choice == "2":
        process = start_frontend()
        if process:
            try:
                print("\n🔄 Frontend running... Press Ctrl+C to stop")
                process.wait()
            except KeyboardInterrupt:
                print("\n🛑 Stopping frontend...")
                process.terminate()
    
    elif choice == "3":
        print("\n🚀 Starting both backend and frontend...")
        
        backend_process = start_backend()
        if not backend_process:
            return
        
        # Wait a moment for backend to start
        time.sleep(2)
        
        frontend_process = start_frontend()
        if not frontend_process:
            backend_process.terminate()
            return
        
        try:
            print("\n🔄 Both servers running... Press Ctrl+C to stop")
            print("📱 Frontend: http://localhost:8501")
            print("🔧 Backend: http://localhost:8000")
            print("📚 API Docs: http://localhost:8000/docs")
            
            # Wait for either process to finish
            while backend_process.poll() is None and frontend_process.poll() is None:
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n🛑 Stopping servers...")
            backend_process.terminate()
            frontend_process.terminate()
    
    elif choice == "4":
        print("Goodbye!")
    
    else:
        print("❌ Invalid choice. Please enter 1-4.")

if __name__ == "__main__":
    main() 