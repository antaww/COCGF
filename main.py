import os
import time
import cv2
import easyocr  # OCR (Optical Character Recognition)
import numpy as np  # Numpy
import serial  # Serial communication
import pyautogui  # Screen management
from dotenv import load_dotenv  # Environment variables
from gym import Env  # Gym environment
from mss import mss  # Screen capture
from playsound import playsound  # Sound


# Debug : found resources position
# screen positions (for top right to "wind" button of pycharm)
# while True:
#     print(pyautogui.position())  # Print mouse position
#     time.sleep(0.3)


def wrong_input():
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n[ERROR] Wrong input, "
          "try again.")


class CocGF(Env):
    def __init__(self):
        self.capture = mss()
        self.resources_location = {"top": 128, "left": 673, "width": 87, "height": 85}  # full
        self.resources_names = ["gold", "elixir", "dark elixir"]
        self.to_find = 0  # 0 = gold, 1 = elixir, 2 = dark elixir
        self.min_resources = 0  # Minimum resources to stop searching
        self.ser = serial.Serial('COM3', 9600)

    def get_resources(self, min_resources):
        # get screen capture
        img = np.array(self.capture.grab(self.resources_location))
        cv2.imwrite("img.png", img)

        # read text from image with easyocr
        print("[OCR] Reading text...")
        reader = easyocr.Reader(['en'], verbose=False)  # todo: add gpu support
        res = reader.readtext(img)
        arr = []

        try:
            # remove every non digit character for each res[i][1], convert it to int and stock it in another array
            for value in range(len(res)):
                arr.append(int(''.join(filter(str.isdigit, res[value][1]))))

            # if any value in res is higher than min_resources
            if arr[self.to_find] > min_resources:
                return 0, res
            else:
                print(f"{arr[self.to_find]}/{min_resources}")
                return 1, res
        except ValueError or IndexError:
            print(f"[ERROR] OCR failed, retrying...")
            return 2, res


if __name__ == "__main__":
    env = CocGF()
    update = False

    # update settings from .env file
    load_dotenv()
    while True:
        user_ipt = input(f"[CHOICE] Would you like to update your current settings ? (y/n)"
                         f"\n[RESUME] Searching for {env.resources_names[int(os.environ.get('TO_FIND'))]} "
                         f"with minimum {os.environ.get('MIN_RESOURCES')} resources."
                         f"\n>>")
        if user_ipt == "y":
            update = True
            break
        elif user_ipt == "n":
            env.to_find = int(os.environ.get("TO_FIND"))
            env.min_resources = int(os.environ.get("MIN_RESOURCES"))
            break
        else:
            wrong_input()

    if update:
        # user input to select the resource to find
        while True:
            user_ipt = input("[CHOICE] Select resource to find :\n0 - gold\n1 - elixir\n2 - dark elixir\n>>")
            try:
                if int(user_ipt) in range(0, 3):
                    env.to_find = int(user_ipt)
                    break
                wrong_input()
            except ValueError:
                wrong_input()

        # user input to select the minimum resources to stop searching
        while True:
            user_ipt = input("[CHOICE] Type minimum resources to stop searching :\n>>")
            try:
                if int(user_ipt) >= 0:
                    env.min_resources = int(user_ipt)
                    break
            except ValueError:
                wrong_input()

        # erase .env file
        with open(".env", "w") as f:
            f.write("")
        # write new settings in .env file
        with open(".env", "a") as f:
            f.write(f"TO_FIND={env.to_find}\n")
            f.write(f"MIN_RESOURCES={env.min_resources}\n")

        # resuming user choices
        time.sleep(0.5)
        print(f"[RESUME] Searching for {env.resources_names[env.to_find]} with minimum {env.min_resources} resources.")

    # open serial port
    if not env.ser.isOpen():
        env.ser.open()
    print(f"[ARDUINO] COM3 open : {env.ser.isOpen()}\n[WAIT] 4s before beginning...")
    time.sleep(4)

    # Arduino communication
    while True:
        out_code, resources = env.get_resources(env.min_resources)
        if out_code == 1:
            env.ser.write(b'1')
            print(f"[CODE_{out_code}] Insufficient resources :")
            for i in range(len(resources)):
                print(f"    {resources[i][1]} {env.resources_names[i]}")
        if out_code == 1 or out_code == 2:
            print(f"[WAIT] 8s before next check...")
            time.sleep(8)
        elif out_code == 0:
            print(f"[CODE_{out_code}] Game found :")
            for i in range(len(resources)):
                print(f"    {resources[i][1]} {env.resources_names[i]}")
            # play sound to notify game found (absolute path needed)
            with open("sound_path.txt", "r") as f:
                sound_path = f.readline()
            playsound(sound_path)
            env.close()
            break
