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

"""The command line interface to katipo. Run using script in root folder."""

import sys
import argparse
import logging
import abc


def register_cmd(future_class_name, future_class_parents, future_class_attr):
		print future_class_name
		return type(future_class_name, future_class_parents, future_class_attr)


class Command(object):
	@abc.abstractmethod
	def construct_parser(self, parser):
		pass

	@abc.abstractmethod
	def exec_cmd(self, args):
		pass

	@property
	def command_name(self):
		return type(self).__name__.split('_')[1]

	@classmethod
	def get_commands(cls):
		if not hasattr(cls, '_commands'):
			cls._commands = [cmd() for cmd in Command.__subclasses__()]
		return cls._commands


class Command_clone(Command):
	'Clone working copy from assembly description'
	def construct_parser(self, parser):
		parser.add_argument('assemblyrepo', type=str)
		parser.add_argument('assemblyfile', type=str)

	def exec_cmd(self, args):
		print 'clone %s' % str(args)


class Command_about(Command):
	'Learn more about katipo'
	def construct_parser(self, parser):
		pass

	def exec_cmd(self, args):
		print 'about'


def build_arg_parser():
	toplevel_parser = argparse.ArgumentParser(description=
											'katipo: deal with multiple git repos')
	subparsers = toplevel_parser.add_subparsers(help='sub-command help')
	for cmd in Command.get_commands():
		logging.info('Adding command %s', cmd.command_name)
		cmd_parser = subparsers.add_parser(cmd.command_name, help=cmd.__doc__)
		cmd_parser.set_defaults(cmd=cmd)
		cmd.construct_parser(cmd_parser)
	return toplevel_parser


def run_args(args):
	"""Execute the arguments passed."""
	logging.info('Args %s' % str(args))
	parser = build_arg_parser()
	input = parser.parse_args(args)


def main():
	"""First function called when invoked from the command line."""
	run_args(sys.argv[1:])

if __name__ == '__main__':
	main()
