
from yattag import Doc
from usdm_model.eligibility_criterion import EligibilityCriterion
from usdm_model.narrative_content import NarrativeContent
from usdm_db.fhir.to_fhir import ToFHIR
from tests.test_factory import Factory
from uuid import UUID
from bs4 import BeautifulSoup   

fake_uuid = UUID(f'00000000-0000-4000-8000-{1:012}', version=4)
  
def create_criteria(factory):
  INCLUSION = factory.cdisc_code('C25532', 'Inc')
  EXCLUSION = factory.cdisc_code('C25370', 'Exc')
  item_list = [
    {'name': 'IE1', 'label': '', 'description': '', 'text': 'Only perform at baseline', 
     'dictionaryId': None, 'category': INCLUSION, 'identifier': '01', 'nextId': None, 'previousId': None, 'contextId': None
    },
    {'name': 'IE2', 'label': '', 'description': '', 'text': '<p>Only perform on males</p>', 
    'dictionaryId': None, 'category': INCLUSION, 'identifier': '02', 'nextId': None, 'previousId': None, 'contextId': None
    },
  ]
  results = factory.set(EligibilityCriterion, item_list)
  return results

def test_create(mocker, globals, minimal, factory):
  minimal.population.criteria = create_criteria(factory)
  fhir = ToFHIR("xxx", minimal.study, globals.errors_and_logging)
  assert fhir is not None

def test_content_to_section(mocker, globals, minimal, factory):
  minimal.population.criteria = create_criteria(factory)
  fhir = ToFHIR("xxx", minimal.study, globals.errors_and_logging)
  content = factory.item(NarrativeContent, {'name': "C1", 'sectionNumber': '1.1.1', 'sectionTitle': 'Section Title', 'text': 'Something here for the text', 'childIds': []})
  result = fhir._content_to_section(content)
  expected = '{"title": "Section Title", "code": {"text": "section1.1.1-section-title"}, "text": {"status": "generated", "div": "Something here for the text"}}'
  assert result.json() == expected

def test_format_section(mocker, globals, minimal, factory):
  fhir = ToFHIR("xxx", minimal.study, globals.errors_and_logging)
  assert fhir._format_section_title('A Section Heading') == 'a-section-heading'

def test_clean_section_number(mocker, globals, minimal, factory):
  fhir = ToFHIR("xxx", minimal.study, globals.errors_and_logging)
  assert fhir._clean_section_number('1.1') == '1.1'
  assert fhir._clean_section_number('1.1.') == '1.1'

def test_add_section_heading(mocker, globals, minimal, factory):
  fhir = ToFHIR("xxx", minimal.study, globals.errors_and_logging)
  content = factory.item(NarrativeContent, {'name': "C1", 'sectionNumber': '1.1.1', 'sectionTitle': 'Section Title', 'text': '<div xmlns="http://www.w3.org/1999/xhtml">Something here for the text</div>', 'childIds': []})
  div = BeautifulSoup(content.text, 'html.parser')
  assert fhir._add_section_heading(content, div) == '<div xmlns="http://www.w3.org/1999/xhtml"><p>1.1.1 Section Title</p>Something here for the text</div>'

def test_remove_line_feeds(mocker, globals, minimal, factory):
  fhir = ToFHIR("xxx", minimal.study, globals.errors_and_logging)
  text = "<p>CNS imaging (CT scan or MRI of brain) compatible with AD within past 1 year.</p>\n<p>The following findings are incompatible with AD:</p>\n"  
  assert fhir._remove_line_feeds(text) == "<p>CNS imaging (CT scan or MRI of brain) compatible with AD within past 1 year.</p><p>The following findings are incompatible with AD:</p>"  