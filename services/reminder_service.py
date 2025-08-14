
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from .bot_logger_service import logger

scheduler = AsyncIOScheduler()

def setup_reminder_scheduler(bot):
    if not scheduler.running:
        scheduler.start()
        logger.info("Reminder scheduler started.")

    # Example job (placeholder)
    def hello_job():
        logger.info("Reminder tick at %s", datetime.utcnow())

    # Avoid duplicate jobs if reloaded
    if not any(job.id == "hello_job" for job in scheduler.get_jobs()):
        scheduler.add_job(hello_job, "interval", minutes=30, id="hello_job")
