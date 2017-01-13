import os
import shutil
import tempfile
import unittest

import traceslice


class TestDetectEventType(unittest.TestCase):
    def test_log_entry_with_HKT(self):
        type = traceslice.detect_event_type(
            """[10/19/15 22:47:54:792 HKT] 00000045 wle_outbnd_ws 1 com.ibm.bpm.ws.jaxws.connector.SOAPConnector setConfiguration setConfiguration(), connectorConfig = <config type="com.lombardisoftware.client.persistence.SOAPConnectorConfiguration">""")
        self.assertEqual(traceslice.EVENT_LOG_ENTRY, type)

    def test_log_entry_with_GMT(self):
        type = traceslice.detect_event_type(
            """[1/12/17 3:00:01:905 GMT] 00000e5a WICleanupHTM  I   CWTKE0101I: A work item cleanup has been started, the daemon will next run at 'Fri 2017-01-13 03:00:00.879'.""")
        self.assertEqual(traceslice.EVENT_LOG_ENTRY, type)

    def test_additional_message(self):
        type = traceslice.detect_event_type(
            """Caused by: com.lombardisoftware.core.TeamWorksRuntimeException: Java Class org.mozilla.javascript.Undefined is not registered as supported class for the SymbolTable""")
        self.assertEqual(traceslice.EVENT_ADDITIONAL_MESSAGE, type)

    def test_start_display_environment(self):
        type = traceslice.detect_event_type("""************ Start Display Current Environment ************""")
        self.assertEqual(traceslice.EVENT_START_DISPLAY_ENVIRONMENT, type)

    def test_end_display_environment(self):
        type = traceslice.detect_event_type("""************* End Display Current Environment *************""")
        self.assertEqual(traceslice.EVENT_END_DISPLAY_ENVIRONMENT, type)


class TestGetEventTime(unittest.TestCase):
    def test_get_event_time_with_HKT(self):
        eventtime, thread, logger, level = traceslice.get_event_detail(
            """[10/19/15 22:47:54:792 HKT] 00000045 wle_outbnd_ws 1 com.ibm.bpm.ws.jaxws.connector.SOAPConnector setConfiguration setConfiguration(), connectorConfig = <config type="com.lombardisoftware.client.persistence.SOAPConnectorConfiguration">""")
        print(eventtime)

    def test_test_event_time_with_GMT(self):
        eventtime, thread, logger, level = traceslice.get_event_detail(
            """[1/12/17 3:00:01:905 GMT] 00000e5a WICleanupHTM  I   CWTKE0101I: A work item cleanup has been started, the daemon will next run at 'Fri 2017-01-13 03:00:00.879'.""")
        print(eventtime)


class TestSlice(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()
        print('using temporary dir ' + self.test_dir)
        for trace in os.listdir('data'):
            shutil.copy2('data/' + trace, self.test_dir)

    def tearDown(self):
        # Remove the directory after the test
        print(os.listdir(self.test_dir))
        shutil.rmtree(self.test_dir)
        print('temporary dir deleted.')

    def test_slice_one_file(self):
        traceslice.slice([self.test_dir + '/trace.log'])

    def test_slice_multiple_files(self):
        files = [self.test_dir + '/trace_17.01.13_02.36.58.log', self.test_dir + '/trace_17.01.13_02.37.58.log',
                 self.test_dir + '/trace_17.01.13_02.37.59.log', self.test_dir + '/trace_17.01.13_02.43.17.log',
                 self.test_dir + '/trace_17.01.13_02.43.33.log', self.test_dir + '/trace.log']
        traceslice.slice(files)


if __name__ == '__main__':
    unittest.main()
