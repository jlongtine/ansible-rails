# -*- coding: utf-8 -*-

import os
import os.path
import sys

import unittest

from ansible.module_utils.basic import AnsibleModule

import imp
imp.load_source('bundle', os.path.join(os.path.dirname(__file__), os.path.pardir, 'library','bundle'))

from bundle import gems_were_changed

class FakeAnsibleModlue(object):
  def run_command(cmd):
    return (0, "foo", "bar")

class TestBundle(unittest.TestCase):
  def test_install_without_changes(self):
    existing_output = """Using rake (10.1.1)
    Using i18n (0.6.9)"""

    assert gems_were_changed(existing_output) == False

  def test_install_with_updated_gems(self):
    updated_output = """
      1 upgrade rails to 3.2.16
    Using i18n (0.6.9)"""
    assert gems_were_changed(updated_output) == True

    old_updated_output = """
    Updating rails to 3.2.16
    Using i18n (0.6.9)"""
    assert gems_were_changed(old_updated_output) == True

  def test_install_with_new_gems(self):
    install_output = """
    Installing i18n (0.6.9)"""
    assert gems_were_changed(install_output) == True

if __name__ == '__main__':
  unittest.main()