"""Script to convert a JIRA XML query into agilebot JSON format.
"""

import requests
import json
from xml.etree import ElementTree

from commandr import command, Run

_AGILEBOT_HOST = 'http://192.168.128.74/'

@command('convert')
def ConvertXmlFileToJson(xml_path):
  """
  """
  with open(xml_path) as f:
    return ConvertXmlToJson(f.read())

@command('render')
def RenderXml(xml_path):
  """
  """
  json_data = ConvertXmlFileToJson(xml_path)

  url = _AGILEBOT_HOST + 'rendermulti'
  response = requests.post(url, data=json_data)

  print response.text

@command('print')
def PrintXml(xml_path, really=False):
  """
  """
  json_data = ConvertXmlFileToJson(xml_path)

  really_arg = '?really=true' if really else ''
  url = _AGILEBOT_HOST + 'printmulti' + really_arg
  response = requests.post(url, data=json_data)

  print response.text

def ConvertXmlToJson(xml_text):
  """
  """
  root = ElementTree.fromstring(xml_text)
  items = root.find('channel').findall('item')

  tasks = []
  for item in items:
    task = {}

    key_node = item.find('key')
    task['taskid'] = key_node.text if key_node is not None else 'noid'
  
    assignee_node = item.find('assignee')
    task['name'] = assignee_node.text if assignee_node is not None else 'nobody'
  
    summary_node = item.find('summary')
    if summary_node is not None and summary_node.text:
      task['description'] = summary_node.text
  
    time_node = item.find('timeestimate')
    if time_node is not None and time_node.get('seconds'):
      seconds = time_node.get('seconds')
      task['hours'] = int(seconds) / 3600
  
    tasks.append(task)
  
  return json.dumps(tasks)

if __name__ == '__main__':
  Run()
