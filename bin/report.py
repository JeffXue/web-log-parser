# -*- coding:utf-8 -*-
__author__ = 'xuekj'
from util import get_dir_files
from config import config
from template import report_html_header
from template import report_overall_html_table
from template import report_top_request_html_table_header
from template import report_top_request_html_table_body
from template import report_hour_data_header
from template import report_hour_data
from template import report_minute_data_header
from template import report_minute_data
from template import report_second_data_header
from template import report_second_data
from template import report_html_end
from template import index_html_header
from template import index_html_li
from template import index_html_end
from template import url_html_header
from template import url_html_table_body
from template import url_html_end


def generate_web_log_parser_report(data):
    if config.goaccess_flag:
        data.setdefault('goaccess_file', data.get('source_file')+'_GoAccess.html')
        data.setdefault('goaccess_title', u'查看GoAccess生成报告'.encode('utf-8'))
    else:
        data.setdefault('goaccess_file', '#')
        data.setdefault('goaccess_title', u'GoAccess报告已设置为无效，无法查看'.encode('utf-8'))
    html_body = report_overall_html_table  % data

    html_body += report_top_request_html_table_header % {'web_log_urls_file': data.get('source_file')+'_urls.html'}

    url_data_list = data.get('url_data_list')
    for url_data in url_data_list:
        url_data_dict = {'url': url_data.url.split()[1], 'pv': url_data.pv, 'ratio': url_data.ratio,
                         'response_peak': url_data.peak,
                         'protocol': url_data.url.split()[2].replace('"', ''),
                         'method': url_data.url.split()[0].replace('"', '')}
        html_body += report_top_request_html_table_body % url_data_dict
    
    hours_pv = data.get('hours_hits')
    minutes_pv = data.get('minutes_hits')
    seconds_pv = data.get('second_hits')
    
    html_body += report_hour_data_header
    for hour in sorted(list(hours_pv)):
        html_body += report_hour_data % {'hour': hour, 'pv': hours_pv[hour]}
    
    html_body += report_minute_data_header
    for minute in sorted(list(minutes_pv)):
        html_body += report_minute_data % {'minute': minute, 'pv': minutes_pv[minute]}
    
    html_body += report_second_data_header
    for second in sorted(list(seconds_pv)):
        html_body += report_second_data % {'second': second, 'pv': seconds_pv[second]}

    html = report_html_header + html_body + report_html_end
    html_file = '../result/report/'+data.get('source_file')+'.html'
    with open(html_file, 'w') as f:
        f.write(html)

def generate_web_log_parser_urls(data):
    html = url_html_header % data
    for index, url_data in enumerate(sorted(data.get('urls'))):
        html += url_html_table_body % {'url': url_data.split()[1], 'num': index+1,
                'method': url_data.split()[0].replace('"', ''),
                'protocol': url_data.split()[2].replace('"', '')}
    html += url_html_end
    html_file = '../result/urls/'+data.get('source_file')+'_urls.html'
    with open(html_file, 'w') as f:
        f.write(html)

def update_index_html():
    html = index_html_header
    for report_file in sorted(get_dir_files('../result/report/')):
        if report_file.find('GoAccess') != -1 or report_file.find('.git') != -1 :
            pass
        else:
            html += index_html_li % {'web_log_parser_file': report_file}
    html += index_html_end

    with open('../result/index.html', 'w') as f:
        f.write(html)

