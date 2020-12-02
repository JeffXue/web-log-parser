# -*- coding:utf-8 -*-
import codecs
import os
import re
import json
import time
import traceback
import datetime
from collections import Counter
from numpy import var, average, percentile

from util import get_dir_files
from config import config
from report import generate_web_log_parser_report
from report import generate_web_log_parser_urls
from report import update_index_html


class URLData:
    def __init__(self, url=None, pv=None, ratio=None, peak=None):
        self.url = url
        self.pv = pv
        self.ratio = ratio
        self.peak = peak
        self.time = []
        self.cost = []
        self.cost_time = {'p9': None, 'p8': None, 'p5': None, 'avg': None, 'variance': None}

    def get_data(self):
        return {'url': self.url, 'pv': self.pv, 'ratio': self.ratio,
                'peak': self.peak, 'cost_time': self.cost_time}


def parse_log_format():
    log_format_index = {}
    log_format_list = config.log_format.split()
    for item in log_format_list:
        if item == 'ip':
            log_format_index.setdefault('ip_index', log_format_list.index(item) + 1)
        if item == 'real_ip':
            log_format_index.setdefault('real_ip_index', log_format_list.index(item) + 1)
        if item == 'datetime':
            log_format_index.setdefault('time_index', log_format_list.index(item) + 1)
        if item == 'url':
            log_format_index.setdefault('url_index', log_format_list.index(item) + 1)
        if item == 'method':
            log_format_index.setdefault('method_index', log_format_list.index(item) + 1)
        if item == 'protocol':
            log_format_index.setdefault('protocol_index', log_format_list.index(item) + 1)
        if item == 'cost':
            log_format_index.setdefault('cost_time_index', log_format_list.index(item) + 1)
        if item == 'status':
            log_format_index.setdefault('status', log_format_list.index(item) + 1)

    if 'real_ip_index' in log_format_index.keys():
        log_format_index.setdefault('host_index', log_format_list.index('real_ip') + 1)
    else:
        log_format_index.setdefault('host_index', log_format_list.index('ip') + 1)

    return log_format_index


def not_static_file(url):
    url_front = url.split('?')[0]
    if url_front.split('.')[-1] not in config.static_file:
        return True
    else:
        return False


def is_ignore_url(url):
    url_front = url.split('?')[0]
    if url_front not in config.ignore_urls:
        return False
    else:
        return True


def get_new_url_with_parameters(origin_url):
    origin_url_list = origin_url.split('?')

    if len(origin_url_list) == 1:
        return origin_url
    url_front = origin_url_list[0]
    url_parameters = sorted(origin_url_list[1].split('&'))
    new_url_parameters = []
    for parameter in url_parameters:
        parameter_list = parameter.split('=')
        key = parameter_list[0]
        if len(parameter_list) == 1:
            new_url_parameters.append(parameter)
        elif key in config.custom_keys:
            new_url_parameters.append(key + '=' + config.custom_parameters.get(key))
        elif key in config.fixed_parameter_keys:
            new_url_parameters.append(parameter)
        else:
            new_url_parameters.append(key + '=' + '{' + key + '}')
    new_url = url_front + '?' + '&amp;'.join(new_url_parameters)
    return new_url


def get_new_url_for_always_parameters(origin_url):
    origin_url_list = origin_url.split('?')

    if len(origin_url_list) == 1:
        return origin_url_list[0]

    url_front = origin_url_list[0]
    url_parameters = sorted(origin_url_list[1].split('&'))
    new_url_parameters = []
    for parameter in url_parameters:
        key = parameter.split('=')[0]
        if key in config.always_parameter_keys:
            new_url_parameters.append(parameter)
    if new_url_parameters:
        new_url = url_front + '?' + '&amp;'.join(new_url_parameters)
    else:
        new_url = url_front
    return new_url


