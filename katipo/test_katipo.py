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

"""Test the primary ketapo object."""

import unittest
import git
import tempfile
import logging
import os
import shutil
import katipo
from test_reposetup import TestWithRepoSetup


class TestKatipoRootBasics(TestWithRepoSetup):
	test_repo_description = {
				'version': 1,
				'repos': [
				{'path': "test", 'test': True,
					'files': {'test': {'content': '#!/bin/sh\necho Testing\n',
										'exec': True}}},
				{'path': 'notest', 'test': False,
					'files': {'notest': {'content': 'Hello\n'}}}
				]}

	def test_clone(self):
		k = katipo.KatipoRoot(folder=os.path.join(self.tempfolder, 'workingcopy'),
				giturl=os.path.join(self.tempfolder, 'gitrepos/assemblies'),
				assemblyfile='testassembly.katipo')
		# Check that the two repos in the assembly were created properly
		os.stat(os.path.join(self.tempfolder, 'workingcopy', 'test', 'test'))
		os.stat(os.path.join(self.tempfolder, 'workingcopy', 'notest', 'notest'))

	def test_overclone(self):
		"""Check that trying to clone on top of an existing katipo setup throws an
		Exception."""
		k = katipo.KatipoRoot(folder=os.path.join(self.tempfolder, 'workingcopy'),
				giturl=os.path.join(self.tempfolder, 'gitrepos/assemblies'),
				assemblyfile='testassembly.katipo')

		def _run():
			katipo.KatipoRoot(folder=os.path.join(self.tempfolder, 'workingcopy'),
				giturl=os.path.join(self.tempfolder, 'gitrepos/assemblies'),
				assemblyfile='testassembly.katipo')
		self.assertRaises(Exception, _run)


class TestWithWorkingCopyCommands(TestWithRepoSetup):
	test_repo_description = {
				'version': 1,
				'repos': [
				{'path': "test", 'test': True,
					'files': {'test': {'content': '#!/bin/sh\necho Testing\n',
										'exec': True}}},
				{'path': 'notest', 'test': False,
					'files': {'notest': {'content': 'Hello\n'}}}
				]}

	def setUp(self):
		TestWithRepoSetup.setUp(self, checkout=True)

	def test_find_root(self):
		"""Check that Katipo can find a katipo root after it is created."""
		katipo.KatipoRoot(folder=os.path.join(self.tempfolder, 'workingcopy'))
		# Check that you can find it inside a folder
		os.mkdir(os.path.join(self.tempfolder, 'workingcopy', 'test', 'foo'))
		katipo.KatipoRoot(folder=os.path.join(self.tempfolder, 'workingcopy',
											'test', 'foo'))

	def test_run_cmd_per_repo(self):
		self.k.run_cmd_per_repo(['ls'])


class TestKatipoSchemeVersion(TestWithRepoSetup):
	"""Check that the schema is checked and an Exception is raised if scheme
	is unknown (positive test case is implicit since it is need for other tests
	to pass."""
	test_repo_description = {
				'version': 2,
				'repos': [
				{'path': "test", 'test': True,
					'files': {'test': {'content': '#!/bin/sh\necho Testing\n',
										'exec': True}}}]}

	def test_schema_check(self):
		def _run():
			katipo.KatipoRoot(folder=os.path.join(self.tempfolder, 'workingcopy'),
				giturl=os.path.join(self.tempfolder, 'gitrepos/assemblies'),
				assemblyfile='testassembly.katipo')
		self.assertRaises(Exception, _run)


class TestKatipoCheckoutSingleBranch(TestWithRepoSetup):
	test_repo_description = {
			'version': 1,
			'repos': [
			{'path': "test", 'test': True, 'branch': 'test-branch',
				'files': {'testfoo': {'content': 'foo'}}}]}

	def setUp(self):
		TestWithRepoSetup.setUp(self, checkout=True)

	def test_checkout_single_branch(self):
		self.k.checkout('origin/test-branch')
		assert os.path.exists(os.path.join(self.tempfolder,
										'workingcopy', 'test', 'testfoo'))


