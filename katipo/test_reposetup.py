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
"""Helper class for initializing a katipo repo based on a variant of an
assemblyfile (also contains the repo contents for ease of testing)."""

import tempfile
import unittest
import logging
import git
import os
import copy
import json
import shutil
import katipo


def create_repo_with_files(repo_path, files, branch=None):
	"""Create a git repo at repo_path containing files (list of dicts with
	{'filename' : {'content' : 'content', 'exec' : true }} exec is optional"""
	repo = git.Repo.init(repo_path, True)
	if branch is not None:
		# Create everything in a branch
		# First create an empty master branch
		logging.info('Creating on branch %s' % branch)
		filename = os.path.join(repo.working_dir, '_master')
		with open(filename, 'w') as f:
			pass
		repo.git.add(filename)
		repo.git.commit(m='dummy master branch')
		repo.git.checkout(b=branch)

	for filename, desc in files.iteritems():
		logging.info('Creating test file %s' % filename)
		full_filename = os.path.join(repo.working_dir, filename)
		with open(full_filename, 'w') as f:
			f.write(desc['content'])
		if desc.get('exec', False):
			os.chmod(full_filename, 0744)
		repo.git.add(full_filename)
	repo.git.commit(m=' "added files"')

	# Now switch back to make master the default branch
	if branch is not None:
		repo.git.checkout('master')


class TestWithRepoSetup(unittest.TestCase):
	def setUp(self, checkout=False):
		"""Create a fake assemblyfile and other repos for testing."""
		self.tempfolder = tempfile.mkdtemp(prefix='tmp-katipo-test')
		logging.info('Creating temporary git setup in %s' % self.tempfolder)
		os.mkdir(os.path.join(self.tempfolder, 'workingcopy'))
		os.mkdir(os.path.join(self.tempfolder, 'gitrepos'))

		self.create_test_repos()
		self.setup_assembly_file()

		if checkout:
			self.checkout_working_copy()

	def checkout_working_copy(self):
		self.k = katipo.KatipoRoot(folder=os.path.join(
				self.tempfolder, 'workingcopy'),
				giturl=os.path.join(self.tempfolder, 'gitrepos/assemblies'),
				assemblyfile='testassembly.katipo')

	def create_test_repos(self):
		"""Create two repos - test and notest for the assembly file to point to."""
		assembly_repos = []
		# Transform the test description of a repo (which includes the file
		# content into a assemblyfile description while creating the repos.
		for repo in self.test_repo_description['repos']:
			# Create this repo
			giturl = os.path.join(self.tempfolder, 'gitrepos', repo['path'])
			create_repo_with_files(giturl, repo['files'],
								branch=repo.get('branch', None))
			assembly_repos.append({'path': repo['path'],
								'test': repo['test'], 'giturl': giturl})
		self._assembly_desc = copy.copy(self.test_repo_description)
		self._assembly_desc['repos'] = assembly_repos

	def setup_assembly_file(self):
		"""Create an assembly file and repo to hold it."""
		create_repo_with_files(os.path.join(self.tempfolder, 'gitrepos',
				'assemblies'), {'testassembly.katipo': {'content':
										json.dumps(self._assembly_desc, indent=4)}})

	def tearDown(self):
		shutil.rmtree(self.tempfolder)
