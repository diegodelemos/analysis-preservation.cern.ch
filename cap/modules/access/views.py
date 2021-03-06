# -*- coding: utf-8 -*-
#
# This file is part of CERN Analysis Preservation Framework. 
# Copyright (C) 2016 CERN.
#
# CERN Analysis Preservation Framework is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# CERN Analysis Preservation Framework is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CERN Analysis Preservation Framework; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""Access blueprint in order to dispatch the login request."""

from __future__ import absolute_import, print_function

from flask import Blueprint

from flask_login import current_user
from flask_principal import identity_loaded
from flask import current_app
from flask_principal import AnonymousIdentity, RoleNeed

access_blueprint = Blueprint('cap_access', __name__,
                             url_prefix='/access',
                             template_folder='templates')


@identity_loaded.connect
def load_extra_info(sender, identity):
    """Access rights for user."""
    if isinstance(identity, AnonymousIdentity):
        return
    if current_user.get_id() is not None:
        # Fetch groups from the identity
        groups = identity.provides
        superuser_egroups = current_app.config.get('SUPERUSER_EGROUPS', [])
        superuser_roles = current_app.config.get('SUPERUSER_ROLES', {})

        # Grant all privileges if user is superuser
        if [i for i in superuser_egroups if i in groups]:
            identity.provides |= set(superuser_roles)

        # Grant priviliges according to group
        collab_egroups = current_app.config.get('CAP_COLLAB_EGROUPS', {})
        for collab, egroups in collab_egroups.iteritems():
            if [i for i in egroups if i in groups]:
                identity.provides |= set([RoleNeed(collab)])
