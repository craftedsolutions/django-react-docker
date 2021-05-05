from time import sleep

count = 0
while True:
    sleep(10)
    print("Running! " + str(count))
    count = count + 1
