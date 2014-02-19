"""Utilities for specifying and rendering Cards as PDF bytes.
"""

_DEFAULT_NAME = 'John Doe'
_DEFAULT_TASKID = 'TA-0'
_DEFAULT_HOURS = '0'
_DEFAULT_RISK = ''
_DEFAULT_DESCRIPTION = 'Figure out how to set the description.'

class CardInfo(object):
  __slots__ = ['name', 'taskid', 'hours', 'risk', 'description']

  def __init__(self,
      name=None, taskid=None, hours=None, risk=None, description=None):
    self.name = name if name is not None else _DEFAULT_NAME
    self.taskid = taskid if taskid is not None else _DEFAULT_TASKID
    self.hours = hours if hours is not None else _DEFAULT_HOURS
    self.risk = risk if risk is not None else _DEFAULT_RISK
    self.description = \
        description if description is not None else _DEFAULT_DESCRIPTION

def from_dict(params_dict):
  """Convert a dict into a CardInfo object.

  Args:
    params_dict - A Dict to extract fields from.

  Returns:
    CardInfo object.
  """
  return CardInfo(
      params_dict.get('name', None),
      params_dict.get('taskid', None),
      params_dict.get('hours', None),
      params_dict.get('risk', None),
      params_dict.get('description', None))
