from collections import OrderedDict
from logging import Formatter
from json import dumps


class JSONFormatter(Formatter):
    def __init__(self, record_fields=['levelname', 'asctime'], datefmt=None, customjson=None):
        Formatter.__init__(self, None, datefmt)
        self.record_fields = record_fields
        self.customjson = customjson

    def usesTime(self):
        return 'asctime' in self.record_fields

    def format_time(self, record):
        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)

    def get_json_data(self, record):
        if len(self.record_fields) > 0:
            fields = []
            for x in self.record_fields:
                try:
                    fields.append((x, getattr(record, x)))
                except AttributeError as e:
                    print(e)
                    break
            fields.append(('msg', record.msg))
            # An OrderedDict is used to ensure that the converted data appears in the same order for every record
            return OrderedDict(fields)
        else:
            return record.msg

    def format(self, record):
        self.format_time(record)
        json_data = self.get_json_data(record)
        formatted_json = dumps(json_data, cls=self.customjson, sort_keys=True,
                               separators=(',', ': '), indent=4)
        return formatted_json
