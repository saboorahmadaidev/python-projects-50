from time import time
import random as r

def mistake(partest, usertest):
    error = 0
    for i in range(len(partest)):
        try:
            if partest[i] != usertest[i]:
                error += 1
        except:
            error += 1
    return error


def speed_time(time_s, time_e, userinput):
    time_delay = time_e - time_s
    if time_delay == 0:   # safety check
        return 0
    time_r = round(time_delay, 2)
    speed = len(userinput) / time_r
    return round(speed, 2)


if __name__ == "__main__":

    while True:
        ck = input("Do you want to start the typing speed test? (yes/no): ").lower()

        if ck == 'yes':
            test = [
                "The typing speed test is a fun and engaging way to improve your typing skills.",
                "Practice makes perfect, so keep typing to enhance your speed and accuracy.",
                "Typing quickly and accurately is an essential skill in today's digital world.",
            ]

            test1 = r.choice(test)
            print("\nTyping Speed Test")
            print(test1)
            print()

            time_1 = time()
            testinput = input("Type here: ")
            time_2 = time()

            print('Speed:', speed_time(time_1, time_2, testinput), 'chars/sec')
            print("Error:", mistake(test1, testinput))
            print("-" * 40)

        elif ck == 'no':
            print("Thank you for using the typing speed test. Goodbye!")
            break

        else:
            print("Invalid input. Please enter 'yes' or 'no'.")
