from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from logger import get_logger
import settings
from photos import reload_photo

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
        logger.info(f"{event.event_type}: {event.src_path}")
        if not event.is_directory:
            reload_photo(event.src_path)
