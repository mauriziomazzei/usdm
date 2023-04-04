# USDM CDISC / Transcelerate DDF USDM

This package provides an implementation of the Digital Data Flow (DDF) CDISC / TransCelerate Unified Study Definitions Model (USDM). Two main parts are provided:

- Within the `usdm_model` directory are a set of classes reflecting the USDM model as transported using the DDF USDM API 
- Within the `usdm_excel` directory is a class, `USDMExcel`, that can be used to import an entire study definition from an excel file and build the equivalent json as defined by the API

# Warning

When originally written, this package was not intended for public use and, consequently, only informal testing has been performed on the package. 

Formal testing has just begun. Use this at your own risk.

# Setup

Setup is via pip

`pip install usdm`

The package requires a single environment variable `CDISC_API_KEY` that should be set to your CDISC library API key. This is used to access CDISC CT and BC definitions.

See below for a simple example program.

# USDM Model

Not further information as yet.

# Excel Import

## Example Program

The following code imports an Excel file (in the appropriate structure) and processes it. The data are then exported to a file in JSON API format.

Note: The logging is not needed.
```
import logging
log = logging.basicConfig(level=logging.INFO)

import json
from usdm_excel import USDMExcel

excel = USDMExcel("source_data/simple_1.xlsx")
with open('source_data/simple_1.json', 'w', encoding='utf-8') as f:
  f.write(json.dumps(json.loads(excel.to_json()), indent=2))
```

## Format of Workbook

### General

#### Sheets

The workbook consists of several sheets each with a dedicated purpose.

- Study sheet
- Study Identifiers sheet
- Study Design sheet
- one or more Timeline sheets
- Study Design Indications and Interventions sheet
- Study Design Populations sheet
- Study Design Objectives and Endpoints sheet
- Study Design Estimands sheet
- Study Design Procedures sheet
- Study Design Encounters sheet
- Study Design Elements sheet
- Configuration sheet

The content of each sheet is described below

#### CDISC Terminology

For those cells where CDISC codes are used the user can enter either the CDISC C Code, for example `C15602`, the CDISC submission value, for example `PHASE III TRIAL`, or the preferred term, for example `Phase III Trial`

#### External Terminology

For those cells where external CT is referenced the user can enter code in the form `<code system>: <code> = <decode>`. For example `SPONSOR: A = decode 1, SPONSOR: B = decode 2`.

### Study Sheet

#### Sheet Name

`study`

#### Sheet Contents

The study sheet consists of two parts, the upper section for those single values and then a section for the potentially repeating protocol version informaion

For the single values, the keyword is in column A while the value is in column B. The order of the fields cannot be changed.

| Row Name | Description | Format and Values |
| :--- | :--- | :--- |
| studyTitle | The study title | Text string |
| studyVersion | String version | Text string |
| studyType | The study type | CDISC code reference |
| studyPhase | The study phase | CDISC code reference |
| studyAcronym | The study acronym | Text string |
| studyRationale | the study rationale | Text string |
| businessTherapeuticAreas | The set of business therapuetic area codes | External CT code format. Likely filled with sponsor terms |

For each Study Protocol Version a row containing:

| Column Name | Description | Format and Values |
| :--- | :--- | :--- |
| briefTitle | The brief title | Text string | 
| officialTitle	 | The officiall title | Text string| 
| publicTitle	 | The public title | Text string| 
| scientificTitle	 | The scientific title | Text string| 
| protocolVersion	 | The version of the protocol | Text string | 
| protocolAmendment	 |The version amendment | Text string | 
| protocolEffectiveDate	 | Effective date of the protocol | Date field, dd/mm/yyyy | 
| protocolStatus | The status | CDISC code reference | 

### Study Identifiers	Sheet
	
#### Sheet Name

`studyIdentifiers`

#### Sheet Contents

| Column Name | Description | Format and Values |
| :--- | :--- | :--- |
| organisationIdentifierScheme | The scheme for the organisation identifier.  | Example would be 'DUNS' |
| organisationIdentifier | Organisation identifier | Text string |
| organisationName | Organisation name | Text string |
| organisationType | Organisation type | CDISC code reference |
| studyIdentifier | The identifier for the study | Text string |
| organisationAddress | The organisation address | Formated using a pipe delimited - allows for commas in items within the address - form, i.e. `line|city|district|state|postal_code|<country code>`. All fields are Text string except for `<country code>`. `<country code>` is either a two or three character ISO-3166 country code. |

### Study Design sheet

#### Sheet Name

`studyDesign`

#### Sheet Contents

The study design sheet consists of two parts, the upper section for those single values and then a section for the arms and epochs.

For the single values, the keyword is in column A while the value is in column B. The order of the fields cannot be changed.

| Row Name | Description | Format and Values |
| :--- | :--- | :--- |
| studyDesignName | Study design name | Text string |
| studyDesignDescription | Study design description | Text string |
| therapeuticAreas | Set of therapeutic area codes | Set of external CT references, comma separated |
| studyDesignRationale | Study design rationale | Text string |
| studyDesignBlindingScheme | Code for the blinding scheme | CDISC code reference |
| trialIntentTypes | Codes for the trial intent types | Comma separated string. Set of C Code, the submission value or the preferred term for the terms desired. |
| trialTypes | Code for the trial type | CDISC code reference|
| interventionModel | | CDISC code reference |
| mainTimeline | Name of main timeline sheet | This must be present |
| otherTimelines | Names of other timeline sheets | Commma separated list of sheet names. Can be empty |

For the arms and epochs, a simple table is required. The table starts in row 12 and can consists of a header row and 1 or more arm rows. 

The header row consists of a cell that is ignored followed by 1 or more cells containing the epoch names.

The arm rows consist of the arm name in the first column followed by a cells for each epoch containing one or more references to study design elements defined in the studyDesignElements sheet.

### Timeline sheets

#### Sheet Name

As defined within the study design sheet, see above.

#### Sheet Contents

### Study Design Indications and Interventions Sheet
	
#### Sheet Name

`studyDesignII`

#### Sheet Contents

| Column Name | Description | Format and Values |
| :--- | :--- | :--- |
| type | The type, either IND for indication or INT for intervention | Text string |
| description | A Text string description for the indication or intervvention | Text string |
| codes | The set of indication or intervention codes | A set of external CT codes, comma separated |	

### Study Design Populations sheet

#### Sheet Name

`studyDesignPopulations`

#### Sheet Contents




### Study Design Objectives and Endpoints sheet

#### Sheet Name

`studyDesignOE`

#### Sheet Contents




### Study Design Estimands sheet

#### Sheet Name

`studyDesignEstimands`

#### Sheet Contents




### Study Design Procedures sheet

#### Sheet Name

`studyDesignProcedures`

#### Sheet Contents




### Study Design Encounters sheet

#### Sheet Name

`studyDesignEncounters`

#### Sheet Contents




### Study Design Elements sheet

#### Sheet Name

`studyDesignElements`

#### Sheet Contents




### Configuration Sheet

#### Sheet Name

`configuration`

#### Sheet Contents

A set of rows consisting of configuration parameters. The first column is the type of configuration parameter while the second is the value. The values for specific parameters may vary in their format

| Parameter | Description | Format and Values |
| :--- | :--- | :--- |
| CT Version | Allows for the version of a specific external CT to be set. Multiple rows can be included to set the versions for several CTs | Of the form CT name = Version value, For example `SNOMED = 21st June 2012`|

### Content Not Suported As Yet

It is intended to support all of the content in the USDM. The following features are not yet supported:

- Full Arm definitions
- Full Epoch definitions