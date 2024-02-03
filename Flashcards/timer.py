import time


# define the countdown func.
def countdown():
    t = 10
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        t -= 1
        print(t)

    print('Fire in the hole!!')


# input time in seconds

# function call
countdown()