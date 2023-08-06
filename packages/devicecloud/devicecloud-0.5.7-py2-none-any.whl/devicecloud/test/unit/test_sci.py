# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2015-2018 Digi International Inc.

import unittest

import httpretty
import mock
import six
import re
import xml.etree.ElementTree as ET

from devicecloud import DeviceCloud
from devicecloud.sci import DeviceTarget, GroupTarget, AsyncRequestProxy, ServerCommandInterfaceAPI
from devicecloud.test.unit.test_utilities import HttpTestBase


EXAMPLE_SCI_DEVICE_NOT_CONNECTED = """\
<sci_reply version="1.0"><reboot><device id="00000000-00000000-00409DFF-FF58175B"><error id="2001"><desc>Device Not Connected</desc></error></device></reboot></sci_reply>
"""

EXAMPLE_SCI_BAD_DEVICE = """\
<sci_reply version="1.0">
  <send_message>
    <device id="00010000-00000000-03599990-42983300">
      <error id="303">
        <desc>Invalid target. Device not found.</desc>
      </error>
    </device>
    <error>Invalid SCI request. No valid targets found.</error>
  </send_message>
</sci_reply>
"""

EXAMPLE_ASYNC_SCI_DEVICE_NOT_CONNECTED = """\
<sci_reply version="1.0"><status>complete</status><reboot><device id="00000000-00000000-00409DFF-FF58175B"><error id="2001"><desc>Device Not Connected</desc></error></device></reboot></sci_reply>
"""

EXAMPLE_ASYNC_SCI_INCOMPLETE = """\
<sci_reply version="1.0"><status>in_progress</status></sci_reply>
"""

EXAMPLE_SCI_REQUEST_PAYLOAD = """\
<rci_request version="1.1">
  <query_state>
    <device_stats/>
  </query_state>
</rci_request>
"""

EXAMPLE_SCI_REQUEST_RESPONSE = """\
<sci_reply version="1.0">
  <send_message>
    <device id="00000000-00000000-00409dff-ffaabbcc">
      <rci_reply version="1.1">
        <query_state>
          <device_stats>
            <firmwarestate>running</firmwarestate>
          </device_stats>
        </query_state>
      </rci_reply>
    </device>
  </send_message>
</sci_reply>
"""

EXAMPLE_ASYNC_SCI_RESPONSE = """\
<sci_reply version="1.0">
  <send_message>
    <jobId>133225503</jobId>
  </send_message>
</sci_reply>
"""

EXAMPLE_UPDATE_FIRMWARE_INVALID_ATTRIBUTE_REQUEST_PAYLOAD = """
<data>aHNxcAbAADUct1cAAACAHEBAAAEABEAwAIBAAQAAACOFFzU</data>
"""

EXAMPLE_UPDATE_FIRMWARE_INVALID_ATTRIBUTE_RESPONSE = """\
<sci_reply version="1.0"><update_firmware><device id="00000000-00000000-00409dff-ffaabbcc"/>
<error><desc>Default target not availabe, specify a target number of filename</desc></error>
</device></update_firmware>
</sci_reply>
"""

class TestSCI(HttpTestBase):
    def _prepare_sci_response(self, response, status=200):
        self.prepare_response("POST", "/ws/sci", response, status)

    def test_sci_successful_error(self):
        self._prepare_sci_response(EXAMPLE_SCI_DEVICE_NOT_CONNECTED)
        self.dc.get_sci_api().send_sci(
            operation="send_message",
            target=DeviceTarget("00000000-00000000-00409DFF-FF58175B"),
            payload="<reset/>")
        self.assertEqual(httpretty.last_request().body,
                         six.b('<sci_request version="1.0">'
                               '<send_message>'
                               '<targets>'
                               '<device id="00000000-00000000-00409DFF-FF58175B"/>'
                               '</targets>'
                               '<reset/>'
                               '</send_message>'
                               '</sci_request>'))

    def test_sci_successful_group_target(self):
        self._prepare_sci_response(EXAMPLE_SCI_DEVICE_NOT_CONNECTED)
        self.dc.get_sci_api().send_sci(
            operation="send_message",
            target=GroupTarget("TestGroup"),
            payload="<reset/>")
        self.assertEqual(httpretty.last_request().body,
                         six.b('<sci_request version="1.0">'
                               '<send_message>'
                               '<targets>'
                               '<group path="TestGroup"/>'
                               '</targets>'
                               '<reset/>'
                               '</send_message>'
                               '</sci_request>'))

    def test_sci_no_parameters(self):
        self._prepare_sci_response(EXAMPLE_SCI_REQUEST_RESPONSE)
        self.dc.get_sci_api().send_sci(
            operation="send_message",
            target=DeviceTarget('00000000-00000000-00409dff-ffaabbcc'),
            payload=EXAMPLE_SCI_REQUEST_PAYLOAD)
        request = httpretty.last_request().body.decode('utf8')
        # Strip white space from lines and concatenate request
        request = ''.join([line.strip() for line in request.splitlines()])
        self.assertEqual(request,
                         six.u('<sci_request version="1.0">'
                               '<send_message>'
                               '<targets>'
                               '<device id="00000000-00000000-00409dff-ffaabbcc"/>'
                               '</targets>'
                               '<rci_request version="1.1">'
                               '<query_state>'
                               '<device_stats/>'
                               '</query_state>'
                               '</rci_request>'
                               '</send_message>'
                               '</sci_request>'))

    def test_sci_with_parameters(self):
        self._prepare_sci_response(EXAMPLE_SCI_REQUEST_RESPONSE)
        self.dc.get_sci_api().send_sci(
            operation="send_message",
            target=DeviceTarget('00000000-00000000-00409dff-ffaabbcc'),
            payload=EXAMPLE_SCI_REQUEST_PAYLOAD,
            reply="all",
            synchronous=True,
            sync_timeout=42,
            cache=False,
            allow_offline=True,
            wait_for_reconnect=True,
            )
        request = httpretty.last_request().body.decode('utf8')
        # Verify attributes exist in <send_message>
        expected_attrib = {
            "reply": "all",
            "synchronous": "true",
            "syncTimeout": "42",
            "cache": "false",
            "allowOffline": "true",
            "waitForReconnect": "true",
        }
        request_e = ET.fromstring(request)
        send_message_e = request_e.find('./send_message')
        self.assertEqual(expected_attrib, send_message_e.attrib)
        # Strip white space from lines and concatenate request
        request = ''.join([line.strip() for line in request.splitlines()])
        # Replace <send_message> from request with one without parameters so the final check can be done
        match = re.search('<send_message.*?>', request)
        request = request[:match.start()] + '<send_message>' + request[match.end():]
        self.assertEqual(request,
                         six.u('<sci_request version="1.0">'
                               '<send_message>'
                               '<targets>'
                               '<device id="00000000-00000000-00409dff-ffaabbcc"/>'
                               '</targets>'
                               '<rci_request version="1.1">'
                               '<query_state>'
                               '<device_stats/>'
                               '</query_state>'
                               '</rci_request>'
                               '</send_message>'
                               '</sci_request>'))

    def test_sci_update_firmware_attribute(self):

        self._prepare_sci_response(EXAMPLE_UPDATE_FIRMWARE_INVALID_ATTRIBUTE_RESPONSE)
        self.dc.get_sci_api().send_sci(
            operation="update_firmware",
            attribute="filename=\"abcd.bin\"",
            target=DeviceTarget('00000000-00000000-00409dff-ffaabbcc'),
            payload=EXAMPLE_UPDATE_FIRMWARE_INVALID_ATTRIBUTE_REQUEST_PAYLOAD)

        request = httpretty.last_request().body.decode('utf8')
        request = ''.join([line.strip() for line in request.splitlines()])
        self.assertEqual(request,
                         six.u('<sci_request version="1.0">'
                               '<update_firmware filename="abcd.bin">'
                               '<targets>'
                               '<device id="00000000-00000000-00409dff-ffaabbcc"/>'
                               '</targets>'
                               '<data>aHNxcAbAADUct1cAAACAHEBAAAEABEAwAIBAAQAAACOFFzU</data>'
                               '</update_firmware>'
                               '</sci_request>'))


