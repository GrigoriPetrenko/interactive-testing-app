#!/usr/bin/env python3
"""
Startup script for the Web-based Interactive Testing Application
"""

import os
import sys
import webbrowser
import time
import threading
from web_app import app

def open_browser():
    """Open the web browser after a short delay."""
    time.sleep(1.5)
    webbrowser.open('http://localhost:5000')

def main():
    """Main startup function."""
    print("=" * 60)
    print("INTERACTIVE TESTING APPLICATION - WEB VERSION")
    print("=" * 60)
    print()
    print("Starting web server...")
    print("Web interface will be available at: http://localhost:5000")
    print("Sample questions file: sample_questions.json")
    print()
    print("Features:")
    print("  - Modern web interface")
    print("  - Multiple question types")
    print("  - Interactive testing")
    print("  - Real-time feedback")
    print("  - Results export")
    print("  - Responsive design")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    print()

    # Start browser in a separate thread
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()

    try:
        # Run the Flask app
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True,
            use_reloader=False  # Disable reloader to prevent double startup
        )
    except KeyboardInterrupt:
        print("\n\nServer stopped by user")
        print("Thank you for using the Interactive Testing Application!")
    except Exception as e:
        print(f"\nError starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()




