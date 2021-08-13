from worker import app
from constants import topics
from records import UserRecord, JobRecord, JobImpressionRecord

# Defining topics:
users_topic = app.topic(
    topics['user'], 
    partitions=3, 
    retention=7, 
    internal=True,
    key_type=str,
    value_type=UserRecord
)

jobs_topic = app.topic(
    topics['job'], 
    partitions=3, 
    retention=7, 
    internal=True,
    key_type=str,
    value_type=JobRecord
)

job_impressions_topic = app.topic(
    topics['job_impression'], 
    partitions=1, 
    retention=2, 
    internal=True,
    key_type=str,
    value_type=JobImpressionRecord
)

user_enriched_job_impression_topic = app.topic(
    topics['user_enriched_job_impression'], 
    partitions=1, 
    retention=1, 
    internal=True,
    key_type=str,
    value_type=JobImpressionRecord
)

fully_enriched_job_impression_topic = app.topic(
    topics['enriched_job_impression'], 
    partitions=1, 
    retention=2, 
    internal=True,
    key_type=str,
    value_type=JobImpressionRecord
)