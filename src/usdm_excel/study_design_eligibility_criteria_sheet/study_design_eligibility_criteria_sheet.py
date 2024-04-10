import re
import traceback
from usdm_excel.base_sheet import BaseSheet
from usdm_model.eligibility_criterion import EligibilityCriterion
from usdm_model.syntax_template_dictionary import SyntaxTemplateDictionary
from usdm_excel.globals import Globals

class StudyDesignEligibilityCriteriaSheet(BaseSheet):

  SHEET_NAME = 'studyDesignEligibilityCriteria'
  
  def __init__(self, file_path: str, globals: Globals):
    try:
      super().__init__(file_path=file_path, globals=globals, sheet_name=self.SHEET_NAME, optional=True)
      self.items = []
      if self.success:
        for index, row in self.sheet.iterrows():
          category = self.read_cdisc_klass_attribute_cell_by_name('EligibilityCriteria', 'category', index, 'category')
          identifier = self.read_cell_by_name(index, 'identifier')
          name = self.read_cell_by_name(index, 'name')
          description = self.read_cell_by_name(index, 'description')
          label = self.read_cell_by_name(index, 'label')
          text = self.read_cell_by_name(index, 'text')
          dictionary_name = self.read_cell_by_name(index, 'dictionary')
          self._validate_references(index, 'text', text, dictionary_name)
          criteria = self._criteria(name, description, label, text, category, identifier, dictionary_name)
          if criteria:
            self.items.append(criteria)
        
    except Exception as e:
      self._sheet_exception(e)

  def _criteria(self, name, description, label, text, category, identifier, dictionary_name):
    try:
      dictionary_id = self._get_dictionary_id(dictionary_name)
      item = EligibilityCriterion(
        id=self.globals.id_manager.build_id(EligibilityCriterion),
        name=name,
        description=description,
        label=label,
        text=text,
        category=category,
        identifier=identifier,
        dictionaryId=dictionary_id
      )
    except Exception as e:
      self._general_error(f"Failed to create EligibilityCriteria object", e)
      return None
    else:
      self.globals.cross_references.add(item.id, item)
      return item

  def _validate_references(self, row, column_name, text, dictionary_name):
    if dictionary_name:
      column = self.column_present(column_name)
      dictionary = self.globals.cross_references.get(SyntaxTemplateDictionary, dictionary_name)
      if not dictionary:
        self._warning(row, column, f"Dictionary '{dictionary_name}' not found")
        return
      tags = re.findall(r'\[([^]]*)\]',text)
      for tag in tags:
        entry = next((item for item in dictionary.parameterMaps if item.tag == tag), None)
        if not entry:
        #if not tag in dictionary.parameterMap:
          self._warning(row, column, f"Failed to find '{tag}' in dictionary '{dictionary_name}'")
  
  def _get_dictionary_id(self, dictionary_name):
    if dictionary_name:
      dictionary = self.globals.cross_references.get(SyntaxTemplateDictionary, dictionary_name)
      if dictionary:
        return dictionary.id
      else:
        self._general_error(f"Unable to find dictionary with name '{dictionary_name}'")
    return None
