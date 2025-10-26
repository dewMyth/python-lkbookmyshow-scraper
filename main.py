# This is a sample Python script.
from logger import logger
from scraper import scrape_movies
from apscheduler.schedulers.blocking import BlockingScheduler
import pytz


scheduler = BlockingScheduler(timezone=pytz.timezone('Asia/Kolkata'))  # GMT+5:30

def start_app():
    scrape_movies()

scheduler.add_job(start_app, 'cron', minute='*/1')

if __name__ == '__main__':
    logger.info("Scheduler starting...")
    scheduler.start()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
