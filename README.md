## WebLogParser ##
**WebLogParser**为开源的分析web日志工具，采用python语言开发，具有灵活的日志格式配置。

## 数据说明 ##
**Overall Analyzed Requests：**
- 日志文件
- GoAccess分析结果（独立调用，可屏蔽）
- PV
- UV 
- 每秒最大处理消息数量（及其对应时间点）
- 每秒平均处理消息

**Top requests(URLS)**（默认前10）
- Requests URL
- 访问量
- 比例
- 每秒最大处理消息数量
- Protocol
- Method

## 使用方法 ##
1. 将需要分析的日志存放到data目录下
2. 配置Config.ini
- goaccess_flag 是否获取GoAccess分析结果，设置为1：获取，0:不获取（需要已安装GoAccess）
- time-format 日志中的时间格式，用于GoAccess
- date-format 日志中的日期格式，用于GoAccess
- log-format 日志内容格式，用于本工具和GoAccess
- static-file 静态文件后缀，本工具在统计URL时将过滤静态文件
- is_with_parameters 统计URL是否使用URL中参数一起进行分析，设置为1：使用参数， 0：不使用；默认将转换URL中参数，如?key=123统计时记录为key={key}
- custom_parameters 配置特殊的参数键值对，以逗号分隔，配置的t={timeStramp}，在分析参数时会将t键的值替换为固定的{timeStramp}
- fixed_parameter_keys 配置特殊的参数key值，以逗号分隔，参数中的key=123，不会被置换为key={key}
- urls_most_number 配置单独统计的URL最大数量
3. 运行
    python start.py
4. 查看结果
    查看result/目录下的index.html
    （result/report/目录下将生成对应的分析结果）
    
## 样例 ##
<html>
    <head><title>WebLogPaser Report Index</title></head>
    <body>
    <h1>WebLogPaser Report Index</h1>
    <ul>
    <li><a href="#" target="_WebLogPaserReport">access_log_domain_20150506.html</a></li>
    </ul>
    </body>
</html>

<html>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<link rel="stylesheet" href="http://cdnjs.cloudflare.com/ajax/libs/morris.js/0.5.1/morris.css">
<head>
<title>AutoTestReport</title>
</head>
<body>
    <h1 align="center">WebLogPaser</h1>
    <table border="0" align="center" width="80%">
        <caption>Overall Analyzed Requests</caption>
        <tr>
            <th><strong>日志文件</strong></th>
            <td colspan="3"><strong>access_log_domain_20150506</strong></td>
            <td>
                <a href="http://goaccess.io/goaccess_html_report.html?src=gh" target="_goaccess">查看GoAccess生成报告</a>
            </td>
        </tr>
        <tr>
            <th><strong>总PV</strong></th>
            <th><strong>总UV</strong></th>
            <th><strong>每秒最大处<br/>理消息数量</strong></th>
            <th><strong>最大处理<br/>消息时间</strong></th>
            <th><strong>每秒平均<br/>处理消息</strong></th>
        </tr>
        <tr>
            <td><strong>561066</strong></td>
            <td><strong>50501</strong></td>
            <td><strong>136</strong></td>
            <td><strong>06/May/2015:11:51:12</strong></td>
            <td><strong>8</strong></td>
        </tr>
    </table>
    <table border='0' cellpadding='5' cellspacing='2' align='center' width='80%'>
        <caption align='left'>PV Chart (每小时PV变化曲线图)</caption>
        <tr>
            <td><div id="hoursChart" style="height: 250px;"></div></td>
        </tr>
    </table>
    <table border="0" align="center" width="80%%">
        <caption>Top requests(URLS)</caption>
        <tr>
            <th><strong>Requests</strong></th>
            <th><strong>访问量</strong></th>
            <th><strong>比例</strong></th>
            <th><strong>每秒最大处<br/>理消息数量</strong></th>
            <th><strong>Method</strong></th>
            <th><strong>Protocol</strong></th>
        </tr>
        <tr>
            <td><strong>/uc_server/avatar.php</strong></td>
            <td><strong>194084</strong></td>
            <td><strong>34.592%</strong></td>
            <td><strong>75</strong></td>
            <td><strong>GET</strong></td>
            <td><strong>HTTP/1.1</strong></td>
        </tr>
        <tr>
            <td><strong>/forum.php</strong></td>
            <td><strong>95833</strong></td>
            <td><strong>17.081%</strong></td>
            <td><strong>96</strong></td>
            <td><strong>GET</strong></td>
            <td><strong>HTTP/1.1</strong></td>
        </tr>
        <tr>
            <td><strong>/topic.php</strong></td>
            <td><strong>75987</strong></td>
            <td><strong>13.543%</strong></td>
            <td><strong>27</strong></td>
            <td><strong>GET</strong></td>
            <td><strong>HTTP/1.1</strong></td>
        </tr>
        <tr>
            <td><strong>/misc.php</strong></td>
            <td><strong>73379</strong></td>
            <td><strong>13.078%</strong></td>
            <td><strong>26</strong></td>
            <td><strong>POST</strong></td>
            <td><strong>HTTP/1.1</strong></td>
        </tr>
        <tr>
            <td><strong>/home.php</strong></td>
            <td><strong>19729</strong></td>
            <td><strong>3.516%</strong></td>
            <td><strong>10</strong></td>
            <td><strong>GET</strong></td>
            <td><strong>HTTP/1.1</strong></td>
        </tr>
        <tr>
            <td><strong>/</strong></td>
            <td><strong>8280</strong></td>
            <td><strong>1.476%</strong></td>
            <td><strong>7</strong></td>
            <td><strong>GET</strong></td>
            <td><strong>HTTP/1.1</strong></td>
        </tr>
        <tr>
            <td><strong>/setusername.php</strong></td>
            <td><strong>8129</strong></td>
            <td><strong>1.449%</strong></td>
            <td><strong>10</strong></td>
            <td><strong>POST</strong></td>
            <td><strong>HTTP/1.1</strong></td>
        </tr>
        <tr>
            <td><strong>/setusername.php</strong></td>
            <td><strong>7698</strong></td>
            <td><strong>1.372%</strong></td>
            <td><strong>7</strong></td>
            <td><strong>GET</strong></td>
            <td><strong>HTTP/1.1</strong></td>
        </tr>
        <tr>
            <td><strong>/forum-37-1.html</strong></td>
            <td><strong>6782</strong></td>
            <td><strong>1.209%</strong></td>
            <td><strong>2</strong></td>
            <td><strong>GET</strong></td>
            <td><strong>HTTP/1.1</strong></td>
        </tr>
        <tr>
            <td><strong>/api/getdata.php</strong></td>
            <td><strong>3045</strong></td>
            <td><strong>0.543%</strong></td>
            <td><strong>6</strong></td>
            <td><strong>GET</strong></td>
            <td><strong>HTTP/1.0</strong></td>
        </tr>
    </table>
