import time, sys

for i in range(101):
    sys.stdout.write(str(i) + "% \r")
    sys.stdout.flush()
    time.sleep(.3)
quit();

while True:
    try:
        sys.stdout.write("%d...\r" % x)
        sys.stdout.flush()
        time.sleep(.3)
        x += 1
    except KeyboardInterrupt:
        print "Bye"
        sys.exit()
