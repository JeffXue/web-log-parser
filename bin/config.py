# -*- coding:utf-8 -*-
__author__ = 'xuekj'
import ConfigParser


class Config():
    """get config from the ini file"""

    def __init__(self, config_file):
        common_config = ConfigParser.ConfigParser()
        with open(config_file, 'r') as cfg_file:
            common_config.readfp(cfg_file)

        self.goaccess_flag = int(common_config.get('Common', 'goaccess_flag'))
        self.time_format = common_config.get('Common', 'time-format')
        self.date_format = common_config.get('Common', 'date-format')
        self.log_format = common_config.get('Common', 'log-format')
        self.static_file = common_config.get('Common', 'static-file').split(',')

config = Config('../conf/Config.ini')