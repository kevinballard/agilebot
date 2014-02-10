"""Utilities for rendering CardInfo objects as PDF bytes.
"""

from cStringIO import StringIO

from pyPdf import PdfFileWriter, PdfFileReader
from xhtml2pdf import pisa

def render_card_html(card_info):
  """Convert a single CardInfo into an HTML document.

  Args:
    card_info - CardInfo object.

  Returns:
    HTML document string.
  """
  return _TEMPLATE.render(**{
      'name': card_info.name,
      'taskid': card_info.taskid,
      'hours': card_info.hours,
      'risk': card_info.risk,
      'description': card_info.description})

def render_card_pdf(card_info):
  """Convert a single CardInfo into PDF bytes.

  Args:
    card_info - CardInfo object.

  Returns:
    Byte string of the rendered PDF.
  """
  stream = StringIO()
  pisa.CreatePDF(_MakeHtml(card_info), stream)
  return stream.getvalue()

def render_multiple_cards_pdf(card_infos):
  """Convert a list of CardInfo objects into a multi-page PDF.

  Args:
    card_infos - List of CardInfo objects.

  Returns:
    Byte string of the rendered multi-page PDF.
  """
  pdf_writer = PdfFileWriter()

  for card_info in card_infos:
    card_pdf = RenderCard(card_info)
    pdf_writer.addPage(PdfFileReader(StringIO(card_pdf)).getPage(0))

  all_bytes = StringIO()
  pdf_writer.write(all_bytes)

  return all_bytes.getvalue()
