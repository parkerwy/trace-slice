import unittest
import slice


class TestDetectEventType(unittest.TestCase):
    def test_log_entry_with_HKT(self):
        type = slice.detect_event_type(
            """[10/19/15 22:47:54:792 HKT] 00000045 wle_outbnd_ws 1 com.ibm.bpm.ws.jaxws.connector.SOAPConnector setConfiguration setConfiguration(), connectorConfig = <config type="com.lombardisoftware.client.persistence.SOAPConnectorConfiguration">""")
        self.assertEqual(slice.EVENT_LOG_ENTRY, type)

    def test_log_entry_with_GMT(self):
        type = slice.detect_event_type(
            """[1/12/17 3:00:01:905 GMT] 00000e5a WICleanupHTM  I   CWTKE0101I: A work item cleanup has been started, the daemon will next run at 'Fri 2017-01-13 03:00:00.879'.""")
        self.assertEqual(slice.EVENT_LOG_ENTRY, type)

    def test_additional_message(self):
        type = slice.detect_event_type(
            """Caused by: com.lombardisoftware.core.TeamWorksRuntimeException: Java Class org.mozilla.javascript.Undefined is not registered as supported class for the SymbolTable""")
        self.assertEqual(slice.EVENT_ADDITIONAL_MESSAGE, type)

    def test_start_display_environment(self):
        type = slice.detect_event_type("""************ Start Display Current Environment ************""")
        self.assertEqual(slice.EVENT_START_DISPLAY_ENVIRONMENT, type)

    def test_end_display_environment(self):
        type = slice.detect_event_type("""************* End Display Current Environment *************""")
        self.assertEqual(slice.EVENT_END_DISPLAY_ENVIRONMENT, type)


class TestGetEventTime(unittest.TestCase):
    def test_get_event_time_with_HKT(self):
        eventtime, thread, logger, level = slice.get_event_detail(
            """[10/19/15 22:47:54:792 HKT] 00000045 wle_outbnd_ws 1 com.ibm.bpm.ws.jaxws.connector.SOAPConnector setConfiguration setConfiguration(), connectorConfig = <config type="com.lombardisoftware.client.persistence.SOAPConnectorConfiguration">""")
        print eventtime

    def test_test_event_time_with_GMT(self):
        eventtime, thread, logger, level = slice.get_event_detail(
            """[1/12/17 3:00:01:905 GMT] 00000e5a WICleanupHTM  I   CWTKE0101I: A work item cleanup has been started, the daemon will next run at 'Fri 2017-01-13 03:00:00.879'.""")
        print eventtime


class TestSlice(unittest.TestCase):
    def test_slice_one_file(self):
        slice.slice(['data/trace.log'])

    def test_slice_multiple_files(self):
        files = ['data/trace_17.01.13_02.36.58.log', 'data/trace_17.01.13_02.37.58.log',
                 'data/trace_17.01.13_02.37.59.log', 'data/trace_17.01.13_02.43.17.log',
                 'data/trace_17.01.13_02.43.33.log', 'data/trace.log']
        slice.slice(files)


if __name__ == '__main__':
    unittest.main()
