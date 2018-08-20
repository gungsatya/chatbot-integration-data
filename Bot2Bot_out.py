import time
from Bot2Bot import importDb, pulseChecker, trxChecker

importDb()

while (True):
    pulseChecker()
    trxChecker()
    time.sleep(2)
