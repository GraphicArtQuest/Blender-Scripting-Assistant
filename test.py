"""
Runs the unit tests for Blender Scripting Assistant.

The test classes are imported individually, but do not need additional references. Running unittest.main()
takes care of running all tests.
"""
import unittest

from tests.test_directory_monitor import TestDirectoryMonitor
from tests.test_bundler import TestBundler
from tests.test_hot_swap import TestHotSwap_create_addon_name
from tests.test_hot_swap import TestHotSwap_get_most_recent_bl_name_info

if __name__ == '__main__':
    unittest.main()