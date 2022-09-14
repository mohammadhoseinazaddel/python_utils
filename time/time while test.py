import time


# example1
start_time = time.time()
print(start_time)
print(time.localtime(start_time))
print(time.asctime(time.localtime(start_time)))

# Get the epoch
obj = time.gmtime(0)
print(obj)
epoch = time.asctime(obj)
print("epoch is:", epoch)

# Get the time in seconds
# since the epoch
time_sec = time.time()
print("Time in seconds since the epoch:", time_sec)

# example2
# Date 1
date1 = "1 Jan 2000 00:00:00"

# Date 2
# Current date
date2 = "24 Aug 2022 19:09:00"

# Parse the date strings
# and convert it in
# time.struct_time object using
# time.strptime() method
obj1 = time.strptime(date1, "%d %b %Y %H:%M:%S")
obj2 = time.strptime(date2, "%d %b %Y %H:%M:%S")

# Get the time in seconds
# since the epoch
# for both time.struct_time objects
time1 = time.mktime(obj1)
time2 = time.mktime(obj2)

print("Date 1:", time.asctime(obj1))
print("Date 2:", time.asctime(obj2))

# Seconds between Date 1 and date 2
seconds = time2 - time1
print("Seconds between date 1 and date 2 is %s f seconds" % seconds)


# example3
while True:
    time.sleep(1)
    current_time = time.time()
    elapsed_time = current_time - start_time
    print(start_time)
    print(current_time)
    print(elapsed_time)
    if elapsed_time > 30:
        break
print "done"