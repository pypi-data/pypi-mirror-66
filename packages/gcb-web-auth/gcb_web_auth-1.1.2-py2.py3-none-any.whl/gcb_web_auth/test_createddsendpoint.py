from django.test import TestCase
from gcb_web_auth.management.commands.createddsendpoint import Command


class CreateDDSEndpointTestCase(TestCase):
    def test_createddsentpoint_handle(self):
        cmd = Command()
        cmd.handle(name='a', api_root='b', portal_root='c', agent_key='d', openid_provider_id='e',
                   openid_provider_service_id='f')
        cmd.handle(name='a', api_root='b', portal_root='c', agent_key='d', openid_provider_id='e',
                   openid_provider_service_id='f')
