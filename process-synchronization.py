import threading
import time

num_slots = int(input("Enter the number of slots inside the fitting room: "))
num_blue = int(input("Enter the number of blue threads: "))
num_green = int(input("Enter the number of green threads: "))

slots = threading.Semaphore(num_slots)
green = threading.Lock()
blue = threading.Lock()
mutex = threading.Lock()
empty = threading.Lock()

thread_ID = 1
occupied = 0
flag_blue = 0
flag_green = 0
counter = 0

class EmptyRoom(threading.Thread):
    def run(self):
        global num_blue, num_green, num_slots
        global thread_ID, occupied, flag_blue, flag_green, counter

        while counter < num_blue + num_green:
            if not mutex.locked():
                slots.acquire()
                mutex.acquire()
                occupied = 0
                if blue.locked() and not green.locked():
                    blue.release()
                    green.acquire()
                elif green.locked() and not blue.locked():
                    green.release()
                    blue.acquire
                elif green.locked() and blue.locked():
                    if counter % 2 == 0:
                        blue.release()
                    else:
                        green.release()
                
                if flag_blue == 1 and green.locked():
                    green.release()
                if flag_green == 1 and blue.locked():
                    blue.release()

                if empty.locked():
                    print("\n>> Empty Room ")
                    empty.release()
                mutex.release()

class Blue(threading.Thread):
    def run(self):
        global num_blue, num_green, num_slots
        global thread_ID, occupied, flag_blue, flag_green, counter
        
        blueCount = 0
        green.acquire()
        while blueCount < num_blue:
            if not blue.locked() and occupied < num_slots and not mutex.locked():
                mutex.acquire()
                slots.release()
                if occupied == 0:
                    print("\n----- Blue Only -----")
                    empty.acquire()
                    if not green.locked():
                        green.acquire()
                occupied = occupied + 1
                blueCount = blueCount + 1
                counter = counter + 1
                print("Thread ID: {}".format(thread_ID))
                print("Color: BLUE")
                thread_ID = thread_ID + 1

                if occupied == num_slots:
                    blue.acquire()
                elif blueCount == num_green:
                    blue.acquire()
                mutex.release()
        flag_blue = 1

class Green(threading.Thread):
    def run(self):
        global num_blue, num_green, num_slots
        global thread_ID, occupied, flag_blue, flag_green, counter
        
        greenCount = 0
        blue.acquire()
        while greenCount < num_green:
            if not green.locked() and occupied < num_slots and not mutex.locked():
                mutex.acquire()
                slots.release()
                if occupied == 0:
                    print("\n----- Green Only -----")
                    empty.acquire()
                    if not blue.locked():
                        blue.acquire()
                occupied = occupied + 1
                greenCount = greenCount + 1
                counter = counter + 1
                print("Thread ID: {}".format(thread_ID))
                print("Color: GREEN")
                thread_ID = thread_ID + 1

                if occupied == num_slots or greenCount == num_green:
                    green.acquire()
                mutex.release()
        flag_green = 1

blue_only = Blue()
green_only = Green()
room = EmptyRoom()

blue_only.start()
green_only.start()
room.start()

blue_only.join()
green_only.join()
room.join()
