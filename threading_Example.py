import threading

# threading.Timer(delay, funtion, args=[..])

isClear = False
def clear() :
    global isClear
    print("Call clear")
    isClear = True
    
def function(count) :
    print("Funtion call :", count)
    count += 1
    
    timer1 = threading.Timer(1, function, args = [count])
    
    if count < 5 :
        timer1.start()
        # timer.cancel()
        
#function(0)
timer2 = threading.Timer(2, clear, args=[])
timer2.start()
i = 0
while not isClear :
    print(i)
    i+=1

# target up -> wait 5 sec(timer.start()) -> clear()