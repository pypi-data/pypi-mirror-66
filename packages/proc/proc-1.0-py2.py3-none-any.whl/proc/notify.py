# proc: Simple interface to Linux process information.
#
# Author: Peter Odding <peter@peterodding.com>
# Last Change: April 26, 2020
# URL: https://proc.readthedocs.io

"""
The :mod:`proc.notify` module implements a headless notify-send_ program.

.. contents::
   :local:

Introduction to notify-send
---------------------------

The notify-send program can be used to send desktop notifications to the user
from the command line. It's great for use in otherwise non-interactive programs
to unobtrusively inform the user about something, for example I use it to show
a notification when a system backup is starting and when it has completed (see
my rsync-system-backup_ package).

Problems using notify-send
--------------------------

One problem is that notify-send needs access to a few environment variables
from the desktop session in order to deliver its message. The values of these
environment variables change every time a desktop session is started. This
complicates the use of notify-send from e.g. system daemons and `cron jobs`_
(say for an automated backup solution :-).

The notify-send-headless program
--------------------------------

This module builds on top of the :mod:`proc.core` module as a trivial (but
already useful :-) example of how the `proc` package can be used to search
through the environments of all available processes. It looks for the variables
in :attr:`REQUIRED_VARIABLES` in the environments of all available processes
and uses the values it finds to run the notify-send program. It's available on
the command line as ``notify-send-headless`` (which accepts the same arguments
as ``notify-send``). Given super-user privileges this should work fine out of
the box on any Linux system.

The with-gui-environment program
--------------------------------

This module also implements the ``with-gui-environment`` program which uses the
same algorithm as ``notify-send-headless`` to identify the desktop session but
instead of running the notify-send command it can execute arbitrary commands.

My personal use case for the ``with-gui-environment`` program is to execute
programs like xrandr_ in my desktop session from custom udev_ rules (which by
default run commands as root, disconnected from the desktop session).

.. _cron jobs: http://unix.stackexchange.com/q/111188
.. _notify-send: http://manpages.debian.org/cgi-bin/man.cgi?query=notify-send
.. _rsync-system-backup: https://rsync-system-backup.readthedocs.io/
.. _udev: https://en.wikipedia.org/wiki/Udev
.. _xrandr: https://manpages.debian.org/xrandr
"""

# Standard library modules.
import collections
import logging
import os
import sys

# External dependencies.
import coloredlogs
from executor import CommandNotFound, ExternalCommandFailed
from executor.contexts import LocalContext

# Modules included in our package.
from proc.core import find_processes

# Public identifiers that require documentation.
__all__ = (
    'REQUIRED_VARIABLES',
    'find_graphical_context',
    'logger',
    'main',
    'notify_desktop',
    'with_gui_environment',
)

REQUIRED_VARIABLES = 'DBUS_SESSION_BUS_ADDRESS', 'DISPLAY', 'XAUTHORITY'
"""The names of environment variables required by ``notify-send`` (a tuple of strings)."""

# Initialize a logger for this module.
logger = logging.getLogger(__name__)


def main():
    """Command line interface for ``notify-send-headless``."""
    coloredlogs.install(syslog=True)
    context = find_graphical_context()
    context.execute('notify-send', *sys.argv[1:])


def with_gui_environment():
    """Command line interface for ``with-gui-environment``."""
    coloredlogs.install(syslog=True)
    context = find_graphical_context()
    command = context.execute(*sys.argv[1:], check=False)
    sys.exit(command.returncode)


def notify_desktop(body, summary=None, **options):
    """
    Python API for headless ``notify-send`` commands.

    :param body: The notification's message / details (a string).
    :param summary: The notification's summary / title (a string, defaults to
                    :data:`None`).
    :param options: Any keyword arguments are translated into optional
                    arguments to the ``notify-send`` command (see the examples
                    below).

    This function is a wrapper around ``notify-send`` that knows how to run the
    ``notify-send`` command in the execution environment required to deliver
    notifications to the current graphical session, even if the current process
    is not part of a graphical session. Here's an example:

    >>> from proc.notify import notify_desktop
    >>> notify_desktop(summary="Battery low", body="Your laptop is about to die!", urgency="critical")
    """
    command_line = ['notify-send']
    for name, value in sorted(options.items()):
        command_line.append('--%s=%s' % (name.replace('_', '-'), value))
    if summary:
        command_line.append(summary)
    command_line.append(body)
    context = find_graphical_context()
    try:
        context.execute(*command_line)
    except CommandNotFound:
        logger.debug("Desktop notification failed (the `notify-send' program isn't installed).")
    except ExternalCommandFailed:
        logger.debug("Desktop notification failed (the `notify-send' program reported an error).")


def find_graphical_context():
    """
    Create a command execution context for the current graphical session.

    :returns: A :class:`~executor.contexts.LocalContext` object.

    This function scans the process tree for processes that are running in a
    graphical session and collects information about graphical sessions from
    each of these processes. The collected information is then ranked by
    "popularity" (number of occurrences) and the most popular information is
    used to create a command execution context that targets the graphical
    session.
    """
    options = {}
    # Collect information about graphical sessions from running processes.
    matches = collections.defaultdict(int)
    for process in find_processes():
        environment = dict((k, v) for k, v in process.environ.items() if k in REQUIRED_VARIABLES and v)
        if environment:
            hashable_environment = tuple(sorted(environment.items()))
            matches[(process.user_ids.real, hashable_environment)] += 1
    ordered = sorted((counter, key) for key, counter in matches.items())
    if ordered:
        # Pick the most popular graphical session.
        counter, key = ordered[-1]
        uid, environment = key
        # Apply the user ID to the context?
        if os.getuid() != uid:
            options['uid'] = uid
        # Apply the environment to the context.
        options['environment'] = dict(environment)
    return LocalContext(**options)
