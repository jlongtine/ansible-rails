# -*- coding: utf-8 -*-

import os
import os.path
import sys

import unittest

from mock import Mock

from ansible.module_utils.basic import AnsibleModule

import imp
imp.load_source('bundle', os.path.join(os.path.dirname(__file__), os.path.pardir, 'library','bundle'))

from bundle import BundlerModule

class FakeAnsibleModule(object):
  check_mode = False
  params = {}


class TestBundle(unittest.TestCase):
  def test_run_bundler_with_path_option(self):
    module = FakeAnsibleModule()
    module.run_command = Mock(return_value=(0, "", ""))

    bundler = BundlerModule(module)
    bundler.get_bundle_path = Mock(return_value='/bin/bandler')
    bundler.run_bundle()

    module.run_command.assert_called_with(['/bin/bandler', 'install', '--without=deployment:test'], check_rc=True)

  """tests for resolving bundler binary. rely on AnsibleModule.get_bin_path
  when no executable is given
  """
  def test_get_bundle_path_with_defined_executable_parameter(self):
    module = FakeAnsibleModule()
    module.params['executable'] = '/bin/bandler'

    bundler = BundlerModule(module)
    assert bundler.get_bundle_path() == '/bin/bandler'

  def test_get_bundle_path_without_executable(self):
    module = FakeAnsibleModule()
    module.get_bin_path = Mock(return_value='/bin/bandler')

    bundler = BundlerModule(module)
    assert bundler.get_bundle_path() == '/bin/bandler'


  """general tests to classify bundler output correctly."""
  def test_install_without_changes(self):
    existing_output = """Using rake (10.1.1)
    Using i18n (0.6.9)"""

    assert BundlerModule(None).gems_were_changed(existing_output) == False

  def test_install_with_updated_gems(self):
    updated_output = """
      1 upgrade rails to 3.2.16
    Using i18n (0.6.9)"""
    assert BundlerModule(None).gems_were_changed(updated_output) == True

    old_updated_output = """
    Updating rails to 3.2.16
    Using i18n (0.6.9)"""
    assert BundlerModule(None).gems_were_changed(old_updated_output) == True

  def test_install_with_new_gems(self):
    install_output = """
    Installing i18n (0.6.9)"""
    assert BundlerModule(None).gems_were_changed(install_output) == True

if __name__ == '__main__':
  unittest.main()