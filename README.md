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
- special_parameter_keys 配置特殊的参数key值，以逗号分隔，参数中的key=123，不会被置换为key={key}
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
<head>
<title>AutoTestReport</title>
</head>
<body>
    <h1 align="center">WebLogPaser</h1>
    <table class="details" border="0" align="center" width="80%">
        <caption align="left">Overall Analyzed Requests</caption>
        <tr valign="top">
            <td style="BACKGROUND: #a6caf0" align="center" vertical-align="middle" class="cell"><strong>日志文件</strong></td>
            <td style="background:#BFBFBF;font-weight:bold;color:green;" colspan="3"><strong>access_log_domain_20150506</strong></td>
            <td style="background:#BFBFBF;font-weight:bold;color:green;">
                <a href="#" target="_goaccess">查看GoAccess生成报告</a>
            </td>
        </tr>
        <tr valign="top">
            <td style="BACKGROUND: #a6caf0" align="center" vertical-align="middle" class="cell"><strong>总PV</strong></td>
            <td style="BACKGROUND: #a6caf0" align="center" vertical-align="middle" class="cell"><strong>总UV</strong></td>
            <td style="BACKGROUND: #a6caf0" align="center" vertical-align="middle" class="cell"><strong>每秒最大处理消息数量</strong></td>
            <td style="BACKGROUND: #a6caf0" align="center" vertical-align="middle" class="cell"><strong>最大处理消息时间</strong></td>
            <td style="BACKGROUND: #a6caf0" align="center" vertical-align="middle" class="cell"><strong>每秒平均处理消息</strong></td>
        </tr>
        <tr valign="top">
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>561066</strong></td>
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>50501</strong></td>
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>136</strong></td>
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>06/May/2015:11:51:12</strong></td>
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>8</strong></td>
        </tr>
    </table>
    <table class="details" border="0" align="center" width="80%%">
        <caption align="left">Top requests(URLS)</caption>
        <tr valign="top">
            <td style="BACKGROUND: #a6caf0" align="center" vertical-align="middle" class="cell"><strong>Requests</strong></td>
            <td style="BACKGROUND: #a6caf0" align="center" vertical-align="middle" class="cell"><strong>访问量</strong></td>
            <td style="BACKGROUND: #a6caf0" align="center" vertical-align="middle" class="cell"><strong>比例</strong></td>
            <td style="BACKGROUND: #a6caf0" align="center" vertical-align="middle" class="cell"><strong>每秒最大处理消息数量</strong></td>
            <td style="BACKGROUND: #a6caf0" align="center" vertical-align="middle" class="cell"><strong>Protocol</strong></td>
            <td style="BACKGROUND: #a6caf0" align="center" vertical-align="middle" class="cell"><strong>Method</strong></td>
        </tr>
        <tr valign="top">
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>/uc_server/avatar.php</strong></td>
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>194084</strong></td>
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>34.592%</strong></td>
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>75</strong></td>
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>"GET</strong></td>
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>HTTP/1.1"</strong></td>
        </tr>
        <tr valign="top">
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>/forum.php</strong></td>
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>95833</strong></td>
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>17.081%</strong></td>
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>96</strong></td>
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>"GET</strong></td>
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>HTTP/1.1"</strong></td>
        </tr>
        <tr valign="top">
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>/topic.php</strong></td>
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>75987</strong></td>
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>13.543%</strong></td>
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>27</strong></td>
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>"GET</strong></td>
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>HTTP/1.1"</strong></td>
        </tr>
        <tr valign="top">
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>/misc.php</strong></td>
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>73379</strong></td>
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>13.078%</strong></td>
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>26</strong></td>
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>"POST</strong></td>
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>HTTP/1.1"</strong></td>
        </tr>
        <tr valign="top">
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>/home.php</strong></td>
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>19729</strong></td>
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>3.516%</strong></td>
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>10</strong></td>
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>"GET</strong></td>
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>HTTP/1.1"</strong></td>
        </tr>
        <tr valign="top">
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>/</strong></td>
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>8280</strong></td>
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>1.476%</strong></td>
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>7</strong></td>
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>"GET</strong></td>
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>HTTP/1.1"</strong></td>
        </tr>
        <tr valign="top">
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>/setusername.php</strong></td>
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>8129</strong></td>
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>1.449%</strong></td>
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>10</strong></td>
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>"POST</strong></td>
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>HTTP/1.1"</strong></td>
        </tr>
        <tr valign="top">
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>/setusername.php</strong></td>
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>7698</strong></td>
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>1.372%</strong></td>
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>7</strong></td>
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>"GET</strong></td>
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>HTTP/1.1"</strong></td>
        </tr>
        <tr valign="top">
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>/forum-37-1.html</strong></td>
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>6782</strong></td>
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>1.209%</strong></td>
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>2</strong></td>
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>"GET</strong></td>
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>HTTP/1.1"</strong></td>
        </tr>
        <tr valign="top">
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>/api/getdata.php</strong></td>
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>3045</strong></td>
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>0.543%</strong></td>
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>6</strong></td>
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>"GET</strong></td>
            <td style="background:#BFBFBF;font-weight:bold;color:green;"><strong>HTTP/1.0"</strong></td>
        </tr>
    </table>
</body>
</html>

GoAccess请参考http://goaccess.io/goaccess_html_report.html?src=gh
