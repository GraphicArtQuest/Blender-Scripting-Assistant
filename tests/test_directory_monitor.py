import os
import time
import unittest

from src.directory_monitor import monitor, DirectoryMonitor

# Verify good file and folder works (The test file and folder have to exist)
good_file_path = os.path.abspath(__file__)
good_folder_path = os.path.dirname(os.path.dirname(__file__))

bad_file_path = os.path.abspath(__file__) + 'abcd'      # Nonsense file
bad_folder_path = os.path.dirname(__file__) + 'abcd'    # Nonsense path

# These filenames and paths should be obscure enough to not exist outside this test suite
testfile_name = "_____testfile.txt"
testfile_path = os.path.join(good_folder_path, "tests\\", testfile_name)
testfile2_name = "_____testfile2.txt"
testfile2_path = os.path.join(good_folder_path, "src\\", testfile2_name)
    
def create_test_files():
    testfile = open(testfile_path, "w")
    testfile.write("Test text. ")
    testfile.close()

    testfile2 = open(testfile2_path, "w")
    testfile2.write("Test text. ")
    testfile2.close()

def modify_test_file1():
    testfile = open(testfile_path, "a")
    testfile.write("Additional Test Text. ")
    testfile.close()

def modify_test_file2():
    testfile2 = open(testfile2_path, "a")
    testfile2.write("Additional Test Text. ")
    testfile2.close()

def delete_test_files():
    if os.path.exists(testfile_path):
        os.remove(testfile_path)
    
    if os.path.exists(testfile2_path):
        os.remove(testfile2_path)

