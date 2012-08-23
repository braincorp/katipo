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
				'katipo_schema': 1,
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


class TestKatipoFindRoot(TestWithRepoSetup):
	test_repo_description = {
				'katipo_schema': 1,
				'repos': [
				{'path': "test", 'test': True,
					'files': {'test': {'content': '#!/bin/sh\necho Testing\n',
										'exec': True}}},
				{'path': 'notest', 'test': False,
					'files': {'notest': {'content': 'Hello\n'}}}
				]}

	def setUp(self):
		TestWithRepoSetup.setUp(self)
		# Create a katipo working folder
		k = katipo.KatipoRoot(folder=os.path.join(self.tempfolder, 'workingcopy'),
				giturl=os.path.join(self.tempfolder, 'gitrepos/assemblies'),
				assemblyfile='testassembly.katipo')

	def test_find_root(self):
		"""Check that Katipo can find a katipo root after it is created."""
		katipo.KatipoRoot(folder=os.path.join(self.tempfolder, 'workingcopy'))


class TestKatipoSchemeVersion(TestWithRepoSetup):
	"""Check that the schema is checked and an Exception is raised if scheme
	is unknown (positive test case is implicit since it is need for other tests
	to pass."""
	test_repo_description = {
				'katipo_schema': 2,
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
