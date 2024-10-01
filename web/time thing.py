import time
import os

def clear_console():
    # Clear the console for Windows
        os.name == 'nt'
        os.system('cls')

def train_station_board(message, speed=0.05):
    final_message = list(message.upper())  # convert the message to uppercase
    display_message = [' '] * len(message)  # initialize display message with spaces

    for i in range(len(message)):
        for char in range(32, 127):  # ASCII printable characters range from 32 to 126
            display_message[i] = chr(char)
            clear_console()
            print(''.join(display_message))
            time.sleep(speed)
            if display_message[i] == final_message[i]:
                break

if __name__ == "__main__":
    train_station_board("hello world", speed=0.005)
