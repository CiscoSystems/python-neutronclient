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


class ListHostingDeviceTemplate(neutronV20.ListCommand):
    """List hosting device templates that belong to a given tenant."""

    resource = 'hosting_device_template'
    list_columns = ['id', 'name', 'host_category', 'service_types',
                    'enabled']
    pagination_support = True
    sorting_support = True


class ShowHostingDeviceTemplate(neutronV20.ShowCommand):
    """Show information of a given hosting device template."""

    resource = 'hosting_device_template'


class CreateHostingDeviceTemplate(neutronV20.CreateCommand):
    """Create a hosting device template for a given tenant."""

    resource = 'hosting_device_template'

    def add_known_arguments(self, parser):
        parser.add_argument(
            'name', metavar='NAME',
            help=_('Name of hosting device template to create.'))
        parser.add_argument(
            '--template_id',
            help=_('Id of hosting device template template to associate hosting device '
                   'with.'))
        parser.add_argument(
            '--credential_id',
            help=_('Id of credential used by hosting device.'))
        parser.add_argument(
            '--device_id',
            help=_('Manufacturer id of hosting device.'))
        parser.add_argument(
            '--device_id',
            help=_('Manufacturer id of hosting device.'))
        parser.add_argument(
            '--admin_state_down',
            dest='admin_state_up',
            action='store_false',
            help=_('Set hosting_device_template administratively down.'),
            default=argparse.SUPPRESS)
        parser.add_argument(
            '--management_ip_address',
            help=_('IP address used for management of hosting device.'))
        parser.add_argument(
            '--management_port_id',
            help=_('Neutron port used for management of hosting device.'))
        parser.add_argument(
            '--protocol_port',
            help=_('Protocol port used for management of hosting device.'))
        parser.add_argument(
            '--cfg_agent_id',
            help=_('Config agent to handle the hosting device.'))
        parser.add_argument(
            '--tenant_bound',
            help=_('Tenant allowed place service instances in the hosting '
                   'device.'))
        parser.add_argument(
            '--disabled',
            dest='enabled',
            action='store_false',
            help=_('Make the hosting device template disabled.'),
            default=argparse.SUPPRESS)

    def args2body(self, parsed_args):
        body = {self.resource: {'admin_state_up': parsed_args.admin_state}}
        neutronV20.update_dict(parsed_args, body[self.resource],
                               ['name', 'tenant_id', 'distributed', 'ha'])
        return body


class DeleteHostingDeviceTemplate(neutronV20.DeleteCommand):
    """Delete a given hosting device template."""

    resource = 'hosting_device_template'


class UpdateHostingDeviceTemplate(neutronV20.UpdateCommand):
    """Update hosting device template's information."""

    resource = 'hosting_device_template'
