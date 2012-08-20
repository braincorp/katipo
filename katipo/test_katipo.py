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
import ketapo

class TestKetapoRootBasics(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		"""Create a fake assemblyfile and other repos for testing."""
		cls.tempfolder = tempfile.mkdtemp(prefix='tmp-ketapo-test')
		logging.info('Creating temporary git setup in %s' % cls.tempfolder)
		os.mkdir(os.path.join(cls.tempfolder, 'workingcopy'))
		
	def test_clone(self):
		k = ketapo.KetapoRoot(folder=os.path.join(self.tempfolder, 'workingcopy'),
				giturl=os.path.join(self.tempfolder, 'git/assemblyfiles'),
				assemblyfile=os.path.join(self.tempfolder, 'test.ketapo'))
	
	@classmethod
	def tearDownClass(self):
		shutil.rmtree(self.tempfolder)