def ignore_url_suffix(origin_url):
    origin_url_list = origin_url.split('?')

    if len(origin_url_list) == 1:
        uri_parameter = None
    else:
        uri_parameter = origin_url_list[1:]

    uri = origin_url_list[0]
    new_uri = uri
    for suffix in config.ignore_url_suffix:
        if uri.endswith(suffix):
            new_uri = uri.replace(suffix, '')
            break
    if uri_parameter:
        return new_uri + '?' + '?'.join(uri_parameter)
    else:
        return new_uri


def get_url(match, log_format):
    origin_url = ignore_url_suffix(match.group(log_format.get('url_index')))
    if config.is_with_parameters:
        url = get_new_url_with_parameters(origin_url)
    else:
        if config.always_parameter_keys:
            url = get_new_url_for_always_parameters(origin_url)
        else:
            url = match.group(origin_url.split('?')[0].split('.json')[0])
    return url


def parse_log_file(target_file, log_format):
    # 用户IP
    hosts = []
    # 访问时间
    times = []
    # 访问时间中的小时
    hours = []
    # 访问时间中的分钟
    minutes = []
    # 请求URL
    urls = []
    # 请求响应时间
    cost_time_list = []
    cost_time_flag = False
    cost_time_percentile_flag = False
    if 'cost_time_index' in log_format.keys():
        if config.cost_time_flag:
            cost_time_flag = True
        if config.cost_time_percentile_flag:
            cost_time_percentile_flag = True

    # 请求方法计数器
    method_counts = {'post': 0, 'post_percentile': 0, 'get': 0, 'get_percentile': 0}

    # http status code统计
    status_codes = {}

    pattern = re.compile(config.log_pattern)

    # 第一次读取整个文件，获取对应的请求时间、请求URL、请求方法、用户IP、请求响应时间等数据
    with codecs.open('../data/' + target_file, 'r', 'utf-8') as f:
        for line in f:
            match = pattern.match(line)
            if match is None:
                continue
            url = get_url(match, log_format)
            if is_ignore_url(url):
                continue

            match_method = match.group(log_format.get('method_index'))

            if match_method not in config.support_method:
                continue
            if not_static_file(url):
                hosts.append(match.group(log_format.get('host_index')).split(',')[0])
                # log_time = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(match.group(log_format.get('time_index')),
                #                                                             '%d/%b/%Y:%H:%M:%S'))
                log_time = match.group(log_format.get('time_index'))
                times.append(log_time)
                log_time_list = log_time.split(':')
                hours.append(':'.join(log_time_list[0:2]))
                minutes.append(':'.join(log_time_list[0:3]))
                if match_method == 'POST':
                    method_counts['post'] += 1
                if match_method == 'GET':
                    method_counts['get'] += 1
                urls.append(match_method + ' ' + url)
                if 'cost_time_index' in log_format.keys():
                    request_cost_time = int(float(match.group(log_format.get('cost_time_index'))) * 1000)
                    if cost_time_flag:
                        cost_time_list.append({'time': log_time, 'cost_time': request_cost_time})
                    else:
                        cost_time_list.append({'time': '', 'cost_time': request_cost_time})
                if 'status' in log_format.keys():
                    status_code = int(match.group(log_format.get('status')))
                    if status_code in status_codes.keys():
                        status_codes[status_code] += 1
                    else:
                        status_codes.setdefault(status_code, 1)

    if len(times) > 2:
        cross_time = datetime.datetime.strptime(times[-1], '%d/%b/%Y:%H:%M:%S') - datetime.datetime.strptime(times[0], '%d/%b/%Y:%H:%M:%S')
    else:
        cross_time = None

    # 计算PV、UV、平均请求数、GET/POST占比
    pv = len(times)
    uv = len(set(hosts))
    response_avg = int(pv / len(set(times)))
    method_counts['post_percentile'] = int(method_counts['post'] * 100 / pv)
    method_counts['get_percentile'] = int(method_counts['get'] * 100 / pv)

    # 获取每小时、每分钟、每秒的请求数量
    hours_counter = Counter(hours)
    minutes_counter = Counter(minutes)
    times_counter = Counter(times)

    # 获取每秒最大请求数及其请求时间
    response_most_common = times_counter.most_common(1)[0]
    response_peak = response_most_common[1]
    response_peak_time = response_most_common[0]

    # 根据不同URL的PV数量截取较多请求，后续只分析进去排名内的URL
    urls_counter = Counter(urls)
    urls_most_common = urls_counter.most_common(config.urls_most_number)

    # 计算请求占比
    url_data_list = []
    for_url_data_uri_index = []
    for item in urls_most_common:
        if item[1] >= config.urls_pv_threshold:
            ratio = '%0.3f' % float(item[1] * 100 / float(pv))
            url_data_list.append(URLData(url=item[0], pv=item[1], ratio=ratio))
            for_url_data_uri_index.append(item[0])
            continue
        if cross_time and cross_time.seconds < config.urls_pv_threshold_time and item[1] >= config.urls_pv_threshold_min:
            ratio = '%0.3f' % float(item[1] * 100 / float(pv))
            url_data_list.append(URLData(url=item[0], pv=item[1], ratio=ratio))
            for_url_data_uri_index.append(item[0])
            continue

    # 第二次读取文件，以获取特定请求的访问时间及响应时间
    with codecs.open('../data/' + target_file, 'r', 'utf-8') as f:
        for line in f:
            match = pattern.match(line)
            if match is None:
                continue
            method = match.group(log_format.get('method_index'))
            url = get_url(match, log_format)

            target_url = ' '.join([method, url])
            if target_url in for_url_data_uri_index:
                index = for_url_data_uri_index.index(target_url)
                url_data_list[index].time.append(match.group(log_format.get('time_index')))
                if 'cost_time_index' in log_format.keys():
                    url_data_list[index].cost.append(float(match.group(log_format.get('cost_time_index'))))

    for url_data in url_data_list:
        # 计算每个特定请求的每秒最大并发
        url_data.peak = Counter(url_data.time).most_common(1)[0][1]

        # 计算每个特定请求的耗时均值，中值，方差，百分位等
        if url_data.cost:
            url_data.cost_time['avg'] = '%0.3f' % float(average(url_data.cost))
            url_data.cost_time['variance'] = int(var(url_data.cost))
            url_data.cost_time['p9'] = '%0.3f' % percentile(url_data.cost, 90)
            url_data.cost_time['p8'] = '%0.3f' % percentile(url_data.cost, 80)
            url_data.cost_time['p5'] = '%0.3f' % percentile(url_data.cost, 50)

    # 统计不同响应时间范围的请求数量
    cost_time_range = {'r1': 0, 'r2': 0, 'r3': 0, 'r4': 0, 'r5': 0, 'r6': 0,
                       'r7': 0, 'r8': 0, 'r9': 0, 'r10': 0, 'r11': 0}
    for cost_time in cost_time_list:
        if cost_time['cost_time'] <= 50:
            cost_time_range['r1'] += 1
        elif 50 < cost_time['cost_time'] <= 100:
            cost_time_range['r2'] += 1
        elif 100 < cost_time['cost_time'] <= 150:
            cost_time_range['r3'] += 1
        elif 150 < cost_time['cost_time'] <= 200:
            cost_time_range['r4'] += 1
        elif 200 < cost_time['cost_time'] <= 250:
            cost_time_range['r5'] += 1
        elif 250 < cost_time['cost_time'] <= 300:
            cost_time_range['r6'] += 1
        elif 300 < cost_time['cost_time'] <= 350:
            cost_time_range['r7'] += 1
        elif 350 < cost_time['cost_time'] <= 400:
            cost_time_range['r8'] += 1
        elif 400 < cost_time['cost_time'] <= 450:
            cost_time_range['r9'] += 1
        elif 450 < cost_time['cost_time'] <= 500:
            cost_time_range['r10'] += 1
        else:
            cost_time_range['r11'] += 1
    # 计算不同响应时间范围的请求占比
    cost_time_range_percentile = {'r1p': 0, 'r2p': 0, 'r3p': 0, 'r4p': 0, 'r5p': 0, 'r6p': 0,
                                  'r7p': 0, 'r8p': 0, 'r9p': 0, 'r10p': 0, 'r11p': 0}
    if cost_time_list:
        total_cost_time_pv = float(len(cost_time_list))
        if cost_time_range['r1']:
            cost_time_range_percentile['r1p'] = '%0.3f' % float(cost_time_range['r1'] * 100 / total_cost_time_pv)
        if cost_time_range['r2']:
            cost_time_range_percentile['r2p'] = '%0.3f' % float(cost_time_range['r2'] * 100 / total_cost_time_pv)
        if cost_time_range['r3']:
            cost_time_range_percentile['r3p'] = '%0.3f' % float(cost_time_range['r3'] * 100 / total_cost_time_pv)
        if cost_time_range['r4']:
            cost_time_range_percentile['r4p'] = '%0.3f' % float(cost_time_range['r4'] * 100 / total_cost_time_pv)
        if cost_time_range['r5']:
            cost_time_range_percentile['r5p'] = '%0.3f' % float(cost_time_range['r5'] * 100 / total_cost_time_pv)
        if cost_time_range['r6']:
            cost_time_range_percentile['r6p'] = '%0.3f' % float(cost_time_range['r6'] * 100 / total_cost_time_pv)
        if cost_time_range['r7']:
            cost_time_range_percentile['r7p'] = '%0.3f' % float(cost_time_range['r7'] * 100 / total_cost_time_pv)
        if cost_time_range['r8']:
            cost_time_range_percentile['r8p'] = '%0.3f' % float(cost_time_range['r8'] * 100 / total_cost_time_pv)
        if cost_time_range['r9']:
            cost_time_range_percentile['r9p'] = '%0.3f' % float(cost_time_range['r9'] * 100 / total_cost_time_pv)
        if cost_time_range['r10']:
            cost_time_range_percentile['r10p'] = '%0.3f' % float(cost_time_range['r10'] * 100 / total_cost_time_pv)
        if cost_time_range['r11']:
            cost_time_range_percentile['r11p'] = '%0.3f' % float(cost_time_range['r11'] * 100 / total_cost_time_pv)

    total_data = {'pv': pv, 'uv': uv, 'response_avg': response_avg, 'response_peak': response_peak,
                  'response_peak_time': response_peak_time, 'url_data_list': url_data_list,
                  'source_file': target_file, 'hours_hits': hours_counter, 'minutes_hits': minutes_counter,
                  'second_hits': times_counter, 'cost_time_list': cost_time_list, 'cost_time_flag': cost_time_flag,
                  'cost_time_range_percentile': cost_time_range_percentile, 'method_counts': method_counts,
                  'cost_time_percentile_flag': cost_time_percentile_flag,
                  'cost_time_threshold': config.cost_time_threshold, 'cost_time_range': cost_time_range,
                  'status_codes': status_codes}
    generate_web_log_parser_report(total_data)


