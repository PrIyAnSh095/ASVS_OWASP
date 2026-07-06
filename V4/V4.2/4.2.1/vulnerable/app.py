#!/usr/bin/env python3
"""
ASVS 4.2.1 Vulnerable Lab - Entry point
Starts both the proxy (port 5001) and the backend (port 8000) servers.
"""
import threading
import proxy
import backend

if __name__ == '__main__':
    # Start backend in a daemon thread
    backend_thread = threading.Thread(target=backend.run_server, daemon=True)
    backend_thread.start()
    # Start proxy in the main thread
    proxy.run_server()
