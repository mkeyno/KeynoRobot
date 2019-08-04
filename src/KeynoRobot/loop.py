import time
import threading


data_ready = threading.Event()
kill_flag = threading.Event()


def keyboard_poller():
        global key_pressed
        loop = True

        while loop:
                time.sleep(1)

                if kill_flag.isSet():
                        loop = False

                ch = input(">")
                if ch:
                        key_pressed = ch
                        data_ready.set()


def main():
        curr_millis = time.time() * 1000
        prev_millis = curr_millis

        poller = threading.Thread(target=keyboard_poller)
        poller.start()

        loop = True

        while loop:
                curr_millis = time.time() * 1000
                if (curr_millis - prev_millis) >= 1000:
                        print("Another second passed..." + str(curr_millis) + "\r")
                        prev_millis = curr_millis
                        # Do some extra stuff here

                if >.isSet():
                        if key_pressed.lower() == "q":
                                kill_flag.set()
                                loop = False
                        else:
                                print("You pressed: " + key_pressed)
                        data_ready.clear()


if __name__ == "__main__":
        print("Started..")
        main()

        input("Press any key to exit...")
        exit()