def parse_log_file_with_goaccess(target_file):
    source_file = '../data/' + target_file
    goaccess_file = '../result/report/' + target_file + '_GoAccess.html'
    command = """ goaccess -f %(file)s  -a -q \
            --time-format=%(time_format)s \
            --date-format=%(date_format)s \
            --log-format='%(goaccess_log_format)s' \
            --no-progress > %(goaccess_file)s""" \
              % {'file': source_file, 'time_format': config.time_format, 'date_format': config.date_format,
                 'goaccess_log_format': config.goaccess_log_format, 'goaccess_file': goaccess_file}
    os.system(command)


def main():
    log_format = parse_log_format()

    result_files = [result_file.replace('.html', '') for result_file in get_dir_files('../result/report/')]
    target_files = sorted([data_file for data_file in get_dir_files('../data') if data_file not in result_files])

    for target_file in target_files:
        try:
            print(datetime.datetime.now(), ' Start parse file : ' + target_file)

            parse_log_file(target_file, log_format)
            if config.goaccess_flag:
                parse_log_file_with_goaccess(target_file)

            print(datetime.datetime.now(), ' End parse file: ' + target_file)
        except Exception:
            exstr = traceback.format_exc()
            print(exstr)
    update_index_html()


if __name__ == '__main__':
    main()
