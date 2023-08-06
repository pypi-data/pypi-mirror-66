from EasyCommunicationHandler import EasyCommunicationSlave
import logging
import time

logging.addLevelName(10, "Slave-Debug")

i = 0
n = 0
while True:
    try:
        slave = EasyCommunicationSlave("localhost", 12456, "test")
        break
    except ConnectionRefusedError:
        n += 1
        print("refused", n)
        time.sleep(1)
while True:
    data = slave.wait_until_receiving()
    print("received by slave", data)

    i += 1
    time.sleep(i)
    slave.send(payload="slave responding")
