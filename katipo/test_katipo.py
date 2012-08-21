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


def create_repo_with_file(repo_path, filename, content):
	"""Create a git repo at repo_path containing a file named filename
	containing content."""
	repo = git.Repo.init(repo_path, True)
	full_filename = os.path.join(repo.working_dir, filename)
	with open(full_filename, 'w') as f:
		f.write(content)
	repo.git.add(full_filename)
	repo.git.commit(m='"add file"')


class TestKatipoRootBasics(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		"""Create a fake assemblyfile and other repos for testing."""
		cls.tempfolder = tempfile.mkdtemp(prefix='tmp-katipo-test')
		logging.info('Creating temporary git setup in %s' % cls.tempfolder)
		os.mkdir(os.path.join(cls.tempfolder, 'workingcopy'))
		os.mkdir(os.path.join(cls.tempfolder, 'gitrepos'))

		cls.setup_assembly_file()
		cls.create_test_repos()

	@classmethod
	def setup_assembly_file(cls):
		"""Create an assembly file and repo to hold it."""
		create_repo_with_file(os.path.join(cls.tempfolder, 'gitrepos', 'assemblies'),
							filename='testassembly.katipo',
							content="""
			{"repos":[
				{"giturl" : "%s", "path" : "test", "test" :true},
				{"giturl" : "%s", "path" : "notest", "test" : false}
			]}
			""" % (os.path.join(cls.tempfolder, 'gitrepos', 'test'),
					os.path.join(cls.tempfolder, 'gitrepos', 'notest')))

	@classmethod
	def create_test_repos(cls):
		"""Create two repos - test and notest for the assembly file to point to."""
		create_repo_with_file(os.path.join(cls.tempfolder, 'gitrepos', 'test'),
							filename='test.sh',
							content='#!/bin/sh\necho Testing\n')
		create_repo_with_file(os.path.join(cls.tempfolder, 'gitrepos', 'notest'),
							filename='notest', content='Hello')

	def test_clone(self):
		k = katipo.KatipoRoot(folder=os.path.join(self.tempfolder, 'workingcopy'),
				giturl=os.path.join(self.tempfolder, 'gitrepos/assemblies'),
				assemblyfile='testassembly.katipo')
		# Check that the two repos in the assembly were created properly
		os.stat(os.path.join(self.tempfolder, 'workingcopy', 'test', 'test.sh'))
		os.stat(os.path.join(self.tempfolder, 'workingcopy', 'notest', 'notest'))

	@classmethod
	def tearDownClass(self):
		shutil.rmtree(self.tempfolder)
