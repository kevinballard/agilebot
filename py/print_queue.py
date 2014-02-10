"""Module for managing submitting jobs to a CUPS printer.
"""

import os
import tempfile
import threading
import time
import traceback

import cups

# Default printer device name.
_DEFAULT_PRINTER = 'QL-700'

# Singleton PrintQueue.
_PRINT_QUEUE = None

class PrintQueue(object):
  """Class for managing a queue of jobs sent to the CUPS service.
  """

  def __init__(self, printer):
    """
    Args:
      printer - Printer device name to print to (as known by CUPS).
    """
    self.printer = printer
    self.temp_files = []

    self.conn = cups.Connection()

    threading.Timer(60, self._flush_temp_files).start()

  def send_to_printer(self, bytes):
    """Send a byte string as a job to the printer.

    Args:
      bytes - Bytes to send to the printer as a job (e.g. a PDF).
    """
    file = tempfile.NamedTemporaryFile(prefix='_agile_bot', delete=False)
    file.write(bytes)
    file.close()

    now = int(time.time())
    self.conn.printFile(
        self.printer,
        file.name,
        'agile_bot_%s' % now,
        {'orientation-requested': '4'})

    self.temp_files.append((file.name, now))

  def _flush_temp_files(self):
    """Delete temporary files after 10 minutes. (This must be done after a
    delay because there is no way to confirm when CUPS is done with the file;
    so we assume that 10 minutes is enough).
    """
    cutoff = time.time() - 600
    while self.temp_files and self.temp_files[0][1] < cutoff:
      to_delete = self.temp_files.pop(0)
      try:
        os.remove(to_delete[0])
      except Exception, e:
        traceback.print_exc(e)

def initialize_queue(printer=_DEFAULT_PRINTER):
  """Initialize the PrintQueue.

  Args:
    printer - Printer device name to print to (as known by CUPS).
  """
  global _PRINT_QUEUE
  if _PRINT_QUEUE is not None:
    raise Exception('PrintQueue is already initialized.')

  _PRINT_QUEUE = PrintQueue(printer)

def send_to_print_queue(bytes):
  """Send a byte string as a job to the PrintQueue.

  Args:
    bytes - Byte string to send to the PrintQueue as a job (e.g. a PDF).
  """
  global _PRINT_QUEUE
  if _PRINT_QUEUE is None:
    raise Exception('PrintQueue is not initialized.')
  _PRINT_QUEUE.send_to_printer(bytes)
