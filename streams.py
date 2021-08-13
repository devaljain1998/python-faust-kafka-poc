from tables import job_table, user_table
from topics import (job_impressions_topic, jobs_topic,
                    user_enriched_job_impression_topic, users_topic, fully_enriched_job_impression_topic)
from worker import app

# Streams:


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
        user_table[user.id] = user


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
        job_table[job.id] = job


@app.agent(job_impressions_topic)
async def enrich_job_impressions_with_user(job_impressions):
    """This function is used to enrich job_impression with user details.

    Args:
        job_impressions
    """
    async for impression in job_impressions.group_by(job_impressions.user_id):
        user = user_table[impression.user_id]

        # enrichment
        impression.language = user.language
        impression.gender = user.gender
        # Pushing it to intermediate topic
        await user_enriched_job_impression_topic.send(key=impression.id, value=impression)


@app.agent(user_enriched_job_impression_topic)
async def enrich_job_impressions_with_job(job_impressions):
    """This function is used to enrich (user-enriched) job_impression with job details.

    Args:
        job_impressions
    """
    await user_enriched_job_impression_topic.declare()
    async for impression in job_impressions.group_by(job_impressions.job_id):
        job = job_table[impression.job_id]

        # enrichment
        # impression.language = user.language
        # impression.gender = user.gender
        # Pushing it to intermediate topic
        await fully_enriched_job_impression_topic.send(key=impression.id, value=impression)
        

@app.agent(fully_enriched_job_impression_topic)
async def enrich_job_impressions_with_job(job_impressions):
    """This function is used to acknowledge the job impressions.

    Args:
        job_impressions
    """
    await fully_enriched_job_impression_topic.declare()
    async for impression in job_impressions:
        print(f'JobImpression: {impression.id} enriched: {impression}')

