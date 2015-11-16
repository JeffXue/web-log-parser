# -*- coding:utf-8 -*-
__author__ = 'xuekj'
from util import get_dir_files
from config import config


def generate_web_log_parser_report(data):
    main_html_header = """
<meta http-equiv='Content-Type' content='text/html; charset=utf-8'/>
<html>
<head>
<title>AutoTestReport</title>

</head>
        """
    if config.goaccess_flag:
        data.setdefault('goaccess_file', data.get('source_file')+'_GoAccess.html')
        data.setdefault('goaccess_title', u'查看GoAccess生成报告'.encode('utf-8'))
    else:
        data.setdefault('goaccess_file', '#')
        data.setdefault('goaccess_title', u'GoAccess报告已设置为无效，无法查看'.encode('utf-8'))
    main_html_body = """
<body>
    <h1 align='center'>WebLogPaser</h1>
    <table class='details' border='0' cellpadding='5' cellspacing='2' align='center' width='80%%'>
        <caption align='left'>Overall Analyzed Requests</caption>
        <tr valign='top'>
            <td style="BACKGROUND: #a6caf0" align="center" vertical-align="middle" class="cell"><strong>日志文件</strong></td>
            <td style='background:#BFBFBF;font-weight:bold;color:green;' colspan='3'><strong>%(source_file)s</strong></td>
            <td style='background:#BFBFBF;font-weight:bold;color:green;'>
                <a href='%(goaccess_file)s' target='_goaccess'>%(goaccess_title)s</a>
            </td>
        </tr>
        <tr valign='top'>
            <td style="BACKGROUND: #a6caf0" align="center" vertical-align="middle" class="cell"><strong>总PV</strong></td>
            <td style="BACKGROUND: #a6caf0" align="center" vertical-align="middle" class="cell"><strong>总UV</strong></td>
            <td style="BACKGROUND: #a6caf0" align="center" vertical-align="middle" class="cell"><strong>每秒最大处理消息数量</strong></td>
            <td style="BACKGROUND: #a6caf0" align="center" vertical-align="middle" class="cell"><strong>最大处理消息时间</strong></td>
            <td style="BACKGROUND: #a6caf0" align="center" vertical-align="middle" class="cell"><strong>每秒平均处理消息</strong></td>
        </tr>
        <tr valign='top'>
            <td style='background:#BFBFBF;font-weight:bold;color:green;'><strong>%(pv)s</strong></td>
            <td style='background:#BFBFBF;font-weight:bold;color:green;'><strong>%(uv)s</strong></td>
            <td style='background:#BFBFBF;font-weight:bold;color:green;'><strong>%(response_peak)s</strong></td>
            <td style='background:#BFBFBF;font-weight:bold;color:green;'><strong>%(response_peak_time)s</strong></td>
            <td style='background:#BFBFBF;font-weight:bold;color:green;'><strong>%(response_avg)s</strong></td>
        </tr>
    </table>
    """ % data

    url_data_list = data.get('url_data_list')
    url_data_html_header = """
    <table class='details' border='0' cellpadding='5' cellspacing='2'  align='center' width='80%%'>
        <caption align='left'>Top requests(URLS)</caption>
        <tr valign='top'>
            <td style="BACKGROUND: #a6caf0" align="center" vertical-align="middle" class="cell"><strong>Requests</strong></td>
            <td style="BACKGROUND: #a6caf0" align="center" vertical-align="middle" class="cell"><strong>访问量</strong></td>
            <td style="BACKGROUND: #a6caf0" align="center" vertical-align="middle" class="cell"><strong>比例</strong></td>
            <td style="BACKGROUND: #a6caf0" align="center" vertical-align="middle" class="cell"><strong>每秒最大处理消息数量</strong></td>
            <td style="BACKGROUND: #a6caf0" align="center" vertical-align="middle" class="cell"><strong>Method</strong></td>
            <td style="BACKGROUND: #a6caf0" align="center" vertical-align="middle" class="cell"><strong>Protocol</strong></td>
        </tr>
        """
    main_html_body += url_data_html_header
    for url_data in url_data_list:
        url_data_dict = {'url': url_data.url.split()[1], 'pv': url_data.pv, 'ratio': url_data.ratio,
                         'response_peak': url_data.peak,
                         'protocol': url_data.url.split()[0].replace('"', ''), 'method': url_data.url.split()[2].replace('"', '')}
        url_data_html = """
        <tr valign='top'>
            <td style='background:#BFBFBF;font-weight:bold;color:green;'><strong>%(url)s</strong></td>
            <td style='background:#BFBFBF;font-weight:bold;color:green;'><strong>%(pv)s</strong></td>
            <td style='background:#BFBFBF;font-weight:bold;color:green;'><strong>%(ratio)s%%</strong></td>
            <td style='background:#BFBFBF;font-weight:bold;color:green;'><strong>%(response_peak)s</strong></td>
            <td style='background:#BFBFBF;font-weight:bold;color:green;'><strong>%(protocol)s</strong></td>
            <td style='background:#BFBFBF;font-weight:bold;color:green;'><strong>%(method)s</strong></td>
        </tr>
        """ % url_data_dict
        main_html_body += url_data_html

    main_html_body += """
    </table>
</body>
</html>
    """
    html = main_html_header + main_html_body
    html_file = '../result/report/'+data.get('source_file')+'.html'
    with open(html_file, 'w') as f:
        f.write(html)


def update_index_html():
    html = """
<html>
    <head><title>WebLogPaser Report Index</title></head>
    <body>
    <h1>WebLogPaser Report Index</h1>
    <ul>
    """
    for report_file in get_dir_files('../result/report/'):
        if report_file.find('GoAccess') != -1:
            pass
        else:
            html += """
    <li><a href="report/%(web_log_parser_file)s" target="_WebLogPaserReport">%(web_log_parser_file)s</a></li>
            """ % {'web_log_parser_file': report_file}

    html += """
    </ul>
    </body>
</html>
    """

    with open('../result/index.html', 'w') as f:
        f.write(html)

