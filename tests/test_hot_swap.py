"""
    NOTE: Within this test module, you have to use a different file or folder name for every test. If you reuse names,
    you will frequently find breaking tests. The `unittest` package runs them in parallel, so you can get race
    conditions when deleting/writing files. Using a different name each time prevents that.
"""
import os
import shutil
import unittest

from src.hot_swap import create_addon_name

unittest.TestLoader.sortTestMethodsUsing = None

good_folder_path = os.path.dirname(os.path.dirname(__file__))
testfile_path = os.path.join(good_folder_path, "tests\\")

def delete_test_file(path):
    if os.path.exists(path):
        os.remove(path)

class TestHotSwap(unittest.TestCase):

    ###############################################################
    # Valid Blender Add-ons - Single Files
    ###############################################################
    def test_valid_single_file_returns_addon_name_no_spaces(self):
        """A single Python file with no spaces in the name and a `bl_info` object returns the correct name."""
        
        filepath = os.path.join(testfile_path, "valid_single_file.py")
        # Delete if already exists, and create the test file
        delete_test_file(filepath)
        testfile = open(filepath, "w")
        testfile.write("bl_info = {\n")
        testfile.write("    'name': 'TestFile'\n")
        testfile.write("}")
        testfile.close()

        # Get name and run test
        name = create_addon_name(filepath)
        self.assertEqual(name, 'testfile')

        # Cleanup
        delete_test_file(filepath)
        
    def test_valid_single_file_returns_addon_name_with_spaces(self):
        """A single Python file with spaces in the name and a `bl_info` object returns the correct name with dashes."""
        
        filepath = os.path.join(testfile_path, "valid_single_file_with_spaces.py")
        # Delete if already exists, and create the test file
        delete_test_file(filepath)
        testfile = open(filepath, "w")
        testfile.write("bl_info = {\n")
        testfile.write("    'name': 'Test File With Spaces'\n")
        testfile.write("}")
        testfile.close()

        # Get name and run test
        name = create_addon_name(filepath)
        self.assertEqual(name, 'test-file-with-spaces')

        # Cleanup
        delete_test_file(filepath)

    ###############################################################
    # Valid Blender Add-ons - Modules
    ###############################################################
    def test_valid_folder_returns_addon_name_no_spaces(self):
        """A folder containing a Python module with no spaces in the `bl_info.name` object returns correct name."""
        
        modulepath = os.path.join(testfile_path, "valid_module_no_spaces")
        # Delete if already exists, and create the test module path
        shutil.rmtree(modulepath, ignore_errors=True)
        os.mkdir(modulepath)

        # Create the __init__.py file
        module_init_file = os.path.join(modulepath, "__init__.py")
        testfile = open(module_init_file, "w")
        testfile.write("bl_info = {\n")
        testfile.write("    'name': 'TestModuleNameNoSpaces'\n")
        testfile.write("}")
        testfile.close()

        # Get name and run test
        name = create_addon_name(modulepath)
        self.assertEqual(name, 'testmodulenamenospaces')

        # Cleanup
        shutil.rmtree(modulepath, ignore_errors=True)

    def test_valid_folder_returns_addon_name_with_spaces(self):
        """A folder containing a Python module with spaces in the `bl_info.name` object returns correct name."""
        
        modulepath = os.path.join(testfile_path, "valid_module_with_spaces")
        # Delete if already exists, and create the test module path
        shutil.rmtree(modulepath, ignore_errors=True)
        os.mkdir(modulepath)

        # Create the __init__.py file
        module_init_file = os.path.join(modulepath, "__init__.py")
        testfile = open(module_init_file, "w")
        testfile.write("bl_info = {\n")
        testfile.write("    'name': 'Test Module Name With Spaces'\n")
        testfile.write("}")
        testfile.close()

        # Get name and run test
        name = create_addon_name(modulepath)
        self.assertEqual(name, 'test-module-name-with-spaces')

        # Cleanup
        shutil.rmtree(modulepath, ignore_errors=True)

    ###############################################################
    # Invalid Blender Add-ons - Single Files
    ###############################################################
    def test_invalid_single_file_returns_empty_string_when_no_bl_info(self):
        """A single Python file MUST have the `bl_info` object to be a valid Blender add-on. If not there, reject it."""
        
        filepath = os.path.join(testfile_path, "invalid_single_file_missing_bl_info.py")
        # Delete if already exists, and create the test file
        delete_test_file(filepath)
        testfile = open(filepath, "w")
        # NO DATA WRITTEN
        testfile.close()

        # Get name and run test
        name = create_addon_name(filepath)
        self.assertEqual(name, '')

        # Cleanup
        delete_test_file(filepath)

    def test_invalid_single_file_returns_empty_string_when_bl_info_missing_name(self):
        """If the `bl_info` object is there but missing a name field, reject it."""
        
        filepath = os.path.join(testfile_path, "invalid_single_file_missing_bl_info_name.py")
        # Delete if already exists, and create the test file
        delete_test_file(filepath)
        testfile = open(filepath, "w")
        testfile.write("bl_info = {\n")
        # testfile.write("    'name': 'TestFile'\n")    # Intentionally excluded
        testfile.write("}")
        testfile.close()

        # Get name and run test
        name = create_addon_name(filepath)
        self.assertEqual(name, '')

        # Cleanup
        delete_test_file(filepath)

    def test_invalid_single_file_returns_empty_string_when_bl_info_name_empty(self):
        """If the `bl_info` object but the name field is empty, reject it."""
        
        filepath = os.path.join(testfile_path, "invalid_single_file_missing_bl_info_name_empty.py")
        # Delete if already exists, and create the test file
        delete_test_file(filepath)
        testfile = open(filepath, "w")
        testfile.write("bl_info = {\n")
        testfile.write("    'name': ''\n")  # Intentionally included, but left blank
        testfile.write("}")
        testfile.close()

        # Get name and run test
        name = create_addon_name(filepath)
        self.assertEqual(name, '')

        # Cleanup
        delete_test_file(filepath)


    def test_invalid_single_file_returns_empty_string_when_bl_info_name_only_spaces(self):
        """If the `bl_info` object but the name field is only spaces, reject it."""
        
        filepath = os.path.join(testfile_path, "invalid_single_file_missing_bl_info_name_only_spaces.py")
        # Delete if already exists, and create the test file
        delete_test_file(filepath)
        testfile = open(filepath, "w")
        testfile.write("bl_info = {\n")
        testfile.write("    'name': '    '\n")  # A bunch of spaces with no actual characters
        testfile.write("}")
        testfile.close()

        # Get name and run test
        name = create_addon_name(filepath)
        self.assertEqual(name, '')

        # Cleanup
        delete_test_file(filepath)
        
    ###############################################################
    # Invalid Blender Add-ons - Modules
    ###############################################################
    def test_invalid_folder_returns_empty_string_when_no_init_file(self):
        """A folder containing a Python module with spaces in the `bl_info.name` object returns correct name."""
        
        modulepath = os.path.join(testfile_path, "invalid_module_with_no_init")
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
        name = create_addon_name(modulepath)
        self.assertEqual(name, '')

        # Cleanup
        shutil.rmtree(modulepath, ignore_errors=True)

    def test_invalid_folder_returns_empty_string_when_no_bl_info(self):
        """A folder containing a Python module MUST have the `bl_info` object to be a valid Blender add-on.
        If not there, reject it.."""
        
        modulepath = os.path.join(testfile_path, "invalid_module_with_no_bl_info")
        # Delete if already exists, and create the test module path
        shutil.rmtree(modulepath, ignore_errors=True)
        os.mkdir(modulepath)

        # Create the __init__.py file
        module_init_file = os.path.join(modulepath, "__init__.py")
        testfile = open(module_init_file, "w")
        # NO DATA WRITTEN
        testfile.close()

        # Get name and run test
        name = create_addon_name(modulepath)
        self.assertEqual(name, '')

        # Cleanup
        shutil.rmtree(modulepath, ignore_errors=True)

    def test_invalid_folder_returns_empty_string_when_bl_info_missing_name(self):
        """A folder containing a Python module MUST have the `bl_info` object with a name field.
        If not there, reject it.."""
        
        modulepath = os.path.join(testfile_path, "invalid_module_with_bl_info_missing_name")
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
        name = create_addon_name(modulepath)
        self.assertEqual(name, '')

        # Cleanup
        shutil.rmtree(modulepath, ignore_errors=True)

    def test_invalid_folder_returns_empty_string_when_bl_info_name_empty(self):
        """A folder containing a Python module MUST have the `bl_info` object with a name field.
        If it is there but blank, reject it.."""
        
        modulepath = os.path.join(testfile_path, "invalid_module_with_bl_info_name_empty")
        # Delete if already exists, and create the test module path
        shutil.rmtree(modulepath, ignore_errors=True)
        os.mkdir(modulepath)

        # Create the __init__.py file
        module_init_file = os.path.join(modulepath, "__init__.py")
        testfile = open(module_init_file, "w")
        testfile.write("bl_info = {\n")
        testfile.write("    'name': ''\n")  # Intentionally included, but left blank
        testfile.write("}")
        testfile.close()

        # Get name and run test
        name = create_addon_name(modulepath)
        self.assertEqual(name, '')

        # Cleanup
        shutil.rmtree(modulepath, ignore_errors=True)

    def test_invalid_folder_returns_empty_string_when_bl_info_name_only_spaces(self):
        """A folder containing a Python module MUST have the `bl_info` object with a name field.
        If it is only spaces, reject it.."""
        
        modulepath = os.path.join(testfile_path, "invalid_module_with_bl_info_name_only_spaces")
        # Delete if already exists, and create the test module path
        shutil.rmtree(modulepath, ignore_errors=True)
        os.mkdir(modulepath)

        # Create the __init__.py file
        module_init_file = os.path.join(modulepath, "__init__.py")
        testfile = open(module_init_file, "w")
        testfile.write("bl_info = {\n")
        testfile.write("    'name': '    '\n")  # Intentionally included, but left blank
        testfile.write("}")
        testfile.close()

        # Get name and run test
        name = create_addon_name(modulepath)
        self.assertEqual(name, '')

        # Cleanup
        shutil.rmtree(modulepath, ignore_errors=True)

if __name__ == '__main__':
    unittest.main()
    
