""" Output messages to the console for DirectoryMonitor.

This module provides defines all the console output messages for the DirectoryMonitor class.
This makes the code in src/directory_monitor.py easier to read and maintain. 
"""

from .color_control import color

class DirectoryMonitorMessages:
    """Consolidates and prints formatted console messages for the DirectoryMonitor class."""

    @staticmethod
    def _ErrorHeader():
        return str(color.FAIL + "DirectoryMonitor error: " + color.ENDC)

    def watch():
        print(color.CONTROL + "Watching for updates..." + color.ENDC)
    
    def secure():
        print(color.CONTROL + "Monitoring is secured." + color.ENDC)
    
    def monitoring_active():
        print(color.CONTROL + "Monitoring is already active." + color.ENDC + " Continuing to monitor...")
    
    def invalid_directory(directory):
        print(DirectoryMonitorMessages._ErrorHeader() + "'DirectoryMonitor.directory' is invalid. Unable to monitor until "
            + "provided a valid file or folder path.\n"
            + "    Current bad DirectoryMonitor.directory: " + color.WARNING + str(directory) + color.ENDC)
    
    def file_or_folder_does_not_exist(dir_path):
        print(DirectoryMonitorMessages._ErrorHeader() + "The file or folder '" + color.WARNING +  dir_path + color.ENDC 
            + "' does not exist.")
    
    def found_deleted_files(num_files):
        del_msg = 'DirectoryMonitor found ' + color.OKGREEN + str(num_files) +color.ENDC
        if num_files > 1:
            del_msg += " deleted files."
        else:
            del_msg += " deleted file."
        print(del_msg)

    def found_updated_file(filepath):
        print("DirectoryMonitor found an updated file: " + color.OKGREEN +  filepath + color.ENDC)
    
    def unable_to_unsubscribe(script):
        print(DirectoryMonitorMessages._ErrorHeader() + "Unable to unsubscribe '" + color.WARNING + script + color.ENDC 
            + "'. This script was never registered.")
    
    def unable_to_change_directory(new_dir, current_dir):
        print(DirectoryMonitorMessages._ErrorHeader() + "'DirectoryMonitor.directory' must be a file or folder that exists.\n"
            + "    You tried: " + color.WARNING + str(new_dir) + color.ENDC + "\n"
            + "    Maintaining the current directory at: '" + color.OKGREEN + str(current_dir) + color.ENDC + "'")
    
    def invalid_polling_delay(delay):
        print(DirectoryMonitorMessages._ErrorHeader() + "'DirectoryMonitor.polling_delay' must be a number greater than 0.\n"
            + "    Maintaining poll interval at : " + color.OKGREEN + str(delay) + color.ENDC + " seconds.")