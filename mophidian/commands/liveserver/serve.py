import logging
from .observe import WatchFiles       
from compiler.setup import init_static

_open_delay = 2

def serve(open: bool, content: str = "./content/", pages: str = "./pages/"):
    """Automatically reload browser tab upon file modification."""
    
    # Start by moving all static files to the site directory
    init_static()
    
    from livereload import Server
    server = Server()
    server.watch("./site/**/*")

    # Use watchdog as to have an incremental build system
    watch_files = WatchFiles(content_dir=content, pages_dir=pages)
    watch_files.start()
    
    # Start livereload server and auto open site in browser
    try:
        server.serve(port=3000, host="localhost", root="site/", open_url_delay=_open_delay if open else None)
    finally:
        # If the server is shutdown also stop watchdog
        watch_files.stop()
        watch_files.join()