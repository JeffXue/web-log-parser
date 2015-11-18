# -*- coding:utf-8 -*-
__author__ = 'xuekj'
import datetime
import os
from collections import Counter

from util import get_dir_files
from config import config
from report import generate_web_log_parser_report
from report import generate_web_log_parser_urls
from report import update_index_html


class URLData():

    def __init__(self, url=None, pv=None, ratio=None, peak=None):
        self.url = url
        self.pv = pv
        self.ratio = ratio
        self.peak = peak
        self.time = []


def parse_log_format():
    log_format_index = {}
    log_format_list = config.log_format.split()
    for item in log_format_list:
        if item.find(r'%h') != -1:
            log_format_index.setdefault('host_index', log_format_list.index(item))
        if item.find(r'%d') != -1 and item.find(r'%t') != -1:
            log_format_index.setdefault('time_index', log_format_list.index(item))
        if item.find(r'%U') != -1:
            log_format_index.setdefault('url_index', log_format_list.index(item))
        if item.find(r'%m') != -1:
            log_format_index.setdefault('method_index', log_format_list.index(item))
        if item.find(r'%H') != -1:
            log_format_index.setdefault('protocol_index', log_format_list.index(item))
    return log_format_index


def not_static_file(url):
    if url.split('.')[-1] not in config.static_file:
        return True
    else:
        return False


def get_new_url(origin_url):
    if len(origin_url.split('?')) == 1:
        return origin_url
    url_front = origin_url.split('?')[0]
    url_parameters = sorted(origin_url.split('?')[1].split('&'))
    new_url_parameters = []
    for parameter in url_parameters:
        key = parameter.split('=')[0]
        if len(parameter.split('=')) == 1:
            new_url_parameters.append(parameter)
        elif key in config.custom_keys:
            new_url_parameters.append(key + '=' + config.custom_parameters.get(key))
        elif key in config.fixed_parameter_keys:
            new_url_parameters.append(parameter)
        else:
            new_url_parameters.append(key + '=' + '{' + key + '}')
    new_url = url_front + '?' + '&amp;'.join(new_url_parameters)
    return new_url


def parse_log_file(target_file, log_format):
    hosts = []
    times = []
    urls = []
    with open('../data/'+target_file, 'r') as f:
        for line in f:
            line = line.split()
            hosts.append(line[log_format.get('host_index')])
            times.append(line[log_format.get('time_index')])
            if config.is_with_parameters:
                url = get_new_url(line[log_format.get('url_index')])
            else:
                url = line[log_format.get('url_index')].split('?')[0]
            if not_static_file(url):
                method = line[log_format.get('method_index')]
                protocol = line[log_format.get('protocol_index')]
                urls.append(method+' '+url+' '+protocol)

    pv = len(times)
    uv = len(set(hosts))
    response_avg = pv/len(set(times))

    times_counter = Counter(times)
    response_most_common = times_counter.most_common(1)[0]
    response_peak = response_most_common[1]
    response_peak_time = response_most_common[0].replace('[', '')

    urls_counter = Counter(urls)
    urls_most_common = urls_counter.most_common(config.urls_most_number)

    url_data_list = []
    for item in urls_most_common:
        ratio = '%0.3f' % float(item[1]*100/float(pv))
        url_data_list.append(URLData(url=item[0], pv=item[1], ratio=ratio))

    with open('../data/'+target_file, 'r') as f:
        for line in f:
            line_list = line.split()
            method = line_list[log_format.get('method_index')]
            if config.is_with_parameters:
                url = get_new_url(line_list[log_format.get('url_index')])
            else:
                url = line_list[log_format.get('url_index')].split('?')[0]
            protocol = line_list[log_format.get('protocol_index')]
            for url_data in url_data_list:
                if url_data.url == method+' '+url+' '+protocol:
                    url_data.time.append(line_list[log_format.get('time_index')])
                    break

    for url_data in url_data_list:
        url_data.peak = Counter(url_data.time).most_common(1)[0][1]

    total_data = {'pv': pv, 'uv': uv, 'response_avg': response_avg, 'response_peak': response_peak,
                  'response_peak_time': response_peak_time, 'url_data_list': url_data_list,
                  'source_file': target_file}
    generate_web_log_parser_report(total_data)

    total_data = {'source_file': target_file, 'urls': urls_counter}
    generate_web_log_parser_urls(total_data)


def parse_log_file_with_goaccess(target_file):
    source_file = '../data/' + target_file
    goaccess_file = '../result/report/' + target_file + '_GoAccess.html'
    command = """ goaccess -f %(file)s  -a -q \
            --time-format=%(time_format)s \
            --date-format=%(date_format)s \
            --log-format='%(log_format)s' \
            --no-progress > %(goaccess_file)s""" \
              % {'file': source_file, 'time_format': config.time_format, 'date_format': config.date_format,
                 'log_format': config.log_format, 'goaccess_file': goaccess_file}
    os.system(command)


def main():

    log_format = parse_log_format()

    result_files = [result_file.replace('.html', '') for result_file in get_dir_files('../result/report/')]
    target_files = sorted([data_file for data_file in get_dir_files('../data') if data_file not in result_files])

    for target_file in target_files:
        print datetime.datetime.now(), ' Start parse file : '+target_file

        parse_log_file(target_file, log_format)
        if config.goaccess_flag:
            parse_log_file_with_goaccess(target_file)

        print datetime.datetime.now(), ' End parse file: '+target_file

    update_index_html()

if __name__ == '__main__':
    main()
