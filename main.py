# This is a sample Python script.
from logger import logger
from scraper import scrape_movies
from apscheduler.schedulers.blocking import BlockingScheduler
import pytz
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()


scheduler = BlockingScheduler(timezone=pytz.timezone('Asia/Kolkata'))  # GMT+5:30

# @scheduler.scheduled_job(
#     'cron',
#     hour=11,
#     minute=29,
#     timezone=pytz.timezone('Asia/Kolkata')
# )

# Run every hour
@scheduler.scheduled_job('interval', minutes=5)
def start_app():
    logger.info("Started Job...")
    try:
        scrape_movies()
    except Exception as e:
        logger.exception(e)


if __name__ == '__main__':
    logger.info("Scheduler starting...")
    #start_app()
    scheduler.start()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
