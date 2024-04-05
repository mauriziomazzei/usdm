import traceback
import pandas as pd
from usdm_excel.base_sheet import BaseSheet
from usdm_model.study_element import StudyElement
from usdm_model.transition_rule import TransitionRule
from usdm_excel.managers import Managers
from usdm_excel.utility import general_sheet_exception

class StudyDesignElementSheet(BaseSheet):

  SHEET_NAME = 'studyDesignElements'

  def __init__(self, file_path: str, managers: Managers):
    try:
      super().__init__(file_path=file_path, managers=managers, sheet_name=self.SHEET_NAME)
      self.items = []
      for index, row in self.sheet.iterrows():
        start_rule = None
        end_rule = None
        xref = self.read_cell_by_name(index, 'xref', default="", must_be_present=False)
        name = self.read_cell_by_name(index, ['studyElementName', 'name'])
        description = self.read_cell_by_name(index, ['studyElementDescription', 'description'])
        label = self.read_cell_by_name(index, 'label', default="", must_be_present=False)
        start_rule_text = self.read_cell_by_name(index, 'transitionStartRule')
        end_rule_text = self.read_cell_by_name(index, 'transitionEndRule')
        if start_rule_text:
          start_rule = TransitionRule(id=self.managers.id_manager.build_id(TransitionRule), name=f"ELEMENT_START_RULE_{index + 1}", text=start_rule_text)
        if end_rule_text:
          end_rule = TransitionRule(id=self.managers.id_manager.build_id(TransitionRule), name=f"ELEMENT_END_RULE_{index + 1}", text=end_rule_text)
        try:
          item = StudyElement(
            id=self.managers.id_manager.build_id(StudyElement), 
            name=name,
            description=description,
            label=label,
            transitionStartRule=start_rule,
            transitionEndRule=end_rule
          )
        except Exception as e:
          self._general_error(f"Failed to create StudyElement object, exception {e}")
          self._traceback(f"{traceback.format_exc()}")
        else:
          self.items.append(item)
          cross_ref = xref if xref else name
          self.managers.cross_references.add(cross_ref, item)     
    except Exception as e:
      general_sheet_exception(self.SHEET_NAME, e)

