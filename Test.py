from threading import Timer, current_thread

def temp():
    print(current_thread().name)

print(current_thread().name)
t = Timer(5, temp).start()