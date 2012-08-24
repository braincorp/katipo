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

import os
import git
import logging
import json
import sys
import shutil
import subprocess


class KatipoException(Exception):
	pass


class Assembly(object):
	"""Class for dealing with assembly files.

	Initialize with a JSON description of an assembly file."""
	def __init__(self, description):
		self.description = description
		if self.description['katipo_schema'] != 1:
			# Only recognise one schema at the moment
			raise KatipoException('Unknown katipo schema %s' %
								str(self.description['schema']))
		self.repos = description['repos']
		logging.info('Assembly object with repos %s' % json.dumps(
												description, indent=4))


class KatipoRoot(object):
	"""Class for interacting with a Katipo repo. It must either be passed
	a folder from which to search for a ketapo root or a giturl and assembly
	file."""
	def __init__(self, folder=None, giturl=None, assemblyfile=None):
		assert(folder is not None)
		if giturl is None:
			logging.info('Creating katipo from prexisting root')
			assert(assemblyfile is None)
			self._find_katipo_root(folder)
			self._reload_katipo_root()
		else:
			logging.info('Clone new katipo root')
			assert(assemblyfile is not None)
			try:
				self._clone(folder, giturl, assemblyfile)
			except:
				exc_info = sys.exc_info()
				if hasattr(self, '_katipo_root'):
					logging.warning('Removing incomplete katipo root %s' %
								self._katipo_root)
					try:
						shutil.rmtree(self._katipo_root)
					except:
						pass
				raise exc_info[1], None, exc_info[2]

	def _find_katipo_root(self, folder):
		"""Load in a katipo setup."""
		# Start from folder and find the root
		# Ensure we check this folder first
		last_checked = None
		while folder != last_checked:
			if os.path.exists(os.path.join(folder, '.katipo')):
				logging.info('Found katipo root in %s' % folder)
				self._working_copy_root = folder
				self._katipo_root = os.path.join(folder, '.katipo')
				return
			last_checked = folder
			folder = os.path.split(folder)[0]
		raise KatipoException('Unable to find .katipo root')

	def _reload_katipo_root(self):
		"""Reload the assembly file."""
		self._load_assembly()

	def _load_assembly(self):
		self.assembly = Assembly(json.load(open(os.path.join(os.path.join(
								self._katipo_root, 'assembly_file')))))

	def _clone(self, folder, assembly_giturl, assemblyfile):
		"""Initial a katipo setup in folder from assemblyfile in
		assembly_giturl."""
		logging.info('Cloning into %s from %s:/%s' %
					(folder, assembly_giturl, assemblyfile))
		self._create_katipo_root_folder(folder)
		self._assembly_repo = git.Repo.clone_from(assembly_giturl,
								os.path.join(self._katipo_root, 'assembly'))
		# Create a symlink to the assembly file to use
		os.symlink(os.path.join(self._katipo_root, 'assembly', assemblyfile),
				os.path.join(self._katipo_root, 'assembly_file'))
		self._load_assembly()
		for repo in self.assembly.repos:
			# Clone each repo
			git.Repo.clone_from(repo['giturl'], os.path.join(self._working_copy_root,
														repo['path']))

	def _create_katipo_root_folder(self, folder):
		"""Create a .katipo root folder."""
		# The reason for not placing .katipo_root in self immediately
		# is that if anything fails during clone we rm katipo_root
		# (since its probably in a messed up state).
		# We only want to do that if we created the folder.
		katipo_root = os.path.join(folder, '.katipo')
		os.mkdir(os.path.join(katipo_root))
		self._katipo_root = katipo_root
		self._working_copy_root = os.path.abspath(folder)

	def run_cmd_per_repo(self, cmd, test_only=False):
		"""Run shell command (given as a list) for all repos (or only test repos)."""
		return_code = 0
		logging.info('Running cmd per repo %s' % str(cmd))
		for repo in self.assembly.repos:
			if not test_only or repo['test'] is True:
				p = subprocess.Popen(' '.join(cmd), cwd=os.path.abspath(
									os.path.join(self._working_copy_root,
												repo['path'])),
									shell=True)
				return_code += p.wait()
		return return_code
