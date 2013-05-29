# ===========================================================================
#
#  COPYRIGHT 2012-2013 Brain Corporation.
#  License under MIT license (see LICENSE file)
# =============================================================================

import unittest
import pytest

import cmdline
from test_reposetup import TestWithRepoSetup
import os
import mock


class TestWithClone(TestWithRepoSetup):
	"""Helper class with clone command"""
	def clone(self):
		"""Make working copy (used in other tests)."""
		cmdline.run_args(['clone', os.path.join(self.tempfolder, 'gitrepos',
				'assemblies'), 'testassembly.katipo', 'workingcopy'], working_dir=
				os.path.join(self.tempfolder))


class TestStandaloneCommands(unittest.TestCase):
	def test_version(self):
		with pytest.raises(SystemExit):
			cmdline.run_args(['--version'], os.getcwd())


class TestCommands(TestWithClone):
	test_repo_description = {
				'version': 1,
				'repos': [
				{'path': "test", 'test': True,
					'files': {'test': {'content': '#!/bin/sh\ntouch testran\n',
										'exec': True}}},
				{'path': 'notest', 'test': False,
					'files': {'notest': {'content': 'Hello\n'}}}
				]}

	def test_clone(self):
		self.clone()
		# Check that the two repos in the assembly were created properly
		os.stat(os.path.join(self.tempfolder, 'workingcopy', 'test', 'test'))
		os.stat(os.path.join(self.tempfolder, 'workingcopy', 'notest', 'notest'))

	def test_clone_with_default(self):
		cmdline.run_args(['clone', os.path.join(self.tempfolder, 'gitrepos',
				'assemblies'), 'testassembly.katipo'], working_dir=
				os.path.join(self.tempfolder))
		assert os.path.exists(os.path.join(self.tempfolder, 'testassembly'))
		assert os.path.exists(os.path.join(self.tempfolder, 'testassembly',
										'.katipo'))

	def test_perrepo(self):
		self.clone()
		cmdline.run_args(['perrepo', 'ls', '-l'], working_dir=
				os.path.join(self.tempfolder, 'workingcopy'))

	def test_test_cmd(self):
		self.clone()
		cmdline.run_args(['test', 'touch', 'foo3'], working_dir=
				os.path.join(self.tempfolder, 'workingcopy'))
		assert os.path.exists(os.path.join(self.tempfolder,
							'workingcopy', 'test', 'foo3'))
		assert not os.path.exists(os.path.join(self.tempfolder,
							'workingcopy', 'notest', 'foo3'))

	def test_test_cmd_no_args(self):
		self.clone()
		cmdline.run_args(['test'], working_dir=
				os.path.join(self.tempfolder, 'workingcopy'))
		assert os.path.exists(os.path.join(self.tempfolder,
							'workingcopy', 'test', 'testran'))


class TestCheckout(TestWithClone):
	test_repo_description = {
			'version': 1,
			'repos': [
			{'path': "test", 'test': True, 'branch': 'test-branch',
				'files': {'testfoo': {'content': 'foo'}}},
			{'path': 'onlymaster', 'test': True,
				'files': {'testonlymaster': {'content': 'foo'}}}]}

	def test_checkout(self):
		self.clone()
		cmdline.run_args(['checkout', '-t', 'origin/test-branch'],
				os.path.join(self.tempfolder, 'workingcopy'))
		assert os.path.exists(os.path.join(self.tempfolder,
							'workingcopy', 'test', 'testfoo'))


# Flat test using py.test monkey patching support
def test_virtualenv_command(monkeypatch):
	k = mock.Mock()
	monkeypatch.setattr(cmdline.katipo, 'KatipoRoot', k)
	cmdline.run_args(['virtualenv'])
	k.return_value.setup_virtualenv.assert_called_with(
												python_exe=None)

	cmdline.run_args(['virtualenv', '--python', 'python27'])
	k.return_value.setup_virtualenv.assert_called_with(
												python_exe='python27')
