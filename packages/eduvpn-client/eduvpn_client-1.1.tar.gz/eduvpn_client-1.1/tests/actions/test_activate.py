import unittest
from unittest.mock import MagicMock, patch
from tests.util import MockBuilder
from eduvpn.actions.activate import activate_connection
from eduvpn.metadata import Metadata
from eduvpn.util import have_dbus_notification_service


class TestActions(unittest.TestCase):
    uuid = 'test'

    @classmethod
    def setUpClass(cls):
        cls.meta = Metadata()
        cls.meta.uuid = cls.uuid

        cls.builder = MockBuilder()
        cls.verifier = MagicMock()

    @patch('gi.repository.Gtk.MessageDialog')
    @patch('eduvpn.actions.activate.connect_provider')
    @unittest.skipUnless(have_dbus_notification_service(), "DBus notification service not available")
    def test_activate_connection(self, *args):
        activate_connection(builder=self.builder, meta=self.meta, verifier=self.verifier, lets_connect=False)
