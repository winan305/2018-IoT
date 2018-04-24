import time
from time import strftime

print("Start")
start_time = time.time()

time.sleep(10)

end_time = time.time()
print("End")
elapsed_time = end_time - start_time

print(elapsed_time)
# 10.xxxxxx sec.