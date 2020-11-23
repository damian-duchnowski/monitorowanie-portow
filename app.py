import schedule
import time

from notify import send_emails
from settings import SCAN_INTERVAL_MIN

schedule.every(SCAN_INTERVAL_MIN).seconds.do(send_emails)

while True:
    schedule.run_pending()
    time.sleep(1)
