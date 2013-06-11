# ===========================================================================
#
#  COPYRIGHT 2012-2013 Brain Corporation.
#  License under MIT license (see LICENSE file)
# =============================================================================

from setuptools import setup
import katipo


setup(name='katipo',
	author='Brain Corporation',
	author_email='hunt@braincorporation.com',
	url='https://github.com/braincorp/katipo',
	long_description='Tool for using multiple git repos together.',
	version=katipo.__version__,
	packages=['katipo'],
	scripts=['bin/katipo'],
	install_requires=['GitPython ==0.3.2.RC1'])
