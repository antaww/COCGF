import subprocess

import imutils
from mss import mss  # Screen capture
import cv2  # Image processing
import time  # Time
import serial  # Serial communication
import pyautogui  # Mouse and keyboard control
from gym import Env  # Gym environment
from gym.spaces import Box, Discrete  # Gym spaces
import numpy as np  # Numpy
import os
from PIL import Image
import pytesseract  # OCR (Optical Character Recognition)


# while True:
#     print(pyautogui.position())  # Print mouse position
#     time.sleep(0.3)


# screen positions (for top right to "wind" button of pycharm)
# top left : 614, 60
# top right : 830, 60
# bottom right : 830, 223
# bottom left : 614, 223

class CocGF(Env):
    def __init__(self):
        self.capture = mss()
        # self.game_location = {"top": 128, "left": 678, "width": 80, "height": 80} # full
        self.gold_location = {"top": 128, "left": 678, "width": 80, "height": 20}  # gold
        self.elixir_location = {"top": 154, "left": 678, "width": 80, "height": 20}  # elixir
        self.dark_location = {"top": 181, "left": 678, "width": 80, "height": 20}  # dark elixir
        # self.observation_space = Box(low=0,
        #                              high=255,
        #                              shape=(self.game_location["height"], self.game_location["width"], 3),
        #                              dtype=np.uint8)
        self.action_space = Discrete(3)
        # todo: serial communication

    # def render(self):
    #     img = np.array(self.capture.grab(self.game_location))
    #     img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    #     cv2.imshow("Game", img)
    #     cv2.waitKey(1)

    # def get_observation(self):
    #     raw = np.array(self.capture.grab(self.game_location))[:, :, :3]
    #     gray = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)
    #     resized = cv2.resize(gray, (25, 42))
    #     channel = np.reshape(resized, (1, 42, 25))
    #     return channel

    def get_ressources(self):
        done = False

        # Gold capture
        gold_capture = np.array(self.capture.grab(self.gold_location))
        gold_img = Image.fromarray(gold_capture)
        gold_img.save("temp_screen.png")
        os.system("tesseract temp_screen.png stdout")
        os.remove("temp_screen.png")
        # todo: get command output in variable

        # Elixir capture
        elixir_capture = np.array(self.capture.grab(self.elixir_location))
        elixir_img = Image.fromarray(elixir_capture)
        elixir_img.save("temp_screen.png")
        os.system("tesseract temp_screen.png stdout")
        os.remove("temp_screen.png")

        # Dark elixir capture
        dark_capture = np.array(self.capture.grab(self.dark_location))
        dark_img = Image.fromarray(dark_capture)
        dark_img.save("temp_screen.png")
        os.system("tesseract temp_screen.png stdout")
        os.remove("temp_screen.png")

        # debug
        # cv2.imshow("Captured Image", dark_capture)
        # cv2.waitKey(0)
        # end debug
        return done

    # def reset(self):
    #     return self.get_observation()

    def close(self):
        cv2.destroyAllWindows()


if __name__ == "__main__":
    env = CocGF()
    print(env.get_ressources())
    # env.close()
