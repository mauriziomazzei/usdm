class IdManager():

  def __init__(self):
    self.id_index = {
      'Address': 0,
      'Code': 0,
      'AliasCode': 0,
      'Organisation': 0,
      'StudyIdentifier': 0,
      'StudyEpoch': 0,
      'StudyArm': 0,
      'StudyCell': 0,
      'Entry': 0, 
      'ScheduleTimelineExit': 0, 
      'ScheduledActivityInstance': 0,
      'ScheduleTimeline': 0, 
      'Timing': 0, 
      'StudyDesign': 0, 
      'Study': 0, 
      'Activity': 0, 
      'Encounter': 0, 
      'BiomedicalConceptSurrogate': 0, 
      'BiomedicalConcept': 0,
      'BiomedicalConceptProperty': 0,
      'ResponseCode': 0,
      'InvestigationalIntervention': 0,
      'Indication': 0
    }

  def build_id(self, klass):
    klass_name = str(klass.__name__)
    self.id_index[klass_name] += 1
    return "%s_%s" % (klass_name, self.id_index[klass_name])


