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


class Assembly(object):
	"""Class for dealing with assembly files.

	Initialize with a JSON description of an assembly file."""
	def __init__(self, description):
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
			self._find_ketapo_root(folder)
		else:
			logging.info('Clone new katipo root')
			assert(assemblyfile is not None)
			self._clone(folder, giturl, assemblyfile)

	def _find_ketapo_root(self, folder):
		"""Load in a katipo setup."""
		raise NotImplementedError()

	def _clone(self, folder, assembly_giturl, assemblyfile):
		"""Initial a katipo setup in folder from assemblyfile in
		assembly_giturl."""
		logging.info('Cloning into %s from %s:/%s' %
					(folder, assembly_giturl, assemblyfile))
		self._katipo_root = os.path.join(folder, '.katipo')
		self._workingcopy_root = os.path.abspath(folder)
		os.mkdir(self._katipo_root)
		self._assembly_repo = git.Repo.clone_from(assembly_giturl,
								os.path.join(self._katipo_root, 'assembly'))
		self.assembly = Assembly(json.load(open(os.path.join(os.path.join(
								self._katipo_root, 'assembly', assemblyfile)))))
		for repo in self.assembly.repos:
			# Clone each repo
			git.Repo.clone_from(repo['giturl'], os.path.join(self._workingcopy_root,
														repo['path']))
