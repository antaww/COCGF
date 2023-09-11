import os

from mss import mss  # Screen capture
import cv2  # Image processing
import time  # Time
import serial  # Serial communication
import pyautogui  # Mouse and keyboard control
from gym import Env  # Gym environment
import numpy as np  # Numpy
from PIL import Image
import pytesseract  # OCR (Optical Character Recognition)
import easyocr  # OCR (Optical Character Recognition)
import tensorflow as tf  # GPU support
from playsound import playsound  # Sound


# Debug : found resources position
# screen positions (for top right to "wind" button of pycharm)
# while True:
#     print(pyautogui.position())  # Print mouse position
#     time.sleep(0.3)


class CocGF(Env):
    def __init__(self):
        self.capture = mss()
        self.game_location = {"top": 128, "left": 673, "width": 80, "height": 85}  # full
        self.toFind = 0  # 0 = gold, 1 = elixir, 2 = dark elixir
        self.min_resources = 0  # Minimum resources to stop searching
        self.ser = serial.Serial('COM3', 9600)

    def get_resources(self, min_resources):
        # get screen capture
        resources = np.array(self.capture.grab(self.game_location))
        # read text from image with easyocr
        reader = easyocr.Reader(['en'], verbose=True)  # todo: add gpu support
        res = reader.readtext(resources)

        # print every word found
        for i in range(len(res)):
            print(res[i][1])

        # if any value in res is higher than min_resources
        if any(int(res[i][1]) > min_resources for i in range(len(res))):
            return 0, res
        else:
            return 1, res


if __name__ == "__main__":
    env = CocGF()

    if not env.ser.isOpen():
        env.ser.open()
    print(f"COM3 open : {env.ser.isOpen()}\n[WAIT] 4s before beginning...")
    time.sleep(4)

    # Arduino communication
    while True:
        out_code, resources = env.get_resources(env.min_resources)
        if out_code == 1:
            env.ser.write(b'1')
            print(f"[{out_code}] Insufficient resources ({resources})")
            time.sleep(8)
        else:
            print(f"[{out_code}] Game found ! ({resources})")
            # play sound to notify game found (absolute path needed)
            with open("sound_path.txt", "r") as f:
                sound_path = f.readline()
            playsound(sound_path)
            env.close()
            break
