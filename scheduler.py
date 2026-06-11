from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from config import TIMEZONE

scheduler = AsyncIOScheduler(timezone=TIMEZONE)

def start_scheduler(bot):
    # Пример: ежедневное приветствие в 9 утра (можно заменить на свою логику)
    @scheduler.scheduled_job(CronTrigger(hour=9, minute=0))
    async def good_morning():
        # Здесь можно отправить сообщение всем пользователям или что-то другое
        pass
    scheduler.start()
