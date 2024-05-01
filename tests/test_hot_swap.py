"""
    NOTE: Within this test module, you have to use a different file or folder name for every test. If you reuse names,
    you will frequently find breaking tests. The `unittest` package runs them in parallel, so you can get race
    conditions when deleting/writing files. Using a different name each time prevents that.
"""
import os
import shutil
import unittest

from src.hot_swap import create_addon_name, get_most_recent_bl_name_info

unittest.TestLoader.sortTestMethodsUsing = None

good_folder_path = os.path.dirname(os.path.dirname(__file__))
testfile_path = os.path.join(good_folder_path, "tests\\")

def delete_test_file(path):
    if os.path.exists(path):
        os.remove(path)

class TestHotSwap_create_addon_name(unittest.TestCase):

    ###############################################################
    # Valid Blender Add-ons - Single Files
    ###############################################################
    def test_valid_single_file_returns_addon_name_with_spaces(self):
        """The given name string should return the correct same value in lower case and with spaces replaced by
            dashes. Trailing and leading spaces should get cut off.
        """
        
        self.assertEqual(create_addon_name('testfilealllowercase'), 'testfilealllowercase')
        self.assertEqual(create_addon_name('TestModuleNameNoSpaces'), 'testmodulenamenospaces')
        self.assertEqual(create_addon_name('Test File With Spaces'), 'test-file-with-spaces')
        self.assertEqual(create_addon_name('test-module-name-with-dashes'), 'test-module-name-with-dashes')
        self.assertEqual(create_addon_name('test_module_name_with_underscores'), 'test_module_name_with_underscores')
        self.assertEqual(create_addon_name(
            'test-module-name-with-trailing-space     '), 
            'test-module-name-with-trailing-space')
        self.assertEqual(create_addon_name(
            '     test-module-name-with-leading-space'), 
            'test-module-name-with-leading-space')
        self.assertEqual(create_addon_name(
            'Test module with       MIDDLE extra spaces'), 
            'test-module-with-------middle-extra-spaces')
        self.assertEqual(create_addon_name(''), '')
        self.assertEqual(create_addon_name('    '), '')

