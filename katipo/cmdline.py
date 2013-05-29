# ===========================================================================
#
#  COPYRIGHT 2012-2013 Brain Corporation.
#  License under MIT license (see LICENSE file)
# =============================================================================

"""The command line interface to katipo. Run using script in root folder."""

import sys
import argparse
import logging
import abc
import os
import webbrowser
import katipo
from __init__ import __version__


class Command(object):
	@abc.abstractmethod
	def construct_parser(self, parser):
		pass

	@abc.abstractmethod
	def exec_cmd(self, args, working_dir):
		pass

	@property
	def command_name(self):
		return type(self).__name__.split('_')[1]

	@classmethod
	def get_commands(cls):
		if not hasattr(cls, '_commands'):
			cls._commands = [cmd() for cmd in cls._get_subclasses()]
		return cls._commands

	@classmethod
	def _get_subclasses(cls):
		"""Find all subclasses of this class."""
		subclasses = cls.__subclasses__()
		for sub in subclasses:
			subclasses.extend(sub._get_subclasses())
		return subclasses


class Command_clone(Command):
	'Clone working copy from assembly description'
	def construct_parser(self, parser):
		parser.add_argument('assemblyrepo', type=str)
		parser.add_argument('assemblyfile', type=str)
		parser.add_argument('clonelocation', type=str, nargs='?',
				help='Location where clone occurs - '
					'defaults to assembyfile name without extension')

	def exec_cmd(self, args, working_dir):
		clone_location = args.clonelocation
		if clone_location is None:
			# Default to cloning in the basename of assembly file
			clone_location = os.path.splitext(args.assemblyfile)[0]

		if os.path.isabs(clone_location):
			working_dir = clone_location
		else:
			working_dir = os.path.join(working_dir,
								clone_location)
		logging.info('Cloning into working_dir %s' % working_dir)
		katipo.KatipoRoot(folder=working_dir,
				giturl=args.assemblyrepo, assemblyfile=args.assemblyfile)


class Command_about(Command):
	'Learn more about katipo'
	def construct_parser(self, parser):
		pass

	def exec_cmd(self, args, working_dir):
		webbrowser.open_new('https://www.google.com/search?q=katipo')
		webbrowser.open('https://github.com/braincorp/katipo')


class Command_perrepo(Command):
	def construct_parser(self, parser):
		parser.add_argument('external_cmd', type=str,
						nargs=argparse.REMAINDER, help='command to run per repo')

	def exec_cmd(self, args, working_dir):
		logging.info('Executing command', args.external_cmd)
		k = katipo.KatipoRoot(folder=working_dir)
		k.run_cmd_per_repo(args.external_cmd)


class Command_test(Command_perrepo):
	def exec_cmd(self, args, working_dir):
		external_cmd = args.external_cmd
		if len(external_cmd) == 0:
			external_cmd = ['./test']
		logging.info('Executing command %s' % str(external_cmd))
		k = katipo.KatipoRoot(folder=working_dir)
		k.run_cmd_per_repo(external_cmd, test_only=True)


class Command_checkout(Command):
	def construct_parser(self, parser):
		parser.add_argument('-t', '--tracking', help='Create tracking branch',
						action="store_true")
		parser.add_argument('branch', help='Branch to checkout')

	def exec_cmd(self, args, working_dir):
		k = katipo.KatipoRoot(folder=working_dir)
		k.checkout(args.branch, tracking=args.tracking)


class Command_virtualenv(Command):
	def construct_parser(self, parser):
		parser.add_argument('--python', help='Set virtualenv python',
						action='store')

	def exec_cmd(self, args, working_dir):
		k = katipo.KatipoRoot(folder=working_dir)
		k.setup_virtualenv(python_exe=args.python)


def build_arg_parser():
	toplevel_parser = argparse.ArgumentParser(description=
											'katipo: deal with multiple git repos')
	subparsers = toplevel_parser.add_subparsers(help='sub-command help')
	toplevel_parser.add_argument('-v', '--version', help='Query version',
								action='version',
								version='katipo %s' % __version__)
	for cmd in Command.get_commands():
		logging.info('Adding command %s', cmd.command_name)
		cmd_parser = subparsers.add_parser(cmd.command_name, help=cmd.__doc__)
		cmd_parser.set_defaults(cmd=cmd)
		cmd.construct_parser(cmd_parser)
	return toplevel_parser


def run_args(args, working_dir=None):
	"""Execute the arguments passed."""
	if working_dir is None:
		working_dir = os.getcwd()
	logging.info('Args %s is working dir %s' % (str(args), working_dir))
	parser = build_arg_parser()
	input = parser.parse_args(args)
	input.cmd.exec_cmd(input, working_dir)


def main():
	"""First function called when invoked from the command line."""
	run_args(sys.argv[1:])


if __name__ == '__main__':
	main()
