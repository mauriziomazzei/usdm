import traceback
from usdm_excel.base_sheet import BaseSheet
from usdm_model.activity import Activity
from usdm_excel.managers import Managers
from usdm_excel.utility import general_sheet_exception
from usdm_excel.utility import general_sheet_exception

class StudyDesignActivitySheet(BaseSheet):

  SHEET_NAME = 'studyDesignActivities'

  def __init__(self, file_path: str, managers: Managers):
    try:
      super().__init__(file_path=file_path, managers=managers, sheet_name=self.SHEET_NAME, optional=True)
      self.items = []
      if self.success:
        for index, row in self.sheet.iterrows():
          name = self.read_cell_by_name(index, ['activityName', 'name'])
          description = self.read_cell_by_name(index, ['activityDescription', 'description'])
          label = self.read_cell_by_name(index, 'label', default="", must_be_present=False)
          try:
            item = Activity(
              id=self.managers.id_manager.build_id(Activity), 
              name=name,
              description=description,
              label=label
            )
          except Exception as e:
            self._general_error(f"Failed to create Activity object, exception {e}")
            self._traceback(f"{traceback.format_exc()}")
          else:
            self.items.append(item)
            self.managers.cross_references.add(name, item)     
        self.double_link(self.items, 'previousId', 'nextId')   
    except Exception as e:
      general_sheet_exception(self.SHEET_NAME, e)

