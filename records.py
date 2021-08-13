from faust import Record, serializers
from faust.models import record

class UserRecord(Record, serializer='json'):
    id: str
    username: str
    gender: str
    language: str
    

class JobRecord(Record, serializer='json'):
    id: str
    


class JobImpressionRecord(Record, serializer='json'):
    user_id: str
    job_id: str