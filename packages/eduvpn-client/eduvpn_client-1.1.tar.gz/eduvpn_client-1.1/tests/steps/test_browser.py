from unittest import TestCase, skip
from unittest.mock import MagicMock, patch
from tests.util import MockBuilder, MockOAuth, MockResponse, MockDialog
from eduvpn.metadata import Metadata
from eduvpn.steps.browser import browser_step, _phase1_background, _phase1_callback, _phase2_background,\
    _phase2_callback, _show_dialog


class TestSteps(TestCase):
    uuid = 'test'

    @classmethod
    def setUpClass(cls):
        cls.meta = Metadata()
        cls.meta.uuid = cls.uuid
        cls.meta.api_base_uri = "test_url"
        cls.meta.token = {'token_endpoint': 'https://test'}
        cls.meta.api_base_uri = 'https://test'
        cls.meta.instance_base_uri = 'https://test'
        cls.builder = MockBuilder()
        cls.verifier = MagicMock()
        cls.oauth = MockOAuth()
        cls.dialog = MockDialog()

    def phase1_sideeffect(self, url):
        if url == self.meta.api_base_uri + '/info.json':
            return MockResponse()
        elif url == self.meta.api_base_uri + '/info.json.sig':
            return MockResponse('ABCDEFG')
        else:
            raise Exception

    @patch('eduvpn.steps.browser.thread_helper')
    def test_browser_step(self, *_):
        browser_step(builder=self.builder, meta=self.meta, verifier=self.verifier, lets_connect=False)

    @patch('requests.get')
    def test_phase1_background(self, mock_get):
        mock_get.get.side_effect = self.phase1_sideeffect
        _phase1_background(builder=self.builder, meta=self.meta, verifier=self.verifier, dialog=self.dialog,
                           force_token_refresh=True, lets_connect=False)
        _phase1_background(builder=self.builder, meta=self.meta, verifier=self.verifier, dialog=self.dialog,
                           force_token_refresh=False, lets_connect=False)

    @patch('eduvpn.steps.browser.thread_helper')
    def test_phase1_callback(self, _):
        _phase1_callback(builder=self.builder, meta=self.meta, auth_url=None, dialog=self.dialog, code_verifier=None,
                         oauth=self.oauth, port=1, state="1234", lets_connect=False)

    @patch('webbrowser.open')
    @patch('eduvpn.steps.browser.get_oauth_token_code', side_effect=lambda x, lets_connect, timeout: ("code", "state"))
    def test_phase2_background(self, *args):
        _phase2_background(builder=self.builder, meta=self.meta, auth_url=None, dialog=self.dialog, code_verifier=None,
                           oauth=self.oauth, port=1, state="state", lets_connect=False)

    @patch('webbrowser.open')
    @patch('eduvpn.steps.browser.get_oauth_token_code', side_effect=lambda x: ("code", "state"))
    def test_phase2_background_wrong_state(self, *args):
        with self.assertRaises(Exception):
            _phase2_background(builder=self.builder, meta=self.meta, auth_url=None, dialog=self.dialog,
                               code_verifier=None, oauth=self.oauth, port=1, state="wrongstate", lets_connect=False)

    @patch('eduvpn.steps.browser.fetch_profile_step')
    def test_phase2_callback(self, *_):
        _phase2_callback(builder=self.builder, meta=self.meta, dialog=self.dialog, oauth=self.oauth, lets_connect=False)

    def test_show_dialog(self):
        _show_dialog(builder=self.builder, auth_url=None, dialog=self.dialog)

