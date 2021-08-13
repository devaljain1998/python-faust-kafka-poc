from worker import app
from topics import users_topic, jobs_topic, job_impressions_topic
from tables import user_table, job_table

# Streams:
@app.agent(users_topic)
async def save_users(users):
    # Creating users topic
    await users_topic.declare()
    
    async for user in users:
        user_table[user.id] = user

@app.agent(jobs_topic)
async def save_jobs(jobs):
    # Creating jobs topic
    await jobs_topic.declare()
    
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