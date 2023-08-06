"""
sentry-syslog tests for integrating with Sentry to send events and breadcrumbs.
"""

import pathlib
import tempfile
import unittest
from unittest import mock

import syslog_rfc5424_parser

import sentrysyslog
from .. import tests


class SentrySyslogSentryTests(unittest.TestCase):
    """
    sentry-syslog tests for integrating with Sentry to send events and breadcrumbs.
    """

    @mock.patch("sentry_sdk.transport.HttpTransport.capture_event")
    def test_sentry_integration(self, capture_event):
        """
        The main function initializes the integration and sends events and breadcrumbs.
        """
        breadcrumb_syslog_msg = syslog_rfc5424_parser.SyslogMessage.parse(
            tests.SYSLOG_INFO_LINES.split("\n", 1)[0]
        )
        event_syslog_msg = syslog_rfc5424_parser.SyslogMessage.parse(
            tests.SYSLOG_ALERT_LINES.split("\n", 1)[0]
        )

        with tempfile.NamedTemporaryFile("w+") as input_file:
            input_file.write(tests.SYSLOG_INFO_LINES)
            input_file.write(tests.SYSLOG_ALERT_LINES)
            input_file.seek(0)
            self.addCleanup(tests.cleanupBreadcrumbs)
            sentrysyslog.main(
                args=["--input-file={}".format(input_file.name), tests.DSN_VALUE]
            )

        capture_event.assert_called_once()
        processed_event = capture_event.call_args[0][0]

        self.assertEqual(
            processed_event["platform"], "syslog", "Wrong captured event logger"
        )
        self.assertEqual(
            processed_event["server_name"],
            event_syslog_msg.hostname,
            "Wrong captured event hostname",
        )
        self.assertEqual(
            processed_event["level"], "fatal", "Wrong captured event level"
        )
        self.assertEqual(
            processed_event["logger"],
            "{}.{}".format(event_syslog_msg.facility.name, event_syslog_msg.appname),
            "Wrong captured event logger",
        )
        self.assertEqual(
            processed_event["logentry"]["message"],
            event_syslog_msg.msg,
            "Wrong captured event message",
        )

        self.assertNotIn(
            "contexts",
            processed_event,
            "Captured event includes Python integration runtime context",
        )
        self.assertNotIn(
            "modules",
            processed_event,
            "Captured event includes Python integration modules",
        )
        self.assertNotIn(
            "sys.argv",
            processed_event["extra"],
            "Captured event includes Python integration argv",
        )

        self.assertIn(
            "breadcrumbs", processed_event, "Captured event missing breadcrumbs"
        )
        self.assertEqual(
            len(processed_event["breadcrumbs"]),
            1,
            "Wrong number of captured event breadcrumbs",
        )
        processed_breadcrumb = processed_event["breadcrumbs"][0]
        self.assertEqual(
            processed_breadcrumb["level"],
            breadcrumb_syslog_msg.severity.name,
            "Wrong captured event breadcrumb level",
        )
        self.assertEqual(
            processed_breadcrumb["category"],
            "{}.{}".format(
                breadcrumb_syslog_msg.facility.name, breadcrumb_syslog_msg.appname
            ),
            "Wrong captured event breadcrumb category",
        )
        self.assertEqual(
            processed_breadcrumb["message"],
            breadcrumb_syslog_msg.msg,
            "Wrong captured event breadcrumb message",
        )
        self.assertIn(
            "data",
            processed_breadcrumb,
            "Captured event breadcrumb missing log record arguments",
        )
        self.assertIn(
            "hostname",
            processed_breadcrumb["data"],
            "Captured event breadcrumb missing log record arguments key",
        )
        self.assertEqual(
            processed_breadcrumb["data"]["hostname"],
            breadcrumb_syslog_msg.hostname,
            "Wrong captured event breadcrumb missing log record arguments value",
        )

    @mock.patch("sentry_sdk.transport.HttpTransport.capture_event")
    def test_invalid_syslog_messages(self, capture_event):
        """
        Syslog messages that can't be parsed are captured as Sentry exception events.
        """
        with open(pathlib.Path(__file__).parent / "invalid.syslog.log") as input_file:
            self.addCleanup(tests.cleanupBreadcrumbs)
            sentrysyslog.main(
                args=["--input-file={}".format(input_file.name), tests.DSN_VALUE]
            )

        capture_event.assert_called()
        self.assertEqual(
            capture_event.call_count,
            len(tests.SYSLOG_INVALID_LINES[:-1].split("\n")),
            "Wrong number of events captured for invalid syslog lines",
        )
        processed_event = capture_event.call_args[0][0]
        self.assertIn(
            "exception",
            processed_event,
            "Internal exception not included in captured event",
        )
