# -*- coding:utf-8 -*-
__author__ = 'xuekj'
import ConfigParser


class Config():
    """get config from the ini file"""

    def __init__(self, config_file):
        all_config = ConfigParser.ConfigParser()
        with open(config_file, 'r') as cfg_file:
            all_config.readfp(cfg_file)

        self.goaccess_flag = int(all_config.get('Common', 'goaccess_flag'))
        self.time_format = all_config.get('Common', 'time-format')
        self.date_format = all_config.get('Common', 'date-format')
        self.log_format = all_config.get('Common', 'log-format')
        self.static_file = all_config.get('Common', 'static-file').split(',')
        self.is_with_parameters = int(all_config.get('Common', 'is_with_parameters'))
        self.special_parameter_keys = all_config.get('Common', 'special_parameter_keys').split(',')

config = Config('../conf/Config.ini')
