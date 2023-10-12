from typing import Literal, Union
from .api_base_model import ApiBaseModelWithIdNameLabelAndDesc
from .syntax_template_dictionary import SyntaxTemplateDictionary

class SyntaxTemplate(ApiBaseModelWithIdNameLabelAndDesc):
  instanceType: Literal['ENDPOINT', 'OBJECTIVE', 'ELIGIBILITY_CRITERIA']
  text: str = None
  dictionary: Union[SyntaxTemplateDictionary, None] = None
