# -*- coding:utf-8 -*-
from util import get_dir_files
from config import config
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('./templates'))
report_template = env.get_template('report.html')
index_template = env.get_template('index.html')
url_template = env.get_template('url.html')


def generate_web_log_parser_report(data):
    if config.goaccess_flag:
        data.setdefault('goaccess_file', data.get('source_file')+'_GoAccess.html')
        data.setdefault('goaccess_title', u'查看GoAccess生成报告')
    else:
        data.setdefault('goaccess_file', '#')
        data.setdefault('goaccess_title', u'GoAccess报告已设置为无效，无法查看')

    hours_pv = sorted(list(data.get('hours_hits')))
    minutes_pv = sorted(list(data.get('minutes_hits')))
    seconds_pv = sorted(list(data.get('second_hits')))

    html = report_template.render(data=data,
                                  web_log_urls_file=data.get('source_file')+'_urls.html',
                                  second_line_flag=config.second_line_flag,
                                  hours_pv=hours_pv,
                                  minutes_pv=minutes_pv,
                                  seconds_pv=seconds_pv,
                                  method_counts=data.get('method_counts'),
                                  cost_time_range_percentile=data.get('cost_time_range_percentile'),
                                  cost_time_list=data.get('cost_time_list'),
                                  cost_time_flag=data.get('cost_time_flag'),
                                  cost_time_percentile_flag=data.get('cost_time_percentile_flag')
                                  )

    html_file = '../result/report/'+data.get('source_file')+'.html'
    with open(html_file, 'w') as f:
        f.write(html.encode('utf-8'))


def generate_web_log_parser_urls(data):

    html = url_template.render(data=data,
                               url_datas=sorted(data.get('urls')))

    html_file = '../result/urls/'+data.get('source_file')+'_urls.html'
    with open(html_file, 'w') as f:
        f.write(html.encode('utf-8'))


def update_index_html():
    html = index_template.render(files=sorted(get_dir_files('../result/report/')))

    with open('../result/index.html', 'w') as f:
        f.write(html.encode('utf-8'))

