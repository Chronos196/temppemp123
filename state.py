from enum import Enum

class State(Enum):
    OBJECT = 'object'
    CONTRACTOR = 'contractor'
    PEOPLE = 'people'
    EQUIPMENT = 'equipment'
    REPORT_DATE = 'report_date'
    NOTES = 'notes'
    WORK_PLAN = 'work_plan'
    PHOTO = 'photo'
    END = 'end'

class CallBack(Enum):
    SEND = 'send'
    CANCEL = 'cancel'
    OBJECT = 'obj'
    CONTRACTOR = 'con'
    YES = 'yes'
    NO = 'no'
