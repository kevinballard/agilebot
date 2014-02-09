
from cStringIO import StringIO
import json

from flask import Flask, make_response, request
from pyPdf import PdfFileWriter, PdfFileReader

import agile_bot

app = Flask(__name__)

@app.route("/")
def index():
  return "Hello"

@app.route('/render')
def render():
  html = agile_bot.MakeHtml(
      request.args.get('name', 'John Doe'),
      request.args.get('taskid', '0'),
      request.args.get('hours', '0'),
      request.args.get('risk', 'N'),
      request.args.get('description', '...'))
  pdf = agile_bot.MakePdf(html)

  response = make_response(pdf)
  response.headers['Content-Type'] = 'application/pdf'
  return response

@app.route('/rendermulti', methods=['GET', 'POST'])
def renderMulti():
  params = request.get_json(force=True)
  
  pdf_writer = PdfFileWriter()

  for args in params:
    html = agile_bot.MakeHtml(**args)
    pdf = agile_bot.MakePdf(html)

    pdf_writer.addPage(PdfFileReader(StringIO(pdf)).getPage(0))

  output_stream = StringIO()
  pdf_writer.write(output_stream)

  response = make_response(output_stream.getvalue())
  response.headers['Content-Type'] = 'application/pdf'
  return response

@app.route('/printmulti', methods=['GET', 'POST'])
def printMulti():
  params = request.get_json(force=True)

  pdf_writer = PdfFileWriter()

  for args in params:
    html = agile_bot.MakeHtml(**args)
    pdf = agile_bot.MakePdf(html)

    pdf_writer.addPage(PdfFileReader(StringIO(pdf)).getPage(0))

  output_stream = StringIO()
  pdf_writer.write(output_stream)

  pdf = output_stream.getvalue()

  agile_bot.PrintStream(pdf)

  return "Ok"

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80, debug=True)

