from worker import app
from constants import topics
from records import UserRecord, JobRecord, JobImpressionRecord

user_table = app.Table(
    name='user_table',
    default=UserRecord
)

job_table = app.Table(
    name='job_table',
    default=JobRecord
)