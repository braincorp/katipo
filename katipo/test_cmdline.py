# ===========================================================================
#
#  COPYRIGHT 2012 Brain Corporation.
#  All rights reserved. Brain Corporation proprietary and confidential.
#
#  The party receiving this software directly from Brain Corporation
#  (the "Recipient" ) may use this software and make copies thereof as
#  reasonably necessary solely for the purposes set forth in the agreement
#  between the Recipient and Brain Corporation ( the "Agreement" ). The
#  software may be used in source code form
#  solely by the Recipient's employees. The Recipient shall have no right to
#  sublicense, assign, transfer or otherwise provide the source code to any
#  third party. Subject to the terms and conditions set forth in the Agreement,
#  this software, in binary form only, may be distributed by the Recipient to
#  its customers. Brain Corporation retains all ownership rights in and to
#  the software.
#
#  This notice shall supercede any other notices contained within the software.
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
				'assemblies'), 'testassembly.katipo'], working_dir=
				os.path.join(self.tempfolder, 'workingcopy'))


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
												python_exe=None, prompt=None)

	cmdline.run_args(['virtualenv', '--python', 'python27', '--prompt', 'foo'])
	k.return_value.setup_virtualenv.assert_called_with(
												python_exe='python27', prompt='foo')
