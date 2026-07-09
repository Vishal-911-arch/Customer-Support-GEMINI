import uuid


class JobService:

    jobs = {}

    @classmethod
    def create_job(cls):

        job_id = str(uuid.uuid4())

        cls.jobs[job_id] = {
            "status": "queued",
            "progress": 0,
            "message": "Waiting..."
        }

        return job_id

    @classmethod
    def update(
        cls,
        job_id,
        progress,
        message,
        status="running"
    ):

        cls.jobs[job_id] = {
            "status": status,
            "progress": progress,
            "message": message
        }

    @classmethod
    def finish(cls, job_id):

        cls.jobs[job_id] = {
            "status": "completed",
            "progress": 100,
            "message": "Knowledge Base Updated"
        }

    @classmethod
    def error(cls, job_id, error):

        cls.jobs[job_id] = {
            "status": "error",
            "progress": 100,
            "message": str(error)
        }

    @classmethod
    def get(cls, job_id):

        return cls.jobs.get(job_id)