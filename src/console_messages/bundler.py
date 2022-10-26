""" Output messages to the console for the bundling functions."""

from .color_control import color

def _Bundler_ErrorHeader():
    # I split this into a function outside of the class because otherwise in order to use
    #   the error messages in the main code required a reference to self by doing 
    #   something like this:
    #   
    #   message.bundle_message(message, input_args)
    return str(color.FAIL + "Bundler error: " + color.ENDC)


class BundlerMessages:
    """Consolidates and prints formatted console messages for the bundler functions."""

    def complete(output_location: str):
        print(color.CONTROL + "Bundling completed." + color.ENDC
        + " Bundled add-on located at: " + color.OKGREEN + output_location + color.ENDC)
    
    def invalid_source_not_a_list(source_input: str):
        print(_Bundler_ErrorHeader() + "Source file argument must be a list. Unable to process: " + color.WARNING
            + str(source_input) + color.ENDC + ".")

    def invalid_source_empty_list():
        print(_Bundler_ErrorHeader() + "Source files cannot be an empty list.")

    def file_does_not_exist(dir_path: str):
        print(_Bundler_ErrorHeader() + "The file or folder '" + color.WARNING +  str(dir_path) + color.ENDC 
            + "' does not exist.")
    
    def output_folder_does_not_exist(dir_path: str):
        print(_Bundler_ErrorHeader() + "The desired output folder '" + color.WARNING +  str(dir_path) + color.ENDC 
            + "' is either not a folder or does not exist.")
    
    def output_file_name_too_long():
        print(_Bundler_ErrorHeader() + "The output file name must be 189 characters or less.")
    
    def bundle_already_exists(bundle_path: str):
        print(_Bundler_ErrorHeader() + "The desired bundle path '" + color.WARNING +  str(bundle_path) + color.ENDC 
            + "' already exists. The bundler will not overwrite this file unless the `overwrite` value is True.")
