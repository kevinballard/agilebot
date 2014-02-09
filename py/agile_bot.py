from cStringIO import StringIO
import os
import tempfile

import cups
from mako.template import Template
from xhtml2pdf import pisa

_TEMPLATE_PATH = 'agile_bot.html'
_TEMPLATE = Template(filename=_TEMPLATE_PATH)

_DEFAULT_PRINTER = 'QL-700'

def MakeHtml(name, taskid, hours, risk, description):
  return _TEMPLATE.render(**{
      'name': name,
      'taskid': taskid,
      'hours': hours,
      'risk': risk,
      'description': description}) 

def MakePdf(html):
  stream = StringIO()
  pdf = pisa.CreatePDF(html, stream)
  return stream.getvalue()
  
def PrintStream(ps_data, device=_DEFAULT_PRINTER, landscape=True):
  file = tempfile.NamedTemporaryFile(prefix='_agile_bot', delete=False)
  file.write(ps_data)
  file.close()
  cups.Connection().printFile(
      device, file.name, '', {'orientation-requested': '4'})

def Print(name='John', taskid=0, hours=0, risk='N', description='[...]'):
  html = MakeHtml(name, taskid, hours, risk, description)
  PrintStream(MakePdf(html))

if __name__ == '__main__':
  Print()

