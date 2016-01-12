# -*- coding:utf-8 -*-
__author__ = 'xuekj'

report_html_header = """
<meta http-equiv='Content-Type' content='text/html; charset=utf-8'/>
<html>
<style type="text/css">
th{
    background: #a6caf0;
    align:center;
    vertical-align:middle;
}
td{
    background:#bfbfbf;
    font-weight:bold;
    color:green;
}
</style>
<link rel="stylesheet" href="../libs/morris.css">
<head>
    <title>LogPaserReport</title>
</head>
"""
report_overall_html_table = """
<body>
    <h1 align='center'>WebLogPaser</h1>
    <table border='0' cellpadding='5' cellspacing='2' align='center' width='80%%'>
        <caption align='left'>Overall Analyzed Requests</caption>
        <tr>
            <th><strong>日志文件</strong></th>
            <td colspan='3'><strong>%(source_file)s</strong></td>
            <td>
                <a href='%(goaccess_file)s' target='_goaccess'>%(goaccess_title)s</a>
            </td>
        </tr>
        <tr>
            <th><strong>总PV</strong></th>
            <th><strong>总UV</strong></th>
            <th><strong>每秒最大处理消息数量</strong></th>
            <th><strong>最大处理消息时间</strong></th>
            <th><strong>每秒平均处理消息</strong></th>
        </tr>
        <tr>
            <td><strong>%(pv)s</strong></td>
            <td><strong>%(uv)s</strong></td>
            <td><strong>%(response_peak)s</strong></td>
            <td><strong>%(response_peak_time)s</strong></td>
            <td><strong>%(response_avg)s</strong></td>
        </tr>
    </table>

    <table border='0' cellpadding='5' cellspacing='2' align='center' width='80%%'>
        <caption align='left'>PV Chart (每小时PV变化曲线图)</caption>
        <tr>
            <td><div id="hoursChart" style="height: 250px;"></div></td>
        </tr>
    </table>
"""

report_top_request_html_table_header = """
    <table border='0' cellpadding='5' cellspacing='2'  align='center' width='80%%' style="TABLE-LAYOUT: fixed; WORD-BREAK: break-all">
        <caption>
            Top requests<a href='../urls/%(web_log_urls_file)s' target='_urls' >（查看所有URL）</a>
        </caption>
        <tr>
            <th colspan="9"><strong>Requests</strong></th>
            <th><strong>访问量</strong></th>
            <th><strong>比例</strong></th>
            <th><strong>每秒最大处<br/>理消息数量</strong></th>
            <th><strong>Method</strong></th>
            <th><strong>Protocol</strong></th>
        </tr>
"""

report_top_request_html_table_body = """
        <tr>
            <td colspan="9"><strong>%(url)s</strong></td>
            <td><strong>%(pv)s</strong></td>
            <td><strong>%(ratio)s%%</strong></td>
            <td><strong>%(response_peak)s</strong></td>
            <td><strong>%(method)s</strong></td>
            <td><strong>%(protocol)s</strong></td>
        </tr>
"""

report_html_end = """
    </table>

<script src="../libs/jquery.min.js"></script>
<script src="../libs//raphael-min.js"></script>
<script src="../libs/morris.min.js"></script>
<script>
new Morris.Line({
    element: 'hoursChart',
    data: [
        { hour: '%(date)s 00:00', pv: %(h0)d },
        { hour: '%(date)s 01:00', pv: %(h1)d },
        { hour: '%(date)s 02:00', pv: %(h2)d },
        { hour: '%(date)s 03:00', pv: %(h3)d },
        { hour: '%(date)s 04:00', pv: %(h4)d },
        { hour: '%(date)s 05:00', pv: %(h5)d },
        { hour: '%(date)s 06:00', pv: %(h6)d },
        { hour: '%(date)s 07:00', pv: %(h7)d },
        { hour: '%(date)s 08:00', pv: %(h8)d },
        { hour: '%(date)s 09:00', pv: %(h9)d },
        { hour: '%(date)s 10:00', pv: %(h10)d },
        { hour: '%(date)s 11:00', pv: %(h11)d },
        { hour: '%(date)s 12:00', pv: %(h12)d },
        { hour: '%(date)s 13:00', pv: %(h13)d },
        { hour: '%(date)s 14:00', pv: %(h14)d },
        { hour: '%(date)s 15:00', pv: %(h15)d },
        { hour: '%(date)s 16:00', pv: %(h16)d },
        { hour: '%(date)s 17:00', pv: %(h17)d },
        { hour: '%(date)s 18:00', pv: %(h18)d },
        { hour: '%(date)s 19:00', pv: %(h19)d },
        { hour: '%(date)s 20:00', pv: %(h20)d },
        { hour: '%(date)s 21:00', pv: %(h21)d },
        { hour: '%(date)s 22:00', pv: %(h22)d },
        { hour: '%(date)s 23:00', pv: %(h23)d },
        ],
        xkey: ['hour'],
        ykeys: ['pv'],
        labels: ['pv']
    });
</script>
</body>
</html>
"""

index_html_header = """
<meta http-equiv='Content-Type' content='text/html; charset=utf-8'/>
<html>
<head>
    <title>WebLogPaser Report Index</title>
</head>
<body>
    <h1>WebLogPaser Report Index</h1>
    <ul>
"""

index_html_li = """
    <li><a href="report/%(web_log_parser_file)s" target="_WebLogPaserReport">%(web_log_parser_file)s</a></li>
"""

index_html_end = """
    </ul>
</body>
</html>
"""

url_html_header = """
<meta http-equiv='Content-Type' content='text/html; charset=utf-8'/>
<html>
<style type="text/css">
th{
    background: #a6caf0;
    align:center;
    vertical-align:middle;
}
td{
    background:#bfbfbf;
    font-weight:bold;
    color:green;
}
</style>
<head>
    <title>LogPaserURLs</title>
</head>
<body>
    <table border='0' cellpadding='5' cellspacing='2'  align='center' width='80%%' style="TABLE-LAYOUT: fixed; WORD-BREAK: break-all">
    <caption algin='left'>日志文件%(source_file)s URL汇总</caption>
    <tr>
        <th>序号</th>
        <th colspan="11">URL</th>
        <th>Method</th>
        <th>Protocol</th>
    </tr>
"""

url_html_table_body = """
    <tr>
        <td>%(num)d</td>
        <td colspan="11">%(url)s</td>
        <td>%(method)s</td>
        <td>%(protocol)s</td>
    </tr>
"""

url_html_end = """
    </table>
</body>
</html>
"""


