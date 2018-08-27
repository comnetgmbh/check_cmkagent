#!/usr/bin/python

import sys

#TODO Subclasses should be put in separate files
#from modules import *

class Check_checkmk():
    '''
        Base class for all checks
    '''
    subclasses = {}

    @classmethod
    def register_subclass(cls, check_type):
        '''
            Register a new subclass
            Called by register_check()
        '''
        def decorator(subclass):
            cls.subclasses[check_type] = subclass
            return subclass

        return decorator


    @classmethod
    def check(cls, check_type, columns, argument, params):
        '''
            Register a new check
        '''
        if check_type not in cls.subclasses:
            raise ValueError('Check type not defined')

        return cls.subclasses[check_type](columns, argument, params)


    def __init__(self, columns, argument, params):
        self.columns = columns
        self.argument = argument
        self.params = params
        self.perfdata = []
        self.status = 0
        try:
            self.do_check()
        except AttributeError:
            raise NotImplementedError('do_check is not implemented')


    def return_status(self):
        if self.status in range(0, 4):
            sys.exit(self.status)
        raise ValueError('Invalid status code')


    def plugin_output(self, text):
        perfdata_text = []
        for metric, value, warn, crit, minimum, maximum in self.perfdata:
            perfdata_text.append('{0}={1},{2},{3},{4},{5}'.format(metric, value, warn, crit, minimum, maximum))
        print('{0} | {1}'.format(text, ' '.join(perfdata_text)))


    def append_to_perfdata(self, value_tuple):
        if len(value_tuple) < 2 or len(value_tuple) > 6:
            raise ValueError('Invalid format for performance data')
        value_list = [str(value_tuple[0])]
        for value in value_tuple[1:]:
            if type(value) not in [float, int]:
                print value_tuple
                raise ValueError('Invalid value given as performance value')
            value_list.append(value)
        self.perfdata.append(tuple(value_list))


    def ok(self):
        self.status = max(0, self.status)


    def warn(self):
        self.status = max(1, self.status)


    def crit(self):
        self.status = 2


    def unknown(self):
        if self.status != 2:
            self.status = 3
        pass



@Check_checkmk.register_subclass('Check_df')
class Check_df(Check_checkmk):

    def parse_data(self):
        parsed_data = []
        is_inodes = False
        for line in self.columns:
            if '[df_inodes_start]' in line:
                is_inodes = True
            elif '[df_inodes_end]' in line:
                is_inodes = False
            if not is_inodes and line[-1] == self.argument:
                parsed_data = line
        return parsed_data


    def do_check(self):
        def calc_unit(value):
            value = float(value)
            units = ['KB', 'MB', 'GB', 'TB', 'PB']
            unit_index = 0
            while value > 1024 and unit_index < 4:
                value = value / 1024
                unit_index += 1
            return '{:.2f} {}'.format(value, units[unit_index])

        warnv, critv = map(float, self.params)
        device, filesystem, size, used, avail, perc, mountpoint = self.parse_data()
        usage_perc = float(used) / float(size) * 100

        if usage_perc >= critv:
            self.crit()
        elif usage_perc >= warnv:
            self.warn()
        perfdata = ('fs_used', usage_perc, warnv, critv, 0, 100)
        self.append_to_perfdata(perfdata)
        self.plugin_output('{:.2f}% used ({} of {})'.format(usage_perc, calc_unit(used), calc_unit(size)))
        self.return_status()