<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js"></script>
<script src="http://cdnjs.cloudflare.com/ajax/libs/raphael/2.1.0/raphael-min.js"></script>
<script src="http://cdnjs.cloudflare.com/ajax/libs/morris.js/0.5.1/morris.min.js"></script>    
<script>
new Morris.Line({
    element: 'hoursChart',
    data: [
        { hour: '2016-01-04 00:00', pv: 31848 },
        { hour: '2016-01-04 01:00', pv: 26482 },
        { hour: '2016-01-04 02:00', pv: 25671 },
        { hour: '2016-01-04 03:00', pv: 23730 },
        { hour: '2016-01-04 04:00', pv: 24062 },
        { hour: '2016-01-04 05:00', pv: 23596 },
        { hour: '2016-01-04 06:00', pv: 24632 },
        { hour: '2016-01-04 07:00', pv: 27568 },
        { hour: '2016-01-04 08:00', pv: 52962 },
        { hour: '2016-01-04 09:00', pv: 101230 },
        { hour: '2016-01-04 10:00', pv: 112175 },
        { hour: '2016-01-04 11:00', pv: 112112 },
        { hour: '2016-01-04 12:00', pv: 75513 },
        { hour: '2016-01-04 13:00', pv: 91474 },
        { hour: '2016-01-04 14:00', pv: 100352 },
        { hour: '2016-01-04 15:00', pv: 103058 },
        { hour: '2016-01-04 16:00', pv: 104474 },
        { hour: '2016-01-04 17:00', pv: 91705 },
        { hour: '2016-01-04 18:00', pv: 66823 },
        { hour: '2016-01-04 19:00', pv: 60107 },
        { hour: '2016-01-04 20:00', pv: 54458 },
        { hour: '2016-01-04 21:00', pv: 54943 },
        { hour: '2016-01-04 22:00', pv: 48205 },
        { hour: '2016-01-04 23:00', pv: 42506 },
        ],
        xkey: ['hour'],
        ykeys: ['pv'],
        labels: ['pv']
    });
</script>
</body>
</html>

GoAccess结果可直接点击上面例子中的链接
