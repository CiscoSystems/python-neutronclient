# Copyright 2013 OpenStack Foundation.
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

from neutronclient.i18n import _
from neutronclient.neutron import v2_0 as neutronV20
from neutronclient.neutron.v2_0 import router


PERFECT_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"


class RoutersOnHostingDevice(object):
    resource = 'router'
    resource_plural = '%ss' % resource
    object_path = '/%s' % resource_plural
    resource_path = '/%s/%%s' % resource_plural
    versions = ['2.0']
    allow_names = True


class AddRouterToHostingDevice(RoutersOnHostingDevice,
                               neutronV20.NeutronCommand):
    """Add a router to hosting device."""

    def get_parser(self, prog_name):
        parser = super(AddRouterToHostingDevice, self).get_parser(prog_name)
        parser.add_argument(
            'hosting_device',
            help=_('Name or id of the hosting device.'))
        parser.add_argument(
            'router',
            help=_('Name or id of router to add.'))
        return parser

    def run(self, parsed_args):
        self.log.debug('run(%s)' % parsed_args)
        neutron_client = self.get_client()
        neutron_client.format = parsed_args.request_format
        _id_hd = neutronV20.find_resourceid_by_name_or_id(
            neutron_client, 'hosting_device', parsed_args.hosting_device)
        _id_r = neutronV20.find_resourceid_by_name_or_id(
            neutron_client, 'router', parsed_args.router)
        neutron_client.add_router_to_hosting_device(_id_hd,
                                                    {'router_id': _id_r})
        print(_('Added router \'%(router)s\' to hosting device \'%(hd)s\'') % {
            'router': parsed_args.router, 'hd': parsed_args.hosting_device},
            file=self.app.stdout, end='')
        return [], []


class RemoveRouterFromHostingDevice(RoutersOnHostingDevice,
                                    neutronV20.NeutronCommand):
    """Remove a router from Hosting Device."""

    def get_parser(self, prog_name):
        parser = super(RemoveRouterFromHostingDevice, self).get_parser(
            prog_name)
        parser.add_argument(
            'hosting_device',
            help=_('Name or id of the hosting device.'))
        parser.add_argument(
            'router',
            help=_('Name or id of router to remove.'))
        return parser

    def run(self, parsed_args):
        self.log.debug('run(%s)' % parsed_args)
        neutron_client = self.get_client()
        neutron_client.format = parsed_args.request_format
        _id_hd = neutronV20.find_resourceid_by_name_or_id(
            neutron_client, 'hosting_device', parsed_args.hosting_device)
        _id_r = neutronV20.find_resourceid_by_name_or_id(
            neutron_client, 'router', parsed_args.router)
        neutron_client.remove_router_from_hosting_device(_id_hd, _id_r)
        print(_('Removed router \'%(router)s\' from hosting device \'%(hd)s\'')
              % {'router': parsed_args.router,
                 'hd': parsed_args.hosting_device}, file=self.app.stdout,
              end='')
        return [], []


class ListRoutersOnHostingDevice(RoutersOnHostingDevice,
                                 neutronV20.ListCommand):
    """List the routers on a Hosting Device."""

    _formatters = {'external_gateway_info':
                   router._format_external_gateway_info}
    list_columns = ['id', 'name', 'external_gateway_info']
    unknown_parts_flag = False

    def get_parser(self, prog_name):
        parser = super(ListRoutersOnHostingDevice,
                       self).get_parser(prog_name)
        parser.add_argument(
            'hosting_device',
            help=_('Name or id of the hosting device to query.'))
        return parser

    def call_server(self, neutron_client, search_opts, parsed_args):
        _id = neutronV20.find_resourceid_by_name_or_id(
            neutron_client, 'hosting_device', parsed_args.hosting_device)
        data = neutron_client.list_routers_on_hosting_device(_id,
                                                             **search_opts)
        return data


class HostingDeviceHostingRouter(object):
    resource = 'hosting_device'
    resource_plural = '%ss' % resource
    object_path = '/%s' % resource_plural
    resource_path = '/%s/%%s' % resource_plural
    versions = ['2.0']
    allow_names = True


class ListHostingDeviceHostingRouter(HostingDeviceHostingRouter,
                                     neutronV20.ListCommand):
    """List hosting devices hosting a router."""

    _formatters = {}
    list_columns = ['id', 'name', 'status', 'admin_state_up', 'template_id']
    unknown_parts_flag = False

    def get_parser(self, prog_name):
        parser = super(ListHostingDeviceHostingRouter,
                       self).get_parser(prog_name)
        parser.add_argument('router',
                            help=_('Name or id of router to query.'))
        return parser

    def call_server(self, neutron_client, search_opts, parsed_args):
        _id = neutronV20.find_resourceid_by_name_or_id(
            neutron_client, 'router', parsed_args.router)
        data = neutron_client.list_hosting_devices_hosting_routers(
            _id, **search_opts)
        return data