class TestKatipoCheckoutSingleBranch(TestWithRepoSetup):
	test_repo_description = {
			'version': 1,
			'repos': [
			{'path': "test", 'test': True, 'branch': 'test-branch',
				'files': {'testfoo': {'content': 'foo'}}},
			{'path': 'onlymaster', 'test': True,
				'files': {'testonlymaster': {'content': 'foo'}}}]}

	def setUp(self):
		TestWithRepoSetup.setUp(self, checkout=True)

	def test_checkout_conflicting_branches(self):
		self.k.checkout('origin/test-branch')
		assert os.path.exists(os.path.join(self.tempfolder,
										'workingcopy', 'test', 'testfoo'))
		assert os.path.exists(os.path.join(self.tempfolder,
										'workingcopy', 'onlymaster', 'testonlymaster'))


class TestKatipoVirtualEnv(TestWithRepoSetup):
	test_repo_description = {
			'version': 1,
			'repos': [
			{'path': "foo", 'test': False,
				'files': {'requirements.txt': {'content': 'pytest==2.2.4\n'}}},
			{'path': 'foo2', 'test': True,
				'files': {'requirements.txt': {'content': 'pytest-capturelog==0.7'}}}]}

	def setUp(self):
		TestWithRepoSetup.setUp(self, checkout=True)

	def test_virtualenv(self):
		self.k.setup_virtualenv()
		# Check that a virtual environment was create
		assert os.path.exists(os.path.join(self.tempfolder,
										'workingcopy', '.env'))
		# Check that the PYTHONPATH was added correctly
		# Check that pointer to tempfolder was added to activate.
		assert open(os.path.join(self.tempfolder, 'workingcopy', '.env',
						'bin', 'activate')).read().find(self.tempfolder) != -1

	def test_virtualenv_python(self):
		self.k.setup_virtualenv(python_exe='python')
		assert os.path.exists(os.path.join(self.tempfolder,
										'workingcopy', '.env'))


class TestKatipoVirtualEnvWithPrompt(TestWithRepoSetup):
	test_repo_description = {
			'version': 1,
			'repos': [
			{'path': "foo", 'test': False,
				'files': {'requirements.txt': {'content': 'pytest==2.2.4\n'}}},
			{'path': 'foo2', 'test': True,
				'files': {'requirements.txt': {'content': 'pytest-capturelog==0.7'}}}],
			'virtualenv': {'prompt': 'katipo_test_prompt'}}

	def setUp(self):
		TestWithRepoSetup.setUp(self, checkout=True)

	def test_virtualenv_prompt(self):
		self.k.setup_virtualenv()
		# Check that the PYTHONPATH was added correctly
		# Check that pointer to tempfolder was added to activate.
		assert open(os.path.join(self.tempfolder, 'workingcopy', '.env',
						'bin', 'activate')).read().find('katipo_test_prompt') != -1


class TestKatipoBaseFiles(TestWithRepoSetup):
	test_repo_description = {
			'version': 1,
			'repos': [
			{'path': "foo", 'test': False,
				'files': {'requirements.txt': {'content': 'pytest==2.2.4\n'}}},
			{'path': 'foo2', 'test': True,
				'files': {'requirements.txt': {'content': 'pytest-capturelog==0.7'}}}],
			'virtualenv': {'prompt': 'katipo_test_prompt'},
			'base_files': {'use_repo.sh': {'content': '#!/bin/sh\n Some content'}}}

	def setUp(self):
		TestWithRepoSetup.setUp(self, checkout=True)

	def test_base_files(self):
		use_repo_path = os.path.join(self.tempfolder, 'workingcopy', 'use_repo.sh')
		assert os.path.exists(use_repo_path)
		assert open(use_repo_path).read().find('Some content') != -1
