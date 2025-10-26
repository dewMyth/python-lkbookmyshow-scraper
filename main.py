# This is a sample Python script.
from logger import logger
from scraper import scrape_movies
from apscheduler.schedulers.blocking import BlockingScheduler

scheduler = BlockingScheduler()

@scheduler.scheduled_job('interval', minutes=1, name='scrape_scheduler')
def start_app():
    scrape_movies()


if __name__ == '__main__':
    logger.info("Scheduler starting...")
    scheduler.start()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
