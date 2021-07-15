import pygame
from pygame.locals import *
import tensorflow as tf
import sys, os, math
import time
import pygame.font
from tkinter import Tk
from tkinter import *
from tkinter import messagebox
from tensorflow.keras.models import load_model
from numpy import asarray
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
import cv2

_image_library = {}
def get_image(path):
        global _image_library
        image = _image_library.get(path)
        if image == None:
                canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
                image = pygame.image.load(canonicalized_path)
                _image_library[path] = image
        return image

height = 512
width = 512
cs = 512 # basic image size
cs2 = 512

clock = pygame.time.Clock()

pygame.display.set_caption('number predictor')

mouse = pygame.mouse

BLACK = pygame.Color( 0 ,  0 ,  0 )
WHITE = pygame.Color(255, 255, 255)
shotNumber = 1
mlNo = 0

clock = pygame.time.Clock()

def saveScreen():
    global shotNumber, mlNo
    mlNo += 1
    save_name = "images_drawn/photo"+str(shotNumber)+".jpg"
    pygame.image.save(window,save_name)
    shotNumber += 1
    print(shotNumber)

def load_image(filename):
    img = cv2.imread("images_drawn/photo"+str(mlNo)+".jpg")
    width = 28
    height = 28
    dim = (width, height)
    newphoto = cv2.cvtColor( img ,  cv2.COLOR_BGR2GRAY )
    # resize image
    resized = cv2.resize(newphoto, dim, interpolation = cv2.INTER_AREA)
    img = resized.reshape(1, 28, 28, 1)
    return img

image = "images_drawn/photo"+str(mlNo)+".jpg"

def run_example():
    img = load_image(image)
    # load model
    model = load_model('mnist1.h5')
    # predict the class
    digit = model.predict_classes(img)
    return str(digit[0])

window = pygame.display.set_mode([512,512])
canvas = window.copy()
left_pressed, middle_pressed, right_pressed = mouse.get_pressed()
canvas.fill(BLACK)
global savePath,autoRotate, saveSource,preRot,flipH,flipV
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_ESCAPE :
                terminate()
            if event.key == pygame.K_s :
                saveScreen()
                Tk().wm_withdraw() #to hide the main window
                messagebox.showinfo('Continue','the number you drew is '+ run_example())
                print("File has been saved")
            if event.key == pygame.K_c :
                canvas.fill(BLACK)
        elif pygame.mouse.get_pressed() == (1, 0, 0):
            pygame.draw.circle(canvas, WHITE, (pygame.mouse.get_pos()),10)
            window.fill(BLACK)
    window.blit(canvas, (0, 0))
    pygame.draw.circle(window,WHITE,(pygame.mouse.get_pos()),5)
    pygame.display.update()
    clock.tick(1000)



