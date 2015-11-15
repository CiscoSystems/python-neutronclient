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

from neutronclient.i18n import _
from neutronclient.neutron import v2_0 as neutronV20


class HostingDeviceHandledByConfigAgent(object):
    resource = 'hosting_device'
    resource_plural = '%ss' % resource
    object_path = '/dev_mgr/%s' % resource_plural
    resource_path = '/dev_mgr/%s/%%s' % resource_plural
    versions = ['2.0']
    allow_names = True


class HostingDeviceAssociateWithConfigAgent(HostingDeviceHandledByConfigAgent,
                                            neutronV20.NeutronCommand):

    def get_parser(self, prog_name):
        parser = super(HostingDeviceAssociateWithConfigAgent, self).get_parser(
            prog_name)
        parser.add_argument(
            'config_agent_id',
            help=_('Id of the Cisco configuration agent.'))
        parser.add_argument(
            'hosting_device',
            help=_('Name or id of hosting device to associate.'))
        return parser

    def run(self, parsed_args):
        self.log.debug('run(%s)' % parsed_args)
        neutron_client = self.get_client()
        neutron_client.format = parsed_args.request_format
        _id_hd = neutronV20.find_resourceid_by_name_or_id(
            neutron_client, 'hosting_device', parsed_args.hosting_device)
        neutron_client.associate_hosting_device_with_config_agent(
            parsed_args.config_agent_id, {'hosting_device_id': _id_hd})
        print(_('Associated hosting device \'%(hd)s\' with Cisco '
                'configuration agent \'%(agent)s\'') % {
            'hd': parsed_args.hosting_device,
            'agent': parsed_args.config_agent_id}, file=self.app.stdout,
            end='')
        return [], []


class HostingDeviceDisassociateFromConfigAgent(
        HostingDeviceHandledByConfigAgent, neutronV20.NeutronCommand):

    def get_parser(self, prog_name):
        parser = super(HostingDeviceDisassociateFromConfigAgent,
                       self).get_parser(prog_name)
        parser.add_argument(
            'config_agent_id',
            help=_('Id of the Cisco configuration agent.'))
        parser.add_argument(
            'hosting_device',
            help=_('Name or id of hosting device to disassociate.'))
        return parser

    def run(self, parsed_args):
        self.log.debug('run(%s)' % parsed_args)
        neutron_client = self.get_client()
        neutron_client.format = parsed_args.request_format
        _id_hd = neutronV20.find_resourceid_by_name_or_id(
            neutron_client, 'hosting_device', parsed_args.hosting_device)
        neutron_client.disassociate_hosting_device_with_config_agent(
            parsed_args.config_agent_id, _id_hd)
        print(_('Disassociated hosting device \'%(hd)s\' from Cisco '
                'configuration agent \'%(agent)s\'') % {
            'hd': parsed_args.hosting_device,
            'agent': parsed_args.config_agent_id}, file=self.app.stdout,
            end='')
        return [], []


class HostingDeviceHandledByConfigAgentList(HostingDeviceHandledByConfigAgent,
                                            neutronV20.ListCommand):
    list_columns = ['id', 'name', 'admin_state_up', 'template_id']

    def get_parser(self, prog_name):
        parser = super(HostingDeviceHandledByConfigAgentList,
                       self).get_parser(prog_name)
        parser.add_argument(
            'config_agent_id',
            help=_('Id of the Cisco configuration agent to query.'))
        return parser

    def call_server(self, neutron_client, search_opts, parsed_args):
        data = neutron_client.list_hosting_device_handled_by_config_agent(
            parsed_args.config_agent_id, **search_opts)
        return data


class ConfigAgentHandlingHostingDevice(object):
    resource = 'agent'
    resource_plural = '%ss' % resource
    object_path = '/%s' % resource_plural
    resource_path = '/%s/%%s' % resource_plural
    versions = ['2.0']
    allow_names = True


class ConfigAgentHandlingHostingDeviceList(ConfigAgentHandlingHostingDevice,
                                           neutronV20.ListCommand):

    list_columns = ['id', 'alive', 'agent_type', 'admin_state_up', 'host']

    def extend_list(self, data, parsed_args):
        for agent in data:
            agent['alive'] = ":-)" if agent.get('alive') else 'xxx'

    def get_parser(self, prog_name):
        parser = super(ConfigAgentHandlingHostingDeviceList, self).get_parser(
            prog_name)
        parser.add_argument('hosting_device',
                            help=_('Name or id of hosting device to query.'))
        return parser

    def call_server(self, neutron_client, search_opts, parsed_args):
        _id = neutronV20.find_resourceid_by_name_or_id(
            neutron_client, 'hosting_device', parsed_args.hosting_device)
        data = neutron_client.list_config_agents_handling_hosting_device(
            _id, **search_opts)
        return data
