## web-log-parser
**web-log-parser** is an open source analysis web log tool, developed in python language, with flexible log format configuration

[中文说明文档](https://github.com/JeffXue/web-log-parser/blob/master/README_ch.md)

---

## Example
![example picture](https://raw.githubusercontent.com/JeffXue/web-log-parser/master/example_en.png)

---

## Instructions
1. store the logs files in the data directory `./data`
2. modify config.ini
3. install requirements `pip install -r requirements.txt`
3. start the analysis in bin dir`cd ./bin && python start.py`
4. check html result in result dir `result/index.html`

---

## Configuration

### Format
- log-pattern: regular expression for parsing logs
- log-format: log content format, corresponding log-pattern match. The following configuration items are supported by default.：
    - ip： request IP
    - real_ip： user real IP. If this option is configured, ip configuration will be ignored, and real_ip will be used for statistics.
    - datetime： request access time
    - url： request url
    - method： request method
    - protocol： request protocol
    - cost: request cost

### Filter
- support_method: supported request method, otherwise no statistics
- is_with_parameters: enable flag for statistics url parameter，By default, the parameters in the URL will be converted, such as? Key = 123 when converting to key = {key}
- urls_most_number: the maximum number of URLs separately counted
- custom_parameters: configure special parameter key-value pairs, separated by commas, when configured t = {timeStamp}, the value of t key will be replaced with a fixed {timeStamp}
- fixed_parameter_keys: configure special parameter key values, separated by commas, when configured key = 123,  will not be replaced with key = {key}
- ignore_urls: urls will be ignore
- static-file: file suffixes will be ignore

### Report
- language: the language use in the report
    - chinese
    - english
- second_line_flag: enable flags for PV curve graph per second
- cost_time_flag: enable flags for response time interval proportion map and response time distribution map

### GoAccess
- goaccess_flag: whether to get GoAccess analysis results, set to 1: Get, 0: Do not get (requires GoAccess installed)
- time-format: time format, for GoAccess
- date-format: date format, for GoAccess
- goaccess-log-format: log format，for GoAccess





    

