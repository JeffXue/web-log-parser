# -*- coding:utf-8 -*-
import json
import requests

from util import get_dir_files
from config import config
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('./templates'))
if config.report_language == 'english':
    report_template = env.get_template('report_en.html')
else:
    report_template = env.get_template('report.html')
index_template = env.get_template('index.html')
url_template = env.get_template('url.html')


def upload_report(data, hours_times, minutes_times):
    target_file = data['source_file']
    pv = data['pv']
    uv = data['uv']
    get_count = data['method_counts']['get']
    get_percent = data['method_counts']['get_percentile']
    post_count = data['method_counts']['post']
    post_percent = data['method_counts']['post_percentile']
    response_peak = data['response_peak']
    response_peak_time = data['response_peak_time']
    response_avg = data['response_avg']
    hours_times = hours_times
    hours_pv = data['hours_hits']
    hours_most_common = data['hours_hits'].most_common(1)[0]
    hours_pv_peak = hours_most_common[1]
    hours_pv_peak_time = hours_most_common[0]
    minute_times = minutes_times
    minute_pv = data['minutes_hits']
    minute_most_common = data['minutes_hits'].most_common(1)[0]
    minute_pv_peak = minute_most_common[1]
    minute_pv_peak_time = minute_most_common[0]
    cost_percent = data['cost_time_range_percentile']
    cost_time_threshold = data['cost_time_threshold']
    cost_range = data['cost_time_range']
    url_data_list = []

    for url_data in data['url_data_list']:
        url_data_list.append(url_data.get_data())

    data = {'target_file': target_file, 'pv': pv, 'uv': uv,
            'get_count': get_count, 'get_percent': get_percent,
            'post_count': post_count, 'post_percent': post_percent,
            'response_peak': response_peak, 'response_peak_time': response_peak_time,
            'response_avg': response_avg,
            'hours_times': hours_times,
            'hours_pv': hours_pv,
            'hours_pv_peak': hours_pv_peak,
            'hours_pv_peak_time': hours_pv_peak_time,
            'minute_times': minute_times,
            'minute_pv': minute_pv,
            'minute_pv_peak': minute_pv_peak,
            'minute_pv_peak_time': minute_pv_peak_time,
            'cost_percent': cost_percent,
            'cost_percent_range': ['<50ms', '50~100ms', '100~150ms', '150~200ms', '200~250ms', '250~300ms',
                                   '300~350ms', '350~400ms', '400~450ms', '450~500ms', '>500ms'],
            'cost_time_threshold': cost_time_threshold,
            'url_data_list': url_data_list,
            'cost_range': cost_range,
            'status_codes': data['status_codes']}
    headers = {'Content-Type': 'application/json'}
    r = requests.post(config.upload_url, data=json.dumps(data), headers=headers)
    print(r.text)


def generate_web_log_parser_report(data):
    if config.goaccess_flag:
        data.setdefault('goaccess_file', data.get('source_file') + '_GoAccess.html')
        if config.report_language == 'english':
            data.setdefault('goaccess_title', u'Check GoAccess Report')
        else:
            data.setdefault('goaccess_title', u'查看GoAccess生成报告')
    else:
        data.setdefault('goaccess_file', '#')
        if config.report_language == 'english':
            data.setdefault('goaccess_title', u'GoAccess Report Is Disable!')
        else:
            data.setdefault('goaccess_title', u'GoAccess报告已设置为无效，无法查看')

    hours_times = sorted(list(data.get('hours_hits')))
    minutes_times = sorted(list(data.get('minutes_hits')))
    seconds_times = sorted(list(data.get('second_hits')))

    if config.upload_flag:
        upload_report(data, hours_times, minutes_times)

    html = report_template.render(data=data,
                                  web_log_urls_file=data.get('source_file') + '_urls.html',
                                  second_line_flag=config.second_line_flag,
                                  hours_times=hours_times,
                                  minutes_times=minutes_times,
                                  seconds_times=seconds_times,
                                  method_counts=data.get('method_counts'),
                                  cost_time_range_percentile=data.get('cost_time_range_percentile'),
                                  cost_time_list=data.get('cost_time_list'),
                                  cost_time_flag=data.get('cost_time_flag'),
                                  cost_time_percentile_flag=data.get('cost_time_percentile_flag'),
                                  cost_time_threshold=data.get('cost_time_threshold'),
                                  cost_time_range=data.get('cost_time_range'),
                                  status_codes=data.get('status_codes'),
                                  status_codes_keys=data.get('status_codes').keys())

    html_file = '../result/report/' + data.get('source_file') + '.html'
    with open(html_file, 'wb') as f:
        f.write(html.encode('utf-8'))


def generate_web_log_parser_urls(data):
    html = url_template.render(data=data,
                               url_datas=sorted(data.get('urls')))

    html_file = '../result/urls/' + data.get('source_file') + '_urls.html'
    with open(html_file, 'wb') as f:
        f.write(html.encode('utf-8'))


def update_index_html():
    html = index_template.render(files=sorted(get_dir_files('../result/report/')))

    with open('../result/index.html', 'wb') as f:
        f.write(html.encode('utf-8'))
