# -*- coding: utf-8 -*-
"""Windows Registry related functions and classes for testing."""

from __future__ import unicode_literals

import os
import unittest


class BaseTestCase(unittest.TestCase):
  """The base test case."""

  _TEST_DATA_PATH = os.path.join(os.getcwd(), 'test_data')

  # Show full diff results, part of TestCase so does not follow our naming
  # conventions.
  maxDiff = None

  def _GetTestFilePath(self, path_segments):
    """Retrieves the path of a test file relative to the test data directory.

    Args:
      path_segments (list[str]): path segments inside the test data directory.

    Returns:
      str: path of the test file.
    """
    # Note that we need to pass the individual path segments to os.path.join
    # and not a list.
    return os.path.join(self._TEST_DATA_PATH, *path_segments)

  def _SkipIfPathNotExists(self, path):
    """Skips the test if the path does not exist.

    Args:
      path (str): path of a test file.

    Raises:
      SkipTest: if the path path does not exist and the test should be skipped.
    """
    if not os.path.exists(path):
      filename = os.path.basename(path)
      raise unittest.SkipTest('missing test file: {0:s}'.format(filename))
