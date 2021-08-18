from faust import models
from tables import job_table, user_table
from topics import (job_impressions_topic, jobs_topic,
                    user_enriched_job_impression_topic, users_topic, fully_enriched_job_impression_topic)
from worker import app
import records

# Streams:

# @app.agent(users_topic)
# async def hi_users(users):
#     """This function is used for saving users in the user table.
#     Key: user_id Value: user (Record)

#     Args:
#         users
#     """
#     # Creating users topic
#     await users_topic.declare()
#     # Processing
#     async for user in users:
#         print(f'user:{user}')

@app.agent(users_topic)
async def save_users(users):
    """This function is used for saving users in the user table.
    Key: user_id Value: user (Record)

    Args:
        users
    """
    # Creating users topic
    await users_topic.declare()
    # Processing
    async for user in users:
        user_table[str(user.id)] = user
        print(f'user_id:{user.id} :saved to: user_table')


@app.agent(jobs_topic)
async def save_jobs(jobs):
    """This function is used for saving jobs in the job table.
    Key: job_id Value: job (Record)

    Args:
        jobs
    """
    # Creating jobs topic
    await jobs_topic.declare()
    # Processing:
    async for job in jobs:
        job_table[str(job.id)] = job
        print(f'job_id:{job.id} :saved to: job_table')


# @app.agent(job_impressions_topic)
# async def enrich_job_impressions_with_user(job_impressions):
#     """This function is used to enrich job_impression with user details.

#     Args:
#         job_impressions
#     """
#     async for impression in job_impressions.group_by(records.JobImpressionRecord.user_id):
#         user = user_table[impression.user_id]

#         # enrichment
#         impression.language = user.language
#         impression.gender = user.gender
#         # Pushing it to intermediate topic
#         await user_enriched_job_impression_topic.send(key=impression.id, value=impression)


# @app.agent(user_enriched_job_impression_topic)
# async def enrich_job_impressions_with_job(job_impressions):
#     """This function is used to enrich (user-enriched) job_impression with job details.

#     Args:
#         job_impressions
#     """
#     await user_enriched_job_impression_topic.declare()
#     async for impression in job_impressions.group_by(records.JobImpressionRecord.job_id):
#         job = job_table[impression.job_id]

#         # enrichment
#         # impression.language = user.language
#         # impression.gender = user.gender
#         # Pushing it to intermediate topic
#         await fully_enriched_job_impression_topic.send(key=impression.id, value=impression)
        

# @app.agent(fully_enriched_job_impression_topic)
# async def enrich_job_impressions_with_job(job_impressions):
#     """This function is used to acknowledge the job impressions.

#     Args:
#         job_impressions
#     """
#     await fully_enriched_job_impression_topic.declare()
#     async for impression in job_impressions:
#         print(f'JobImpression: {impression.id} enriched: {impression}')

# DEBUG-POC:
# qs_stream = app.topic('quickstart')
# @app.agent(qs_stream)
# async def qstart(stream):
#     async for event in stream:
#         print(f'Inside quickstart: {event}')
        
# interesting_topic = app.topic(
#     'interesting', 
#     partitions=8, 
#     retention=3, 
#     internal=True,
# )

# @app.agent(interesting_topic)
# async def qstart(stream):
#     await interesting_topic.declare()
#     async for event in stream:
#         print(f'Inside interesting: {event}')

