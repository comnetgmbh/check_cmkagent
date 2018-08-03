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
    def check(cls, check_type, columns, params):
        '''
            Register a new check
        '''
        if check_type not in cls.subclasses:
            raise ValueError('Check type not defined')

        return cls.subclasses[check_type](columns, params)


    def __init__(self, columns, params):
        self.columns = columns
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
                raise ValueError('Invalid value given as performance value')
            value_list.append(value)
        self.perfdata.append(tuple(value_list))


    def ok(self):
        self.status = max(0, self.status)


    def warn(self):
        self.status = max(1, self.status)


    def crit(self):
        self.status = max(2, self.status)


    def unknown(self):
        if self.status != 2:
            self.status = 3
        pass



@Check_checkmk.register_subclass('Check_df')
class Check_df(Check_checkmk):

    def do_check(self):
        warnv, critv = self.params
        self.status = 0
        value = int(self.columns[0])
        if value >= critv:
            self.crit()
        elif value >= warnv:
            self.warn()
        perfdata = ('test', value, warnv, critv, 0, 100)
        self.append_to_perfdata(perfdata)
        self.plugin_output('Value: {}'.format(value))
        self.return_status()
