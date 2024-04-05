from usdm_excel.base_sheet import BaseSheet
from usdm_excel.cross_ref import cross_references
from usdm_excel.id_manager import id_manager
import traceback
import pandas as pd
from usdm_model.procedure import Procedure

class StudyDesignProcedureSheet(BaseSheet):

  def __init__(self, file_path, manager):
    try:
      super().__init__(file_path=file_path, manager=manager, sheet_name='studyDesignProcedures')
      self.procedures = []
      for index, row in self.sheet.iterrows():
        xref = self.read_cell_by_name(index, "xref", default="", must_be_present=False)
        name = self.read_cell_by_name(index, ["procedureName", 'name'])
        description = self.read_cell_by_name(index, ['procedureDescription', 'description'])
        label = self.read_cell_by_name(index, 'label', default="", must_be_present=False)
        type = self.read_cell_by_name(index, "procedureType")
        code = self.read_other_code_cell_by_name(index, ['procedureCode', 'code'])
        #conditional = self.read_boolean_cell_by_name(index, 'procedureIsConditional')
        #reason = self.read_cell_by_name(index, 'procedureIsConditionalReason')
        try:
          item = Procedure(id=self.managers.id_manager.build_id(Procedure),
            name=name,
            description=description,
            label=label,
            procedureType=type, 
            code=code 
            #isConditional=conditional, 
            #isConditionalReason=reason
          )
        except Exception as e:
          self._general_error(f"Failed to create Procedure object, exception {e}")
          self._traceback(f"{traceback.format_exc()}")
        else:
          self.procedures.append(item)
          cross_ref = xref if xref else name
          self.managers.cross_references.add(cross_ref, item)        
    except Exception as e:
      self._general_error(f"Exception '{e}' raised reading sheet.")
      self._traceback(f"{traceback.format_exc()}")