class TestDirectoryMonitor(unittest.TestCase):
    def setUp(self):
        monitor._directory = ""
        monitor._polling_delay = .15

    ###############################################################
    # Verify Default Properties
    ###############################################################
    def test_default_polling_delay(self):
        self.assertEqual(monitor.polling_delay, .15)

    def test_default_active(self):
        self.assertFalse(monitor.active)
    
    def test_default_directory(self):
        self.assertEqual(monitor.directory, "")

    ###############################################################
    # Verify Property Setting/Getting Methods
    ###############################################################
    def test_prop_update_polling_delay(self):
        # Polling delays must be numerical and greater than 0.
        monitor.polling_delay = 2
        self.assertEqual(monitor.polling_delay, 2)
        monitor.polling_delay = .25
        self.assertEqual(monitor.polling_delay, .25)
        monitor.polling_delay = '.25'
        self.assertEqual(monitor.polling_delay, .25)
        monitor.polling_delay = 0
        self.assertEqual(monitor.polling_delay, .25)
        monitor.polling_delay = -1
        self.assertEqual(monitor.polling_delay, .25)
        monitor.polling_delay = False
        self.assertEqual(monitor.polling_delay, .25)
        monitor.polling_delay = True
        self.assertEqual(monitor.polling_delay, 1)
        monitor.polling_delay = .15 # Reset to default
        
    def test_prop_update_active_fails(self):
        # Verify monitor.active is read only
        try:
            monitor.active = True
        except:
            self.assertFalse(monitor.active)
        
        try:
            monitor.active = False
        except:
            self.assertFalse(monitor.active)
    
    def test_prop_update_directory(self):
        

        monitor.directory = good_file_path
        self.assertEqual(monitor.directory, good_file_path)
        
        monitor.directory = good_folder_path
        self.assertEqual(monitor.directory, good_folder_path)
        
        # Changing to bad paths should do nothing to the directory
        monitor.directory = bad_file_path
        self.assertEqual(monitor.directory, good_folder_path)
        
        monitor.directory = bad_folder_path
        self.assertEqual(monitor.directory, good_folder_path)

        monitor.directory = ""
        self.assertEqual(monitor.directory, good_folder_path)

        monitor.directory = 123456
        self.assertEqual(monitor.directory, good_folder_path)


    ###############################################################
    # Subscribe and Unsubscribe
    ###############################################################
    
    def test_subscribe(self):

        def test1():
            pass
            
        def test2():
            pass
            
        def test3():
            pass

        monitor.clear_subscribers()
        
        self.assertFalse('test1' in monitor._subscribers)
        self.assertFalse('test2' in monitor._subscribers)
        self.assertFalse('test3' in monitor._subscribers)

        monitor.subscribe('test1', test1)
        monitor.subscribe('test2', test2)
        monitor.subscribe('test3', test3)

        self.assertTrue('test1' in monitor._subscribers)
        self.assertTrue('test2' in monitor._subscribers)
        self.assertTrue('test3' in monitor._subscribers)
        self.assertFalse('test4' in monitor._subscribers)

        monitor.clear_subscribers()

    def test_unsubscribe_key_exists(self):
        def test():
            pass
        
        monitor.clear_subscribers()
        monitor.subscribe('test', test)

        self.assertTrue('test' in monitor._subscribers)
        self.assertEqual(len(monitor._subscribers), 1)

        monitor.unsubscribe('test')
        self.assertEqual(len(monitor._subscribers), 0)

        monitor.clear_subscribers()

    def test_unsubscribe_key_does_not_exist(self):
        def test():
            pass
        
        monitor.clear_subscribers()
        monitor.subscribe('test', test)

        self.assertTrue('test' in monitor._subscribers)
        self.assertEqual(len(monitor._subscribers), 1)

        monitor.unsubscribe('badtestname')
        self.assertEqual(len(monitor._subscribers), 1)

        monitor.clear_subscribers()

    def test_clear_subscribers(self):
        def test():
            pass
        
        monitor.clear_subscribers()
        self.assertEqual(len(monitor._subscribers), 0)
        monitor.subscribe('test', test)
        self.assertEqual(len(monitor._subscribers), 1)
        monitor.clear_subscribers()
        self.assertEqual(len(monitor._subscribers), 0)


    ###############################################################
    # Operationally Active
    ###############################################################
    
    def test_watch_and_secure(self):
        monitor.directory = good_folder_path
        self.assertFalse(monitor.active)
        monitor.watch()
        self.assertTrue(monitor.active)
        monitor.secure()
        self.assertFalse(monitor.active)

    
    def test_watch_when_directory_manually_changed_to_bad(self):
        # If someone manually changes monitor._directory to a bad value before watching, it should not run.
        self.assertFalse(monitor.active)
        monitor._directory = bad_file_path
        monitor.watch()
        self.assertFalse(monitor.active)
        monitor.secure()
        self.assertFalse(monitor.active)


    ###############################################################
    # Registering and Unregistering
    ###############################################################
    
    def test_watch_then_register_does_not_run(self):
        # Starting the monitor with .watch() will run any registered scripts
        #   as it initializes. Scripts registered before watching should run
        #   one time, scripts registered after should not.
        monitor.polling_delay = .1
        monitor.directory = good_folder_path

        testval = 1
        def test():
            nonlocal testval
            testval += 10

        monitor.clear_subscribers()
        monitor.watch()
        monitor.subscribe('test', test)
        monitor.secure()
        monitor.clear_subscribers()

        self.assertEqual(testval, 1)

    def test_register_then_watch_runs_one_time(self):
        # Starting the monitor with .watch() will run any registered scripts
        #   as it initializes. Scripts registered before watching should run
        #   one time, scripts registered after should not.
        monitor.directory = good_folder_path

        testval = 1
        def test():
            nonlocal testval
            testval += 10

        monitor.clear_subscribers()
        monitor.subscribe('test', test)
        monitor.watch()
        monitor.secure()
        monitor.clear_subscribers()

        self.assertEqual(testval, 11)

    def test_registering_same_scripts_run_uniquely(self):
        # Registering the same script three times will execute three times.
        monitor.directory = good_folder_path

        testval = 1
        def test():
            nonlocal testval
            testval += 10

        monitor.clear_subscribers()
        monitor.subscribe('test', test)
        monitor.subscribe('test', test)
        monitor.subscribe('test', test)
        monitor.watch()
        monitor.secure()
        monitor.clear_subscribers()

        self.assertEqual(testval, 31)

    def test_registering_different_scripts_run_uniquely_same_event(self):
        # Registering different scripts under the same event name will all run once.
        monitor.directory = good_folder_path

        testval1 = 1
        testval2 = 2
        testval3 = 3

        def test1():
            nonlocal testval1
            testval1 += 10
            
        def test2():
            nonlocal testval2
            testval2 += 10
            
        def test3():
            nonlocal testval3
            testval3 += 10

        monitor.clear_subscribers()
        monitor.subscribe('test', test1)
        monitor.subscribe('test', test2)
        monitor.subscribe('test', test3)
        monitor.watch()
        monitor.secure()
        monitor.clear_subscribers()

        self.assertEqual(testval1, 11)
        self.assertEqual(testval2, 12)
        self.assertEqual(testval3, 13)

    def test_registering_different_scripts_run_uniquely_different_event(self):
        # Registering different scripts under different event names will all run once.
        monitor.directory = good_folder_path

        testval1 = 1
        testval2 = 2
        testval3 = 3

        def test1():
            nonlocal testval1
            testval1 += 10
            
        def test2():
            nonlocal testval2
            testval2 += 10
            
        def test3():
            nonlocal testval3
            testval3 += 10

        monitor.clear_subscribers()
        monitor.subscribe('test1', test1)
        monitor.subscribe('test2', test2)
        monitor.subscribe('test3', test3)
        monitor.watch()
        monitor.secure()
        monitor.clear_subscribers()

        self.assertEqual(testval1, 11)
        self.assertEqual(testval2, 12)
        self.assertEqual(testval3, 13)

    def test_registering_multiple_same_then_deleting_one_deletes_all(self):
        # Registering the same script three times and then unsubscribing one time
        #   will cause all of the scripts to unsubscribe because they all had the
        #   same script subscription name.
        monitor.directory = good_folder_path

        testval = 1
        def test():
            nonlocal testval
            testval += 10

        monitor.clear_subscribers()
        monitor.subscribe('test', test)
        monitor.subscribe('test', test)
        monitor.subscribe('test', test)
        monitor.unsubscribe('test')
        monitor.watch()
        monitor.secure()
        monitor.clear_subscribers()

        self.assertEqual(testval, 1)

    def test_registering_multiple_different_then_deleting_one_deletes_only_that_one(self):
        # Registering the same script three times and then unsubscribing one time
        #   will cause all of the scripts to unsubscribe because they all had the
        #   same script subscription name.
        monitor.directory = good_folder_path

        testval = 1
        def test():
            nonlocal testval
            testval += 10

        monitor.clear_subscribers()
        monitor.subscribe('test1', test)
        monitor.subscribe('test2', test)
        monitor.subscribe('test3', test)
        monitor.unsubscribe('test2')
        monitor.watch()
        monitor.secure()
        monitor.clear_subscribers()

        self.assertEqual(testval, 21)
        

    ###############################################################
    # Detect Changes in Files and Folders
    ###############################################################
    
    def test_modify_tracked_file(self):
        # While watching a file, modifications to it should cause an event to fire
        create_test_files()
        monitor.directory = testfile_path

        testval = 1
        def test():
            nonlocal testval
            testval += 10

        monitor.clear_subscribers()
        monitor.subscribe('test1', test)
        monitor.subscribe('test2', test)
        monitor.subscribe('test3', test)
        monitor.watch()
        time.sleep(monitor.polling_delay * 1.1)
        modify_test_file1()
        time.sleep(monitor.polling_delay * 1.1)
        modify_test_file1()
        time.sleep(monitor.polling_delay * 1.1)
        monitor.secure()
        monitor.clear_subscribers()

        self.assertEqual(testval, 91)

        delete_test_files()

    def test_modify_tracked_folder(self):
        # While watching a folder, modifications to any file within should cause an event to fire
        create_test_files()
        monitor.directory = good_folder_path

        testval = 1
        def test():
            nonlocal testval
            testval += 10

        monitor.clear_subscribers()
        monitor.subscribe('test1', test)
        monitor.subscribe('test2', test)
        monitor.subscribe('test3', test)
        monitor.watch()
        modify_test_file1()
        time.sleep(monitor.polling_delay * 1.2)
        modify_test_file2()
        time.sleep(monitor.polling_delay * 1.2)
        monitor.secure()
        monitor.clear_subscribers()
        
        self.assertEqual(testval, 91)

        delete_test_files()
    
    def test_modify_untracked_file(self):
        # While watching a file, modifications to a different file should not cause an event to fire
        create_test_files()
        monitor.directory = testfile_path

        testval = 1
        def test():
            nonlocal testval
            testval += 10

        monitor.clear_subscribers()
        monitor.subscribe('test1', test)
        monitor.subscribe('test2', test)
        monitor.subscribe('test3', test)
        monitor.watch()
        modify_test_file1()
        time.sleep(monitor.polling_delay * 1.1)
        modify_test_file2()
        time.sleep(monitor.polling_delay * 1.1)
        monitor.secure()
        monitor.clear_subscribers()

        self.assertEqual(testval, 61)

        delete_test_files()

    def test_modify_untracked_folder(self):
        # While watching a folder, modifications to a file in a different folder should not cause an event to fire
        create_test_files()
        monitor.directory = os.path.dirname(testfile_path)

        testval = 1
        def test():
            nonlocal testval
            testval += 10

        monitor.clear_subscribers()
        monitor.subscribe('test1', test)
        monitor.subscribe('test2', test)
        monitor.subscribe('test3', test)
        monitor.watch()
        modify_test_file1()
        time.sleep(monitor.polling_delay * 1.1)
        modify_test_file2()
        time.sleep(monitor.polling_delay * 1.1)
        monitor.secure()
        monitor.clear_subscribers()

        self.assertEqual(testval, 61)

        delete_test_files()

    def test_add_files_to_tracked_folder(self):
        # While watching a folder, modifications to a file in a different folder should not cause an event to fire
        monitor.directory = os.path.dirname(testfile_path)

        testval = 1
        def test():
            nonlocal testval
            testval += 10

        monitor.clear_subscribers()
        monitor.subscribe('test', test)
        monitor.watch()
        create_test_files()
        time.sleep(monitor.polling_delay * 1.1)
        monitor.secure()
        monitor.clear_subscribers()

        self.assertEqual(testval, 21)

        delete_test_files()

    def test_delete_files_from_tracked_folder(self):
        # While watching a folder, deleting a file should trigger an event to fire.
        monitor.directory = os.path.dirname(testfile_path)
        create_test_files()

        testval = 1
        def test():
            nonlocal testval
            testval += 10
        
        monitor.clear_subscribers()
        monitor.subscribe('test', test)
        monitor.watch()
        delete_test_files()
        time.sleep(monitor.polling_delay * 1.1)
        monitor.secure()
        monitor.clear_subscribers()

        self.assertEqual(testval, 21)
    
    def test_delete_currently_tracked_file(self):
        # While watching a file, deleting it should cause the monitor to secure itself.
        create_test_files()
        monitor.directory = testfile_path

        testval = 1
        def test():
            nonlocal testval
            testval += 10
        
        monitor.clear_subscribers()
        monitor.subscribe('test', test)
        monitor.watch()
        delete_test_files()
        time.sleep(monitor.polling_delay * 1.1)
        monitor.secure()
        monitor.watch()
        monitor.clear_subscribers()

        self.assertEqual(testval, 11)


    ###############################################################
    # Test Singleton
    ###############################################################
    def test_singleton(self):
        # Call a new instance of DirectoryMonitor. In a normal class inheritance,
        #   the new instance would get default values. With this singleton, it should
        #    be the same as the original (which we modified away from default above).
        monitor2 = DirectoryMonitor()
        self.assertEqual(monitor.polling_delay, monitor2.polling_delay)


if __name__ == '__main__':
    unittest.main()