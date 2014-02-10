"""Main server for agilebot.
"""

from flask import Flask
from flask import abort, make_response, request

import card_info
import print_queue
import render

app = Flask(__name__)

@app.route('/render')
def render_card():
  """Render a Card.

  GET Params:
    name - CardInfo name.
    taskid - CardInfo taskid.
    hours - CardInfo hours.
    risk - CardInfo risk.
    description - CardInfo description.

  Returns:
    Rendered PDF document.
  """
  info = card_info.from_dict(request.args)
  pdf = render.render_card_pdf(info)

  response = make_response(pdf)
  response.headers['Content-Type'] = 'application/pdf'
  return response

@app.route('/rendermulti', methods=['GET', 'POST'])
def render_multiple_cards():
  """Render multiple Cards.

  POST Document:
    JSON encoded list of dicts, containing CardInfo fields.
    e.g.:
      [ {"name": "Kevin", "taskid": 42, "hours": 8, "description": ""},
      {"name": "Kevin", "taskid": 43, "risk": "U", "description": ""} ]

  Returns:
    Rendered multi-page PDF document.
  """
  decoded_params = request.get_json(force=True)
  if type(decoded_params) is not list:
    abort(400, 'Malformed request')

  infos = [card_info.from_dict(params) for params in decoded_params]
  pdf = render.render_multiple_cards_pdf(infos)

  response = make_response(pdf)
  response.headers['Content-Type'] = 'application/pdf'
  return response

@app.route('/print')
def print_card():
  """Print a Card.

  GET Params:
    name - CardInfo name.
    taskid - CardInfo taskid.
    hours - CardInfo hours.
    risk - CardInfo risk.
    description - CardInfo description.
    really - Will only actually print the Card if this is present and evaluates
        to True.
  """
  info = card_info.from_dict(request.args)
  pdf = render.render_card_pdf(info)

  really = bool(request.args.get('really', False))
  if really:
    print_queue.send_to_print_queue(pdf)
    return "Added to queue"

  else:
    return "Ok, but not queued (use 'really' param)"

@app.route('/printmulti', methods=['GET', 'POST'])
def print_multiple_cards():
  """Print multiple cards.

  GET Params:
    really - Will only actually print the Cards if this is present and
        evaluates to True.

  POST Document:
    JSON encoded list of dicts, containing CardInfo fields.
    e.g.:
      [ {"name": "Kevin", "taskid": 42, "hours": 8, "description": ""},
      {"name": "Kevin", "taskid": 43, "risk": "U", "description": ""} ]

  """
  decoded_params = request.get_json(force=True)
  if type(decoded_params) is not list:
    abort(400, 'Malformed request')

  infos = [card_info.from_dict(params) for params in decoded_params]
  pdf = render.render_multiple_cards_pdf(infos)

  really = bool(request.args.get('really', False))
  if really:
    print_queue.send_to_print_queue(pdf)
    return "Added to queue"

  else:
    return "Ok, but not queued (use 'really' param)"

if __name__ == '__main__':
  print_queue.initialize_queue()
  app.run(host='0.0.0.0', port=80)
