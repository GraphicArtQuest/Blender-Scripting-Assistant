"""
Directory Monitor

Watches a specified file or folder for changes. Will run subscribed scripts if changes detected.
"""

from collections import defaultdict
import os
import threading

from .console_messages.directory_monitor import DirectoryMonitorMessages as message

class DirectoryMonitor(object):
    """This class monitors a specified file or folder for any changes.

    Only one instance of this class can exist.

    The class uses properties for data validation. Accessing the private self._ values directly could cause
    instabilities."""

    def __init__(self):
        """The class uses properties for data validation. Accessing the private self._ values directly could cause
            instabilities."""
        self._polling_delay = .15       # Seconds
        self._directory = ""            # Can be a file or folder
        self._last_tracked_update = 0   # Comparison for file modified times
        self._last_tracked_filecount = 0    # Comparison to check for deleted files

        self._poll_timer = threading.Timer(self.polling_delay, self._poll)
        self._subscribers = defaultdict(list)
        
    def __new__(cls):
        # This class uses a singleton pattern to ensure only one timer exists.
        if not hasattr(cls, 'instance'):
            cls.instance = super(DirectoryMonitor, cls).__new__(cls)
        return cls.instance

    def get_polling_delay(self):
        return self._polling_delay
    
    def set_polling_delay(self, new_delay: float):
        try:
            check_polling_delay = float(new_delay)
            
        except:
            message.invalid_polling_delay(self.polling_delay)
            return

        if check_polling_delay <= 0:
            message.invalid_polling_delay(self.polling_delay)
            return
        
        self._polling_delay = check_polling_delay

    def get_active(self):
        return self._poll_timer.is_alive()

    def get_directory(self):
        return self._directory

    def set_directory(self, desired_directory: str):
        # May be a file or folder, but it has to exist
        if os.path.exists(str(desired_directory)):
            self._directory = str(desired_directory).strip('\\')
            self._last_tracked_filecount = self._num_files(self._directory)
            message.changed_directory(self._directory)
        else:
            message.unable_to_change_directory(desired_directory, self.directory)
    
    polling_delay = property(get_polling_delay, set_polling_delay)
    active = property(get_active)   # Read only. Turn on with 'watch()'
    directory = property(get_directory, set_directory)

    def subscribe(self, script: str, script_function) -> None:
        """ When another class subscribes to the monitor, any time monitor detects a change it will
        run all of the subscribed callback functions that were registered.

        @returns: a list of strings representing the header columns
        """
        self._subscribers[script].append(script_function)
    
    def unsubscribe(self, script: str) -> None:
        try:
            del self._subscribers[script]
        except:
            message.unable_to_unsubscribe(script)

    def clear_subscribers(self) -> None:
        self._subscribers.clear()

    def run_scripts(self) -> None:
        # Run all of the callback functions that have subscribed
        for script in self._subscribers.keys():
            for func in self._subscribers[script]:
                func()

    def _isNewerFileUpdate(self, file_path):
        # Will return boolean False if it is an older version that currently tracked.
        #   If it is newer, it will return that newer value.
        # 'file_path' has to be a safe file. Folders or files that do not exist throw errors.
        file_update_time = os.path.getmtime(file_path)

        if file_update_time > self._last_tracked_update:    # Only file changes (not folders) can trigger updates
            if self.active: # Only print after initialized and active
                message.found_updated_file(file_path)
        else:
            return 0
        
        self._last_tracked_update = file_update_time
        return file_update_time
    
    def _num_files(self, file_path):
        return  sum([len(files) for r, d, files in os.walk(file_path)])
    
    def _update_filecount(self):
        self._last_tracked_filecount = self._num_files(self.directory)
    
    def _isNewerFolderUpdate(self, folder_path, latest_folder_update):
        # 'folder_path' has to be a safe folder. Files or folders that do not exist throw errors.
        #   This loops throw each file and subdirectory in the 'folder_path'.

        for item in os.scandir(folder_path):
            if os.path.isfile(item.path):
                latest_folder_update = max(self._last_tracked_update, self._isNewerFileUpdate(item.path))
            else:
                self._isNewerFolderUpdate(item.path, latest_folder_update)    # Recursively call this method again for folders
        
        return latest_folder_update

    def _scan_and_update(self, file_or_folder_path):
        original_tracked_update = self._last_tracked_update
        original_filecount = self._last_tracked_filecount
        latest_update = 0

        if not os.path.exists(str(file_or_folder_path)):
            message.file_or_folder_does_not_exist(file_or_folder_path)
            self.secure()
            return

        if os.path.isfile(file_or_folder_path):
            latest_update = self._isNewerFileUpdate(file_or_folder_path)
        else:
            latest_update = max(latest_update, self._isNewerFolderUpdate(file_or_folder_path, latest_update))
        
        self._update_filecount()

        if original_tracked_update < self._last_tracked_update:
            self.run_scripts()
            return
    
        if original_filecount > self._last_tracked_filecount:
            message.found_deleted_files(original_filecount - self._last_tracked_filecount)
            self.run_scripts()
            return

    def _poll(self):
        
        self._scan_and_update(self.directory)
        self._poll_timer = threading.Timer(self.polling_delay, self._poll)
        if self._last_tracked_update > 0:   # Break out of infinite loop if the poll request was cancelled
            self._poll_timer.start()
    
    def watch(self) -> None:
        """Begin watching the specified directory for changes. Will secure if the directory is invalid."""
        if not os.path.exists(str(self.directory)):
            message.invalid_directory(self._directory)
            self.secure()
            return
        
        if self.active:
            # Without this guard clause, we could cause additional timers to start and take system resources
            message.monitoring_active()
            return
        
        # Hasn't been run yet. Initialize and commence monitoring
        self._poll()
        if monitor.active:
            message.watch() # Let the user know that there wasn't another error along the way that disabled the monitor
    
    def secure(self) -> None:
        self._poll_timer.cancel()
        self._last_tracked_update = 0
        message.secure()
        

monitor = DirectoryMonitor()
