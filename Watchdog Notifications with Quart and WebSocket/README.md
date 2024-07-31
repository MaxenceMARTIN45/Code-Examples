# Watchdog Notifications with Quart and WebSocket

This project uses Quart, an asynchronous micro-framework for Python, in conjunction with WebSocket to provide real-time notifications when files are modified in a monitored directory. It also utilizes Watchdog for filesystem monitoring and Hypercorn to serve the Quart application.

## Installation

1. **Create and Activate a Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

- **Run the Application with Hypercorn:**
   ```bash
   hypercorn application:app
   ```
- **Start the Server:** After running the above command, the server will start, and you can access the application at `http://localhost:8000` by default.
- **Check that the watcher is working properly:** Modify the contents of the `history/hello.py` file and save it. You should see the modification in the terminal as well as in the web page `http://localhost:8000`.
