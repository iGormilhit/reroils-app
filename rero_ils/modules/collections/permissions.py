# -*- coding: utf-8 -*-
#
# RERO ILS
# Copyright (C) 2020 RERO
# Copyright (C) 2020 UCLouvain
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Collection permissions."""

from rero_ils.modules.organisations.api import current_organisation
from rero_ils.modules.patrons.api import current_patron
from rero_ils.modules.permissions import RecordPermission


class CollectionPermission(RecordPermission):
    """Collection permissions."""

    @classmethod
    def list(cls, user, record=None):
        """List permission check.

        :param user: Logged user.
        :param record: Record to check.
        :return: True if action can be done.
        """
        # everyone can list document
        return True

    @classmethod
    def read(cls, user, record):
        """Read permission check.

        :param user: Logged user.
        :param record: Record to check.
        :return: True if action can be done.
        """
        # same as list permission
        return cls.list(user, record)

    @classmethod
    def create(cls, user, record=None):
        """Create permission check.

        :param user: Logged user.
        :param record: Record to check.
        :return: True if action can be done.
        """
        # user should be authenticated
        if not current_patron:
            return False
        # only staff members (lib,sys_lib) are allowed to create any collection
        return current_patron.is_librarian

    @classmethod
    def update(cls, user, record):
        """Update permission check.

        :param user: Logged user.
        :param record: Record to check.
        :return: True if action can be done.
        """
        # only staff members (lib, sys_lib) can update collection
        # record cannot be null
        if not current_patron or not current_organisation:
            return False
        if current_patron.is_librarian:
            return current_organisation['pid'] == record.organisation_pid
        return False

    @classmethod
    def delete(cls, user, record):
        """Delete permission check.

        :param user: Logged user.
        :param record: Record to check.
        :return: True if action can be done.
        """
        # same as update
        return cls.update(user, record)
