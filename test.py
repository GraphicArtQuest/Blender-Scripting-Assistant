"""
Runs the unit tests for Blender Scripting Assistant.

The test classes are imported individually, but do not need additional references. Running unittest.main()
takes care of running all tests.
"""
import unittest

from tests.test_directory_monitor import TestDirectoryMonitor
from tests.test_bundler import TestBundler

if __name__ == '__main__':
    unittest.main()