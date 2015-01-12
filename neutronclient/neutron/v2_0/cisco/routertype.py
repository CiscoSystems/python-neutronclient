# Copyright 2012 OpenStack Foundation.
# All Rights Reserved
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#

from __future__ import print_function

import argparse

from neutronclient.i18n import _
from neutronclient.neutron import v2_0 as neutronV20


class ListRouterType(neutronV20.ListCommand):
    """List router types that belong to a given tenant."""

    resource = 'routertype'
    list_columns = ['id', 'name', 'description']
    pagination_support = True
    sorting_support = True


class ShowRouterType(neutronV20.ShowCommand):
    """Show information of a given router type."""

    resource = 'routertype'


class CreateRouterType(neutronV20.CreateCommand):
    """Create a router type for a given tenant."""

    resource = 'routertype'

    def add_known_arguments(self, parser):
        parser.add_argument(
            'name', metavar='NAME',
            help=_('Name of router type to create.'))
        parser.add_argument(
            '--description',
            help=_('Description of router type to create.'))
        parser.add_argument(
            '--template_id',
            help=_('Id of hosting device template to associate router type '
                   'with.'))
        parser.add_argument(
            '--shared',
            dest='shared',
            action='store_true',
            help=_('Make routertype shared among tenants.'),
            default=argparse.SUPPRESS)
        parser.add_argument(
            '--slot_need',
            help=_('Number of slots routers of this type consumes.'))
        parser.add_argument(
            '--scheduler',
            help=_('Scheduler module to use for routers of this router type.'))
        parser.add_argument(
            '--cfg_agent_driver',
            help=_('Device driver in config agent to use for routers of this '
                   'router type.'))

    def args2body(self, parsed_args):
        body = {self.resource: {'admin_state_up': parsed_args.admin_state}}
        neutronV20.update_dict(parsed_args, body[self.resource],
                               ['name', 'tenant_id', 'distributed', 'ha'])
        return body


class DeleteRouterType(neutronV20.DeleteCommand):
    """Delete a given router type."""

    resource = 'routertype'


class UpdateRouterType(neutronV20.UpdateCommand):
    """Update router type's information."""

    resource = 'routertype'
