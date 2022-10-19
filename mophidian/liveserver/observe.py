import threading
from typing import TextIO
from watchdog.observers import Observer

from compiler.build import Build
from .WatchHandlers import WatchContent, WatchPages, WatchStatic

all = ["WatchFiles"]


class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self, *args, **kwargs):
        super().__init__(daemon=True, *args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


class WatchFiles(StoppableThread):
    def __init__(self, build: Build, stdout: TextIO):
        super().__init__()

        # Allow for custom watched dirs
        self.build = build
        self.stdout = stdout

    def run(self):
        # Init file event handlers
        content_event_handler = WatchContent(build=self.build, stdout=self.stdout)
        page_event_handler = WatchPages(build=self.build, stdout=self.stdout)
        static_event_handler = WatchStatic(stdout=self.stdout)

        # Create observer and schedule to observe content and pages
        observer = Observer()

        observer.schedule(content_event_handler, "content/", recursive=True)
        observer.schedule(page_event_handler, "pages/", recursive=True)
        observer.schedule(static_event_handler, 'static/', recursive=True)

        # Start observing files
        observer.start()
        while observer.is_alive() and not self.stopped():
            observer.join(1)

        # Stop observing files
        observer.stop()
        observer.join()