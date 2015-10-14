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


class ListHostingDevice(neutronV20.ListCommand):
    """List hosting devices that belong to a given tenant."""

    resource = 'hosting_device'
    list_columns = ['id', 'name', 'template_id', 'admin_state_up',
                    'created_at', 'status']
    pagination_support = True
    sorting_support = True


class ShowHostingDevice(neutronV20.ShowCommand):
    """Show information of a given hosting device."""

    resource = 'hosting_device'


class CreateHostingDevice(neutronV20.CreateCommand):
    """Create a hosting device for a given tenant."""

    resource = 'hosting_device'

    def add_known_arguments(self, parser):
        parser.add_argument(
            'name', metavar='NAME',
            help=_('Name of hosting device to create.'))
        parser.add_argument(
            '--disabled',
            dest='enabled',
            action='store_false',
            help=_('Disable the hostingdevice template.'),
            default=argparse.SUPPRESS)
        parser.add_argument(
            '--host_category',
            help=_('Host category for this hosting device template. One of '
                   'VM, Hardware, or, Network_Node.'))
        parser.add_argument(
            '--service_types',
            help=_('Service types supported by this hosting device template.'))
        parser.add_argument(
            '--glance_image',
            help=_('Glance image used by this hosting device template.'))
        parser.add_argument(
            '--nova_flavor',
            help=_('Nova flavor used by this hosting device template.'))
        parser.add_argument(
            '--default_credentials_id',
            help=_('Id of credentials used by default for hosting devices '
                   'based on this template.'))
        parser.add_argument(
            '--configuration mechanism',
            help=_('Method used to configure hosting devices based on this '
                   'template.'))
        parser.add_argument(
            '--protocol_port',
            help=_('TCP/UDP port used for management of hosting devices '
                   'based on this template.'))
        parser.add_argument(
            '--booting_time',
            help=_('Typical time to boot hosting devices based on this '
                   'template.'))
        parser.add_argument(
            '--slot_capacity',
            help=_('Capacity (in slots) for hosting devices based on this '
                   'template.'))
        parser.add_argument(
            '--desired_slot_free',
            help=_('Number of slots to keep available in hosting devices '
                   'based on this template.'))
        parser.add_argument(
            '--tenant_bound',
            help=_('Tenant allowed place service instances in hosting devices '
                   'based on this template.'))

    def args2body(self, parsed_args):
        body = {self.resource: {'admin_state_up': parsed_args.admin_state}}
        neutronV20.update_dict(parsed_args, body[self.resource],
                               ['name', 'tenant_id', 'distributed', 'ha'])
        return body


class DeleteHostingDevice(neutronV20.DeleteCommand):
    """Delete a given hosting device."""

    resource = 'hosting_device'


class UpdateHostingDevice(neutronV20.UpdateCommand):
    """Update hosting device's information."""

    resource = 'hosting_device'
