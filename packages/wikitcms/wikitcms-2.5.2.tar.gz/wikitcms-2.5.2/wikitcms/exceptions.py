# Copyright (C) 2015 Red Hat
#
# This file is part of wikitcms.
#
# wikitcms is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Author: Adam Williamson <awilliam@redhat.com>

"""Defines custom exceptions used by wikitcms."""

from __future__ import unicode_literals
from __future__ import print_function


class NoPageError(Exception):
    """Page does not exist."""
    pass


class NotFoundError(Exception):
    """Requested thing wasn't found."""
    pass


class TooManyError(Exception):
    """Found too many of the thing you asked for."""
    pass


# this inherits from ValueError as the things that raise this may
# previously have passed along a ValueError from fedfind
class FedfindNotFoundError(ValueError, NotFoundError):
    """Couldn't find a fedfind release (probably the fedfind release
    that matches an event).
    """
    pass

# vim: set textwidth=100 ts=8 et sw=4:
