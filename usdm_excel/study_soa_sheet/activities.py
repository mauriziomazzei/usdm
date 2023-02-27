from usdm_excel.study_soa_sheet.soa_column_rows import SoAColumnRows
from usdm_excel.study_soa_sheet.activity import Activity
import pandas as pd

class Activities:
  
  def __init__(self, sheet):
    self.sheet = sheet
    self.items = []
    self.map = {}
    for row_index, col_def in self.sheet.iterrows():
      if row_index >= SoAColumnRows.FIRST_ACTIVITY_ROW:
        activity = Activity(self.sheet, row_index)
        self.items.append(activity)
        self.map[activity.name] = activity

  def item_by_name(self, name):
    return self.map[name]