class TestHotSwap_get_most_recent_bl_name_info(unittest.TestCase):

    ###############################################################
    # Valid Blender Add-ons - Single Files
    ###############################################################
    def test_valid_single_file_returns_bl_name(self):
        """A single Python file add-on with a `bl_info` object returns the given name."""
        
        filepath = os.path.join(testfile_path, "valid_single_bl_info_file.py")
        # Delete if already exists, and create the test file
        delete_test_file(filepath)
        testfile = open(filepath, "w")
        testfile.write("bl_info = {\n")
        testfile.write("    'name': 'Test File Name'\n")
        testfile.write("}")
        testfile.close()

        # Get name and run test
        name = get_most_recent_bl_name_info(filepath)
        self.assertEqual(name, 'Test File Name')

        # Cleanup
        delete_test_file(filepath)
        
    ###############################################################
    # Valid Blender Add-ons - Modules
    ###############################################################
    def test_valid_folder_returns_bl_name(self):
        """A folder containing a Python module with a `bl_info` object returns the given name."""
        
        modulepath = os.path.join(testfile_path, "valid_module_bl_info_file")
        # Delete if already exists, and create the test module path
        shutil.rmtree(modulepath, ignore_errors=True)
        os.mkdir(modulepath)

        # Create the __init__.py file
        module_init_file = os.path.join(modulepath, "__init__.py")
        testfile = open(module_init_file, "w")
        testfile.write("bl_info = {\n")
        testfile.write("    'name': 'Test Module Name'\n")
        testfile.write("}")
        testfile.close()

        # Get name and run test
        name = get_most_recent_bl_name_info(modulepath)
        self.assertEqual(name, 'Test Module Name')

        # Cleanup
        shutil.rmtree(modulepath, ignore_errors=True)

    ###############################################################
    # Invalid Blender Add-ons - Single Files
    ###############################################################
    def test_invalid_single_file_returns_empty_string_when_no_bl_info_on_refresh(self):
        """A single Python file MUST have the `bl_info` object to be a valid Blender add-on. If not there, reject it."""
        
        filepath = os.path.join(testfile_path, "invalid_single_file_missing_bl_info_on_refresh.py")
        # Delete if already exists, and create the test file
        delete_test_file(filepath)
        testfile = open(filepath, "w")
        # NO DATA WRITTEN
        testfile.close()

        # Get name and run test
        name = get_most_recent_bl_name_info(filepath)
        self.assertEqual(name, '')

        # Cleanup
        delete_test_file(filepath)

    def test_invalid_single_file_returns_empty_string_when_bl_info_missing_name_on_refresh(self):
        """If the `bl_info` object is there but missing a name field, reject it."""
        
        filepath = os.path.join(testfile_path, "invalid_single_file_missing_bl_info_name_on_refresh.py")
        # Delete if already exists, and create the test file
        delete_test_file(filepath)
        testfile = open(filepath, "w")
        testfile.write("bl_info = {\n")
        # testfile.write("    'name': 'TestFile'\n")    # Intentionally excluded
        testfile.write("}")
        testfile.close()

        # Get name and run test
        name = get_most_recent_bl_name_info(filepath)
        self.assertEqual(name, '')

        # Cleanup
        delete_test_file(filepath)

    def test_invalid_single_file_returns_empty_string_when_file_does_not_exist_on_refresh(self):
        """If a file doesn't exist, return an empty string."""
        
        filepath = os.path.join(testfile_path, "filepath_that_doesn't_exist_for_refresh")
        delete_test_file(filepath)
        # No file actually created

        # Get name and run test
        name = get_most_recent_bl_name_info(filepath)
        self.assertEqual(name, '')

    ###############################################################
    # Invalid Blender Add-ons - Modules
    ###############################################################
    def test_invalid_folder_returns_empty_string_when_no_init_file_on_refresh(self):
        """A package containing a Python module with no or improper init file returns correct name."""
        
        modulepath = os.path.join(testfile_path, "invalid_module_with_no_init_on_refresh")
        # Delete if already exists, and create the test module path
        shutil.rmtree(modulepath, ignore_errors=True)
        os.mkdir(modulepath)

        # Create the __init__.py file
        module_init_file = os.path.join(modulepath, "__init2__.py") # Intentional typo to prevent importing as module
        testfile = open(module_init_file, "w")
        testfile.write("bl_info = {\n")
        testfile.write("    'name': 'Invalid No Init'\n")
        testfile.write("}")
        testfile.close()

        # Get name and run test
        name = get_most_recent_bl_name_info(modulepath)
        self.assertEqual(name, '')

        # Cleanup
        shutil.rmtree(modulepath, ignore_errors=True)

    def test_invalid_folder_returns_empty_string_when_no_bl_info_on_refresh(self):
        """A folder containing a Python module MUST have the `bl_info` object to be a valid Blender add-on.
        If not there, reject it.."""
        
        modulepath = os.path.join(testfile_path, "invalid_module_with_no_bl_info_on_refresh")
        # Delete if already exists, and create the test module path
        shutil.rmtree(modulepath, ignore_errors=True)
        os.mkdir(modulepath)

        # Create the __init__.py file
        module_init_file = os.path.join(modulepath, "__init__.py")
        testfile = open(module_init_file, "w")
        # NO DATA WRITTEN
        testfile.close()

        # Get name and run test
        name = get_most_recent_bl_name_info(modulepath)
        self.assertEqual(name, '')

        # Cleanup
        shutil.rmtree(modulepath, ignore_errors=True)

    def test_invalid_folder_returns_empty_string_when_bl_info_missing_name_on_refresh(self):
        """A folder containing a Python module MUST have the `bl_info` object with a name field.
        If not there, reject it.."""
        
        modulepath = os.path.join(testfile_path, "invalid_module_with_bl_info_missing_name_on_refresh")
        # Delete if already exists, and create the test module path
        shutil.rmtree(modulepath, ignore_errors=True)
        os.mkdir(modulepath)

        # Create the __init__.py file
        module_init_file = os.path.join(modulepath, "__init__.py")
        testfile = open(module_init_file, "w")
        testfile.write("bl_info = {\n")
        # testfile.write("    'name': '    '\n")  # Intentionally omitted
        testfile.write("}")
        testfile.close()

        # Get name and run test
        name = get_most_recent_bl_name_info(modulepath)
        self.assertEqual(name, '')

        # Cleanup
        shutil.rmtree(modulepath, ignore_errors=True)
        
    def test_invalid_folder_returns_empty_string_when_folder_does_not_exist_on_refresh(self):
        """If a file doesn't exist, return an empty string."""
        
        modulepath = os.path.join(testfile_path, "module_that_doesn't_exist_for_refresh")
        shutil.rmtree(modulepath, ignore_errors=True)
        # No module actually created

        # Get name and run test
        name = get_most_recent_bl_name_info(modulepath)
        self.assertEqual(name, '')

if __name__ == '__main__':
    unittest.main()
