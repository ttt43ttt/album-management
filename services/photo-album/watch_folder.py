from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from imutils import paths

from logger import get_logger
import settings
from photos import reload_photo, reload_photos

logger = get_logger()


def start_watch_files():
    folder = settings.USER_PHOTO_HOME
    event_handler = FileChangeEventHandler()
    observer = Observer()
    observer.schedule(event_handler, folder, recursive=True)
    observer.start()
    logger.info(f"Started to watch folder {folder}")


class FileChangeEventHandler(FileSystemEventHandler):
    def __init__(self):
        pass

    def on_any_event(self, event):
        logger.info(event)

    def on_created(self, event):
        if event.is_directory:
            pass
        else:
            reload_photo(event.src_path)

    def on_deleted(self, event):
        if event.is_directory:
            pass
        else:
            reload_photo(event.src_path)

    def on_modified(self, event):
        if event.is_directory:
            pass
        else:
            reload_photo(event.src_path)

    def on_moved(self, event):
        if event.is_directory:
            pass
        else:
            reload_photo(event.src_path)
            reload_photo(event.dest_path)
