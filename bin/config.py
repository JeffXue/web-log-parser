# -*- coding:utf-8 -*-
import ConfigParser


class Config:
    """get config from the ini file"""

    def __init__(self, config_file):
        all_config = ConfigParser.ConfigParser()
        with open(config_file, 'r') as cfg_file:
            all_config.readfp(cfg_file)

        self.goaccess_flag = int(all_config.get('common', 'goaccess_flag'))
        self.time_format = all_config.get('common', 'time-format')
        self.date_format = all_config.get('common', 'date-format')
        self.log_format = all_config.get('common', 'log-format')
        self.log_pattern = all_config.get('common', 'log-pattern')
        self.goaccess_log_format = all_config.get('common', 'goaccess-log-format')
        self.static_file = all_config.get('common', 'static-file').split(',')
        self.is_with_parameters = int(all_config.get('common', 'is_with_parameters'))
        self.fixed_parameter_keys = all_config.get('common', 'fixed_parameter_keys').split(',')
        self.custom_parameters_list = all_config.get('common', 'custom_parameters').split(',')
        self.urls_most_number = int(all_config.get('common', 'urls_most_number'))
        self.ignore_urls = all_config.get('common', 'ignore_urls').split(',')

        self.custom_keys = []
        self.custom_parameters = {}
        for item in self.custom_parameters_list:
            key = item.split('=')[0]
            if len(item.split('=')) == 2:
                value = item.split('=')[1]
            else:
                value = ''
            self.custom_parameters.setdefault(key, value)
            self.custom_keys.append(key)

        self.second_line_flag = int(all_config.get('common', 'second_line_flag'))
        self.support_method = all_config.get('common', 'support_method').split(',')

config = Config('../conf/config.ini')
