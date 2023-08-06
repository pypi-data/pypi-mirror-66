import unittest
from unittest.mock import MagicMock, patch
from tests.util import MockSelection
from eduvpn.actions.add import new_provider
from eduvpn.actions.delete import delete_profile
from eduvpn.actions.select import select_profile
from eduvpn.actions.vpn_status import vpn_change
from eduvpn.metadata import Metadata
from eduvpn.util import have_dbus_notification_service


class MockBuilder:
    def __init__(self):
        self.objects = {
            'provider-selection': MockSelection(4),
        }

    def get_object(self, o):
        return self.objects.get(o, MagicMock())


class TestActions(unittest.TestCase):
    uuid = 'test'

    @classmethod
    def setUpClass(cls):
        cls.meta = Metadata()
        cls.meta.uuid = cls.uuid

        cls.builder = MockBuilder()
        cls.verifier = MagicMock()

    @patch('gi.repository.Gtk.MessageDialog')
    def test_delete_profile(self, _):
        delete_profile(builder=self.builder, lets_connect=False)

    def test_select_profile(self):
        select_profile(builder=self.builder, verifier=self.verifier, lets_connect=False)

    def test_new_provider(self):
        new_provider(builder=self.builder, verifier=self.verifier,
                     institute_access_uri="bla",
                     secure_internet_uri="bla", lets_connect=False)

    @unittest.skipUnless(have_dbus_notification_service(), "DBus notification service not available")
    def test_vpn_change(self):
        vpn_change(builder=self.builder, lets_connect=False)
