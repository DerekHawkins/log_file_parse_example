import re
import pandas as pd
from dateutil.parser import parse

def log_parse(data):
    # Response Size
    try:
        size = re.search(r'[0-9] (\d{1,4})', data).group(1)
    except AttributeError as e:
        size = 'n/a'
        
    # Server Response    
    try:
        server_response = re.search(r'http.*?[\"]', data).group(0).replace('"', '')
    except AttributeError as e:
        server_response = 'n/a'
        
    # Date Parameter
    original_date_time_str = re.sub(r':.*', '', re.search(r'\[.*\]', data).group(0).split()[0].replace('[', ''))
    date = parse(timestr=original_date_time_str)
    date_str = date.strftime('%m/%d/%Y')
    
    # Client Request
    requested_element = re.search(r'"(GET|POST|PUT).*" [0-9]', data).group(0)
    if 'GET' in requested_element:
        request_type = 'GET'
        requested_element = requested_element.replace('"GET ', '')
    elif 'POST' in requested_element:
        request_type = 'POST'
        requested_element = requested_element.replace('"POST ', '')
    elif 'PUT' in requested_element:
        request_type = 'PUT'
        requested_element = requested_element.replace('"PUT ', '')
    main_request = re.sub('" [0-9]', '', requested_element).split(' ')[0]
    
    log_dict = {
        'ip_address':re.match(r'.* - -', data).group(0).replace(' - -', ''), 
        'date':date_str, 
        'client_request': main_request,
        'request_method': request_type,
        'status_code': re.search(r'" \d{1,3}', data).group(0).replace('" ', ''), 
        'size': size, 
        'server_response':server_response,
        'user_agent':re.search(r'\" \".*?\"', data).group(0).replace('"', '').strip(), 
        'host':re.search(r' host=.*? ', data).group(0).strip().replace('host=', '')
    }
    return log_dict

log_file_path = r"/path/to/log_file.log"
log_data = []
with open(log_file_path, "r") as file:
    for line in file:
        log_data.append(log_parse(line))
        
df = pd.DataFrame(log_data)
