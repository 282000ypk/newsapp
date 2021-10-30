import os
import time
import datetime


m = os.path.getmtime("test.py")
#print(time.ctime(m))
m = time.gmtime(m)
c = time.time()
#print(time.ctime(c))
c = time.gmtime(c)

print(f"{m} \n {c}")
print((c.tm_hour - m.tm_hour)*60+(c.tm_min - m.tm_min))

if((c.tm_hour - m.tm_hour)*60+(c.tm_min - m.tm_min) >= 1):
    pass
