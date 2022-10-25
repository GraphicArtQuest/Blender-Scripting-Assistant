""" Output messages to the console for DirectoryMonitor.

This module provides defines all the console output messages for the DirectoryMonitor class.
This makes the code in src/directory_monitor.py easier to read and maintain. 
"""

from src.console_messages.color_control import color

def _DirectoryMonitor_ErrorHeader():
    # I split this into a function outside of the class because otherwise in order to use
    #   the error messages in the main code required a reference to self by doing 
    #   something like this:
    #   
    #   message.file_or_folder_does_not_exist(message, file_or_folder_path)
    return str(color.FAIL + "DirectoryMonitor error: " + color.ENDC)


class DirectoryMonitorMessages:
    """Consolidates and prints formatted console messages for the DirectoryMonitor class."""

    def watch():
        print(color.CONTROL + "Watching for updates..." + color.ENDC)
    
    def secure():
        print(color.CONTROL + "Monitoring is secured." + color.ENDC)
    
    def monitoring_active():
        print(color.CONTROL + "Monitoring is already active." + color.ENDC + " Continuing to monitor...")
    
    def invalid_directory(directory):
        print(_DirectoryMonitor_ErrorHeader() + "'DirectoryMonitor.directory' is invalid. Unable to monitor until "
            + "provided a valid file or folder path.\n"
            + "    Current bad DirectoryMonitor.directory: " + color.WARNING + str(directory) + color.ENDC)
    
    def file_or_folder_does_not_exist(dir_path):
        print(_DirectoryMonitor_ErrorHeader() + "The file or folder '" + color.WARNING +  dir_path + color.ENDC 
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
        print(_DirectoryMonitor_ErrorHeader() + "Unable to unsubscribe '" + color.WARNING + script + color.ENDC 
            + "'. This script was never registered.")
    
    def unable_to_change_directory(new_dir, current_dir):
        print(_DirectoryMonitor_ErrorHeader() + "'DirectoryMonitor.directory' must be a file or folder that exists.\n"
            + "    You tried: " + color.WARNING + str(new_dir) + color.ENDC + "\n"
            + "    Maintaining the current directory at: '" + color.OKGREEN + str(current_dir) + color.ENDC + "'")
    
    def invalid_polling_delay(delay):
        print(_DirectoryMonitor_ErrorHeader() + "'DirectoryMonitor.polling_delay' must be a number greater than 0.\n"
            + "    Maintaining poll interval at : " + color.OKGREEN + str(delay) + color.ENDC + " seconds.")