#!/usr/bin/python
import os.path
import re
import sys
from datetime import datetime

EVENT_START_DISPLAY_ENVIRONMENT = 0
EVENT_END_DISPLAY_ENVIRONMENT = 1
EVENT_LOG_ENTRY = 3
EVENT_ADDITIONAL_MESSAGE = 4

log_entry_pattern = re.compile(r'^\[([0-9/]* [0-9:]*) [A-Z]{3}\] (.{8}) (.{13}) (.)')


def detect_event_type(line):
    if log_entry_pattern.match(line):
        return EVENT_LOG_ENTRY
    elif line.strip() == '************ Start Display Current Environment ************':
        return EVENT_START_DISPLAY_ENVIRONMENT
    elif line.strip() == '************* End Display Current Environment *************':
        return EVENT_END_DISPLAY_ENVIRONMENT

    return EVENT_ADDITIONAL_MESSAGE


def get_event_detail(line):
    match = log_entry_pattern.match(line)
    timestring = match.group(1)
    eventtime = datetime.strptime(timestring, '%m/%d/%y %H:%M:%S:%f')

    thread = match.group(2)
    logger = match.group(3)
    level = match.group(4)

    return eventtime, thread, logger, level


def slice(traces):
    indexfile = "trace-slice-index.txt"
    sliceprefix = "trace-slice-"

    is_display_environment = False
    lastthread = ''
    threads = {}
    for trace in traces:
        print "processing " + trace + " ......"
        with open(trace) as tracefile:
            for line in tracefile:
                type = detect_event_type(line)
                if type is EVENT_LOG_ENTRY:
                    eventtime, thread, logger, level = get_event_detail(line)
                    slicefile = threads.get(thread)
                    if slicefile is None:
                        dirname = os.path.dirname(trace)
                        slicefile = open(dirname + '/' + sliceprefix + thread + '.log', 'w')
                        threads.update({thread: slicefile})
                    slicefile.write(line)
                    lastthread = thread
                elif type is EVENT_ADDITIONAL_MESSAGE:
                    if not is_display_environment:
                        slicefile = threads.get(lastthread)
                        slicefile.write(line)
                elif type is EVENT_START_DISPLAY_ENVIRONMENT:
                    is_display_environment = True
                elif type is EVENT_END_DISPLAY_ENVIRONMENT:
                    is_display_environment = False
                else:
                    raise ValueError('Unkown event type ' + str(type))

    for thread, slicefile in threads.iteritems():
        slicefile.close()


def print_usage():
    print "Usage: trace-slicer TRACE_FILE..."


def main():
    if len(sys.argv) > 1:
        files = sys.argv[1:]
        slice(files)
    else:
        print_usage()


if __name__ == "__main__":
    main()
