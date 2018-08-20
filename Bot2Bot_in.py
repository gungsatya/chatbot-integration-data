import time
from Bot2Bot import getLastIdMessageIN, getMyName, receiveMessages

last_id = getLastIdMessageIN()
myName = getMyName()

while (True):
    temp = receiveMessages(myName, last_id)
    if (temp != ""): last_id = temp
    time.sleep(2)
