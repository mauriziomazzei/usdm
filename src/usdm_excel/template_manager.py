from usdm_excel.base_manager import BaseManager
from usdm_excel.errors_and_logging.errors_and_logging import ErrorsAndLogging

class TemplateManager(BaseManager):
  
  DEFAULT_TEMPLATE_NAME = 'SPONSOR'
  DEFAULT_SHEET_NAME = 'document'

  def __init__(self, errors_and_logging: ErrorsAndLogging):
    super().__init__(errors_and_logging)
    self.add(self.DEFAULT_TEMPLATE_NAME, self.DEFAULT_SHEET_NAME)
    self.default_template = self.DEFAULT_TEMPLATE_NAME

  def tidy(self, sheet_names_present: list):
    #print(f"TIDY 1: {sheet_names_present}, {current_template}")
    new_items = {}
    for template, sheet in self._items.items():
      #print(f"TIDY 2: {template}, {sheet}")
      if sheet in sheet_names_present:
        new_items[template] = sheet
    self._items = new_items
    
