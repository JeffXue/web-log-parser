## web-log-parser
**web-log-parser**为开源的分析web日志工具，采用python语言开发，具有灵活的日志格式配置。

---

## 样例
![样例图片](https://raw.githubusercontent.com/JeffXue/web-log-parser/master/example.png)

---

## 使用方法
1. 将需要分析的日志存放到data目录下
2. 配置config.ini
3. 安装依赖`pip install -r requirements.txt`
3. bin目录下运行`python start.py`
4. 查看结果：result/目录下的index.html（result/report/目录下将生成对应的分析结果）

---

## 配置说明

### format
- log-pattern 解析日志的正则表达式
- log-format 日志内容格式，用于本工具，每项对应log-pattern匹配项，默认支持统计以下配置项：
    - ip：用户IP
    - real_ip：用户真实IP，若配置了该项将忽略ip的统计，而使用real_ip进行统计
    - datetime：请求访问时间
    - url：请求url
    - method：请求方法
    - protocol：请求协议
    - cost： 请求耗时

### filter
- support_method 支持的URL Method，否则不进行统计
- is_with_parameters 统计URL参数启用标志位，默认将转换URL中参数，如?key=123统计时转换为key={key}
- urls_most_number 配置单独统计的URL最大数量
- custom_parameters 配置特殊的参数键值对，以逗号分隔，配置的t={timeStamp}，在分析参数时会将t键的值替换为固定的{timeStamp}
- fixed_parameter_keys 配置特殊的参数key值，以逗号分隔，参数中的key=123，不会被置换为key={key}
- ignore_urls URL过滤器
- static-file 需要过滤的静态文件后缀

### report
- second_line_flag 每秒PV曲线图启用标志位
- cost_time_flag 响应时间区间占比图及响应时间分布图启用标志位

### goaccess
- goaccess_flag 是否获取GoAccess分析结果，设置为1：获取，0:不获取（需要已安装GoAccess）
- time-format 日志中的时间格式，用于GoAccess
- date-format 日志中的日期格式，用于GoAccess
- goaccess-log-format 日志格式，用于GoAccess





    

