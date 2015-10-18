# Copyright 2015 Cisco Systems, Inc.
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

from neutronclient.common import extension
from neutronclient.i18n import _
from neutronclient.neutron import v2_0 as neutronV20


DEVICE = 'hosting_device'


def _add_updatable_args(parser):
    parser.add_argument(
        '--credentials-id',
        help=_('Id of credentials used by this hosting device.'))
    parser.add_argument(
        '--name',
        help=_('Name of this hosting device'))
    parser.add_argument(
        '--description',
        help=_('Description of this hosting device.'))
    parser.add_argument(
        '--device-id',
        help=_('Manufacturer id of hosting device.'))
    parser.add_argument(
        '--device_id',
        help=argparse.SUPPRESS)
    parser.add_argument(
        '--admin-state-down',
        dest='admin_state_up',
        action='store_false',
        help=_('Set hosting device administratively down.'),
        default=argparse.SUPPRESS)
    parser.add_argument(
        '--admin_state_down',
        dest='admin_state_up',
        action='store_false',
        help=argparse.SUPPRESS,
        default=argparse.SUPPRESS)
    parser.add_argument(
        '--tenant-bound',
        help=_('Tenant allowed place service instances in the hosting '
               'device.'))
    parser.add_argument(
        '--tenant_bound',
        help=argparse.SUPPRESS)
    parser.add_argument(
        '--auto-delete',
        dest='auto_delete',
        action='store_true',
        help=_('Make hosting device subject to automated life cycle '
               'management.'),
        default=argparse.SUPPRESS)
    parser.add_argument(
        '--auto_delete',
        dest='auto_delete',
        action='store_true',
        help=argparse.SUPPRESS,
        default=argparse.SUPPRESS)


def _updatable_args2body(parsed_args, body):
    neutronV20.update_dict(parsed_args, body[DEVICE],
                               ['credentials_id', 'name', 'description',
                                'device_id', 'admin_state_up', 'auto_delete'])
    # handle tenant_bound separately as we want to allow it to be set to None
    if parsed_args.tenant_bound:
        if (isinstance(parsed_args.tenant_bound, basestring) and
                parsed_args.tenant_bound.lower() == 'none'):
            parsed_args.tenant_bound = None
        body[DEVICE].update({'tenant_bound': parsed_args.tenant_bound})


class HostingDevice(extension.NeutronClientExtension):
    resource = DEVICE
    resource_plural = '%ss' % resource
    object_path = '/dev_mgr/%s' % resource_plural
    resource_path = '/dev_mgr/%s/%%s' % resource_plural
    versions = ['2.0']
    allow_names = True


class HostingDeviceList(extension.ClientExtensionList, HostingDevice):
    """List hosting devices that belong to a given tenant."""

    shell_command = 'cisco-hosting-device-list'
    list_columns = ['id', 'name', 'template_id', 'admin_state_up',
                    'created_at', 'status']
    pagination_support = True
    sorting_support = True


class HostingDeviceShow(extension.ClientExtensionShow, HostingDevice):
    """Show information of a given hosting device."""

    shell_command = 'cisco-hosting-device-show'


class HostingDeviceCreate(extension.ClientExtensionCreate, HostingDevice):
    """Create a hosting device for a given tenant."""

    shell_command = 'cisco-hosting-device-create'

    def add_known_arguments(self, parser):
        parser.add_argument(
            '--template_id',
            help=_('Id of hosting device template template to associate '
                   'hosting device with.'))
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
            'name', metavar='NAME',
            help=_('Name of hosting device to create.'))

    def args2body(self, parsed_args):
        body = {self.resource: {'admin_state_up': parsed_args.admin_state}}
        neutronV20.update_dict(parsed_args, body[self.resource],
                               ['name', 'tenant_id', 'distributed', 'ha'])
        return body


class HostingDeviceDelete(extension.ClientExtensionDelete, HostingDevice):
    """Delete a given hosting device."""

    shell_command = 'cisco-hosting-device-delete'


class HostingDeviceUpdate(extension.ClientExtensionUpdate, HostingDevice):
    """Update hosting device's information."""

    shell_command = 'cisco-hosting-device-update'

    def add_known_arguments(self, parser):
        # adding admin_state_up here so that it is available for update only
        # as it is True by default and not meaningful in the create operation
        parser.add_argument(
            '--admin-state-up',
            dest='admin_state_up',
            action='store_true',
            help=_('Set hosting device administratively up.'),
            default=argparse.SUPPRESS)
        parser.add_argument(
            '--admin_state_up',
            dest='admin_state_up',
            action='store_true',
            help=argparse.SUPPRESS,
            default=argparse.SUPPRESS)
        # adding no_auto_delete here so that it is available for update only
        # as auto_delete is False by default and not meaningful in the create
        # operation
        parser.add_argument(
            '--no-auto-delete',
            dest='auto_delete',
            action='store_false',
            help=_('Exempt hosting device from automated life cycle '
                   'management.'),
            default=argparse.SUPPRESS)
        parser.add_argument(
            '--no_auto_delete',
            dest='auto_delete',
            action='store_false',
            help=argparse.SUPPRESS,
            default=argparse.SUPPRESS)
        _add_updatable_args(parser)

    def args2body(self, parsed_args):
        body = {self.resource: {}}
        _updatable_args2body(parsed_args, body)
        return body