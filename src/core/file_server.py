"""
Simple HTTP file server for serving local audio files to the browser runtime.

The browser sandbox prevents direct access to local files, so we serve them
via HTTP on localhost.
"""
import os
import threading
import http.server
import socketserver
from pathlib import Path
from typing import Optional, Tuple
import socket


class CORSHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP handler with CORS headers for cross-origin audio loading."""

    def __init__(self, *args, directory=None, **kwargs):
        self._directory = directory
        super().__init__(*args, directory=directory, **kwargs)

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Range')
        self.send_header('Access-Control-Expose-Headers', 'Content-Length, Content-Range')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()


class AudioFileServer:
    """Serves local audio files via HTTP for browser runtime access."""

    _instance: Optional['AudioFileServer'] = None
    _lock = threading.Lock()

    def __init__(self):
        self.server: Optional[socketserver.TCPServer] = None
        self.server_thread: Optional[threading.Thread] = None
        self.port: int = 0
        self.serving_dir: Optional[Path] = None

    @classmethod
    def get_instance(cls) -> 'AudioFileServer':
        """Get singleton instance."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    def _find_free_port(self) -> int:
        """Find a free port on localhost."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('127.0.0.1', 0))
            return s.getsockname()[1]

    def start(self, directory: Path) -> int:
        """Start serving files from the given directory. Returns port number."""
        # If already serving same directory, return existing port
        if self.server and self.serving_dir == directory:
            return self.port

        # Stop existing server if running
        self.stop()

        self.serving_dir = directory
        self.port = self._find_free_port()

        # Create handler that serves from the specified directory with CORS
        directory_str = str(directory)
        handler = lambda *args, **kwargs: CORSHTTPRequestHandler(
            *args, directory=directory_str, **kwargs
        )

        # Create server with SO_REUSEADDR
        socketserver.TCPServer.allow_reuse_address = True
        self.server = socketserver.TCPServer(('127.0.0.1', self.port), handler)

        # Run in background thread
        self.server_thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.server_thread.start()

        return self.port

    def stop(self):
        """Stop the file server."""
        if self.server:
            self.server.shutdown()
            self.server = None
            self.server_thread = None
            self.serving_dir = None
            self.port = 0

    def get_url_for_file(self, file_path: str) -> Optional[str]:
        """Get HTTP URL for a local file. Starts server if needed."""
        path = Path(file_path).resolve()

        if not path.exists():
            return None

        # Start server in file's directory
        port = self.start(path.parent)

        # Return URL
        return f"http://127.0.0.1:{port}/{path.name}"


def get_http_url_for_local_file(file_path: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Convert a local file path to an HTTP URL by serving it.

    Args:
        file_path: Local file path

    Returns:
        Tuple of (http_url, error_message). If successful, error is None.
    """
    # Check if already an HTTP URL
    if file_path.startswith(('http://', 'https://')):
        return file_path, None

    # Resolve path
    path = Path(file_path).expanduser().resolve()

    if not path.exists():
        return None, f"File not found: {file_path}"

    if not path.is_file():
        return None, f"Not a file: {file_path}"

    # Get/start file server
    server = AudioFileServer.get_instance()
    url = server.get_url_for_file(str(path))

    if url:
        return url, None
    else:
        return None, f"Failed to serve file: {file_path}"
