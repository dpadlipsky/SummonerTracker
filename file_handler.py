from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileModifiedHandler(FileSystemEventHandler):
    def __init__(self, path, file_name, callback):
        self.file_name = file_name
        self.callback = callback

        self.observer = Observer()
        self.observer.schedule(self, path, recursive=False)
        self.observer.start()

    def stop(self):
        self.observer.stop()
        self.observer.join()

    def on_modified(self, event): 
        if not event.is_directory and event.src_path.endswith(self.file_name):
            self.callback()