class TestGetAsync(HttpTestBase):
    def test_sci_get_async(self):
        self.prepare_response("GET", "/ws/sci/123", EXAMPLE_ASYNC_SCI_DEVICE_NOT_CONNECTED, 200)
        resp = self.dc.get_sci_api().get_async_job(123)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content, six.b(EXAMPLE_ASYNC_SCI_DEVICE_NOT_CONNECTED))


class TestAsyncProxy(HttpTestBase):
    def setUp(self):
        HttpTestBase.setUp(self)
        self.fake_conn = mock.MagicMock()

    def test_ctor(self):
        t = AsyncRequestProxy(123, self.fake_conn)
        self.assertEqual(t.job_id, 123)
        self.assertIs(t.response, None)

    def test_completed_false(self):
        self.prepare_response("GET", "/ws/sci/123", EXAMPLE_ASYNC_SCI_INCOMPLETE, 200)
        t = AsyncRequestProxy(123, self.dc.get_sci_api()._conn)
        self.assertIs(t.completed, False)
        self.assertIs(t.response, None)

    def test_completed_true(self):
        self.prepare_response("GET", "/ws/sci/123", EXAMPLE_ASYNC_SCI_DEVICE_NOT_CONNECTED, 200)
        t = AsyncRequestProxy(123, self.dc.get_sci_api()._conn)
        self.assertIs(t.completed, True)
        self.assertEqual(t.response, six.b(EXAMPLE_ASYNC_SCI_DEVICE_NOT_CONNECTED))

    def test_completed_already(self):
        self.prepare_response("GET", "/ws/sci/123", EXAMPLE_ASYNC_SCI_DEVICE_NOT_CONNECTED, 200)
        t = AsyncRequestProxy(123, self.dc.get_sci_api()._conn)
        t.response = EXAMPLE_ASYNC_SCI_DEVICE_NOT_CONNECTED
        self.assertIs(t.completed, True)


class TestSendSciAsync(HttpTestBase):
    @mock.patch.object(ServerCommandInterfaceAPI, "send_sci")
    def test_bad_resp(self, fake_send_sci):
        fake_resp = mock.MagicMock()
        fake_resp.status_code = 400
        fake_resp.reason = "OK"
        fake_resp.content = EXAMPLE_SCI_BAD_DEVICE
        fake_send_sci.return_value = fake_resp
        resp = self.dc.get_sci_api().send_sci_async("send_message", DeviceTarget('00000000-00000000-00409dff-ffaabbcc'), EXAMPLE_SCI_REQUEST_PAYLOAD)
        self.assertIs(resp, None)

    @mock.patch.object(ServerCommandInterfaceAPI, "send_sci")
    def test_resp_parse(self, fake_send_sci):
        fake_resp = mock.MagicMock()
        fake_resp.status_code = 200
        fake_resp.reason = "OK"
        fake_resp.content = EXAMPLE_ASYNC_SCI_RESPONSE
        fake_send_sci.return_value = fake_resp
        resp = self.dc.get_sci_api().send_sci_async("send_message", DeviceTarget('00000000-00000000-00409dff-ffaabbcc'), EXAMPLE_SCI_REQUEST_PAYLOAD)
        self.assertEqual(resp.job_id, 133225503)


if __name__ == "__main__":
    unittest.main()
