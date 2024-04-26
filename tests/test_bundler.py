import os
import unittest

from src.bundler import isValidBlenderAddonPath, bundle

test_source_files = [os.path.abspath(__file__)]
test_output_folder = os.path.dirname(__file__)
test_name = "TestBundle"
bundle_path = os.path.join(test_output_folder, test_name)  + '.zip'

def delete_test_bundle(path):
    if os.path.exists(path):
        os.remove(path)


class TestBundler(unittest.TestCase):

    ###############################################################
    # Validation Functions
    ###############################################################
    def test_existing_python_file_is_valid(self):
        """A single Python file that exists is valid."""
        
        testpath = os.path.abspath(__file__)
        self.assertTrue(isValidBlenderAddonPath(testpath))
        self.assertIsNotNone(isValidBlenderAddonPath(testpath))
        
    def test_init_files_reject(self):
        """Only .zip files can have an __init__.py file contained within. Standalone must be named something else."""
        testpath = os.path.join(os.path.dirname(__file__), "__init__.py")
        
        self.assertFalse(isValidBlenderAddonPath(testpath))
        self.assertIsNotNone(isValidBlenderAddonPath(testpath))
    
    def test_non_python_files_reject(self):
        """A single file add-on can only be a python file. Anything else should fail."""
        
        testpath = [os.path.join(os.path.dirname(__file__), "myAddon.python"),
            os.path.join(os.path.dirname(__file__), "myAddon.h"),
            os.path.join(os.path.dirname(__file__), "myAddon.js"),
            os.path.join(os.path.dirname(__file__), "myAddon.php"),
            os.path.join(os.path.dirname(__file__), "myAddon.txt"),
            2,
            3.14159,
            'ABC',
            False,
            True,
            {"path": os.path.dirname(__file__)}
        ]

        for path in testpath:
            self.assertFalse(isValidBlenderAddonPath(path))
            self.assertIsNotNone(isValidBlenderAddonPath(path))
    
    def test_existing_folders_reject(self):
        """Only .zip files can have an __init__.py file contained within. Standalone must be named something else."""
        testpath = os.path.dirname(__file__)
        
        self.assertFalse(isValidBlenderAddonPath(testpath))
        self.assertIsNotNone(isValidBlenderAddonPath(testpath))
        
    def test_nonexisting_folders_reject(self):
        """Only .zip files can have an __init__.py file contained within. Standalone must be named something else."""
        testpath = os.path.join(os.path.dirname(__file__), "\________________test_folder")
        
        self.assertFalse(isValidBlenderAddonPath(testpath))
        self.assertIsNotNone(isValidBlenderAddonPath(testpath))
    

    ###############################################################
    # Bundle Function - General Validation
    ###############################################################
    def test_omitting_required_params_throws_error(self):

        with self.assertRaises(TypeError):
            bundle()
        with self.assertRaises(TypeError):
            bundle(test_source_files)
        with self.assertRaises(TypeError):
            bundle(test_source_files, test_output_folder)
        with self.assertRaises(TypeError):
            bundle(name=test_name)


    ###############################################################
    # Bundle Function - Source Inputs Validation
    ###############################################################
    def test_empty_source_files_returns_none(self):
        self.assertIsNone(bundle([], test_output_folder, test_name))
    
    def test_non_string_source_files_returns_none(self):
        self.assertIsNone(bundle("Some String", test_output_folder, test_name))
        self.assertIsNone(bundle(12, test_output_folder, test_name))
        self.assertIsNone(bundle(7.33, test_output_folder, test_name))
        self.assertIsNone(bundle(True, test_output_folder, test_name))
        self.assertIsNone(bundle(False, test_output_folder, test_name))
        self.assertIsNone(bundle({"source_files": test_source_files}, test_output_folder, test_name))

    def test_single_invalid_source_file_returns_none(self):
        """Nonsense files that don't exist should not bundle into a .zip"""
        self.assertIsNone(bundle([os.path.abspath(__file__) + "abcd"], test_output_folder, test_name))
    
    def test_multiple_invalid_source_files_returns_none(self):
        """Multiple nonsense files that don't exist should not bundle into a .zip"""
        test_dir = os.path.dirname(os.path.abspath(__file__))
        files = [
            os.path.join(test_dir, "test_bundler.py123"),
            os.path.join(test_dir, "test_directory_monitor.py123")
        ]

        self.assertIsNone(bundle(files, test_output_folder, test_name))


    ###############################################################
    # Bundle Function - Output Directory Validation
    ###############################################################
    def test_valid_output_folder_bundles(self):
        self.assertEqual(bundle(test_source_files, test_output_folder, test_name), bundle_path)
        delete_test_bundle(bundle_path)
    
    def test_invalid_output_folder_returns_none(self):
        paths = [
            "Random String",
            2,
            3.14159,
            'ABC',
            False,
            True,
            {"path": os.path.dirname(__file__)},
            [os.path.dirname(__file__)]
        ]

        for output_folder in paths:
            self.assertIsNone(bundle(test_source_files, output_folder, test_name))
    
    def test_files_for_output_folder_return_none(self):
        self.assertIsNone(bundle(test_source_files, test_source_files, test_name)) # List of existing files
        self.assertIsNone(bundle(test_source_files, test_source_files[0], test_name)) # Existing file
    
    
    ###############################################################
    # Bundle Function - Name Validation
    ###############################################################
    def test_valid_file_name_strings_bundle(self):
        """Strings (or other values coercible to strings) should all work as long as they are valid file names for 
            the operating system."""
        names = [
            "Random String",
            "my_Package_Filename",
            "Package added zip anyway.zip",
            2,
            3.14159,
            'ABC',
            False,
            True
        ]

        for name in names:
            bundle_path = os.path.join(test_output_folder, str(name)) + ".zip"
            self.assertEqual(bundle(test_source_files, test_output_folder, name), bundle_path)
            delete_test_bundle(bundle_path)
    
    def test_names_longer_than_120_characters_return_none(self):
        """Prevent causing file system errors by names that are too long (i.e. >120 characters)."""
        long_name = ""
        for i in range(0, 120):
            long_name += "a"

        bundle_path = os.path.join(test_output_folder, str(long_name)) + ".zip"
        print(bundle_path)  
        bundle(test_source_files, test_output_folder, long_name)
        self.assertEqual(bundle(test_source_files, test_output_folder, long_name), bundle_path)
        delete_test_bundle(bundle_path)

        long_name += "a"    # Now 121 characters long and should fail
        bundle_path = os.path.join(test_output_folder, str(long_name)) + ".zip"
        self.assertIsNone(bundle(test_source_files, test_output_folder, long_name), bundle_path)
        delete_test_bundle(bundle_path)
    
    def test_names_with_invalid_os_characters_return_none(self):
        pass
        # COME BACK AND ADD THIS TEST ONCE I FIGURE OUT THE BAD CHARACTERS


    ###############################################################
    # Operational Tests - Zip Archive Creation
    ###############################################################
    # These tests essentially check to see if the bundled output exists as expected after calling bundle(...)

    def test_single_valid_source_file_bundles(self):
        self.assertEqual(bundle(test_source_files, test_output_folder, test_name), bundle_path)
        self.assertTrue(os.path.exists(bundle_path))
        delete_test_bundle(bundle_path)
    
    def test_single_valid_source_folder_bundles(self):
        test_folder = os.path.dirname(os.path.abspath(__file__))
        self.assertEqual(bundle([test_folder], test_output_folder, test_name), bundle_path)
        delete_test_bundle(bundle_path)
    
    def test_multiple_valid_source_files_bundle(self):
        test_dir = os.path.dirname(os.path.abspath(__file__))
        files = [
            os.path.join(test_dir, "test_bundler.py"),
            os.path.join(test_dir, "test_directory_monitor.py")
        ]

        self.assertEqual(bundle(files, test_output_folder, test_name), bundle_path)
        delete_test_bundle(bundle_path)
    
    def test_multiple_valid_source_folders_bundle(self):
        test_dir = os.path.dirname(os.path.abspath(__file__))
        src_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
        files = [test_dir, src_dir]

        self.assertEqual(bundle(files, test_output_folder, test_name), bundle_path)
        delete_test_bundle(bundle_path)
    
    def test_multiple_valid_source_files_with_folders_bundle(self):
        test_dir = os.path.dirname(os.path.abspath(__file__))
        src_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
        files = [
            test_dir, 
            os.path.join(test_dir, "test_bundler.py"),
            src_dir,
            os.path.join(test_dir, "test_directory_monitor.py")
        ]

        self.assertEqual(bundle(files, test_output_folder, test_name), bundle_path)
        delete_test_bundle(bundle_path)
        
    def test_forcing_overwrite_successfully_copies_zip_default_true(self):
        delete_test_bundle(bundle_path) # It shouldn't, but guarantee the bundle doesn't exist at the start of this test
        self.assertEqual(bundle(test_source_files, test_output_folder, test_name), bundle_path)
        creation_time = os.path.getmtime(bundle_path)

        # Now that a file exists, make a new one with the same name and different files
        test_dir = os.path.dirname(os.path.abspath(__file__))
        src_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
        files = [test_dir, src_dir]
        self.assertEqual(bundle(files, test_output_folder, test_name), bundle_path)
        new_create_time = os.path.getmtime(bundle_path)

        # This new one should have overwritten, and this the new create time should be more than the old create time
        self.assertGreater(new_create_time, creation_time)

        delete_test_bundle(bundle_path)
    
    def test_forcing_overwrite_successfully_copies_zip_explicitly_true(self):
        delete_test_bundle(bundle_path) # It shouldn't, but guarantee the bundle doesn't exist at the start of this test
        self.assertEqual(bundle(test_source_files, test_output_folder, test_name, overwrite=True), bundle_path)
        creation_time = os.path.getmtime(bundle_path)

        # Now that a file exists, make a new one with the same name and different files
        test_dir = os.path.dirname(os.path.abspath(__file__))
        src_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
        files = [test_dir, src_dir]
        self.assertEqual(bundle(files, test_output_folder, test_name), bundle_path)
        new_create_time = os.path.getmtime(bundle_path)

        # This new one should have overwritten, and this the new create time should be more than the old create time
        self.assertGreater(new_create_time, creation_time)

        delete_test_bundle(bundle_path)

    def test_not_forcing_overwrite_prevents_copying_zip(self):
        delete_test_bundle(bundle_path) # It shouldn't, but guarantee the bundle doesn't exist at the start of this test
        self.assertEqual(bundle(test_source_files, test_output_folder, test_name, overwrite=True), bundle_path)
        creation_time = os.path.getmtime(bundle_path)

        # Now that a file exists, make a new one with the same name and different files
        test_dir = os.path.dirname(os.path.abspath(__file__))
        src_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
        files = [test_dir, src_dir]
        myvar = bundle(files, test_output_folder, test_name, overwrite=False)
        new_create_time = os.path.getmtime(bundle_path)

        # This new one should have overwritten, and this the new modify time should be the same as the old modify time.
        #   Using modify instead of create time because the ctime of the .zip is when it was created, and it was moved
        #   to the output folder a fraction of a second later which is a new modified time.
        self.assertEqual(new_create_time, creation_time)

        delete_test_bundle(bundle_path)

        #####################################
        # TODO: Write tests for the no_pycache option 
    
    def test_bundle_with_no_pycache_has_no_python_binaries_in_zip(self):
        pass
        # Create a temp folder
        # Create two empty python files
        # Create a __pycache__ folder with two .pyc files, and a resources folder with two files
        # Bundle this temp folder into a zip
        # Check zip to make sure it has two folders (each with two files) and two main files

if __name__ == '__main__':
    unittest.main()
    
