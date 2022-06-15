import RPi.GPIO as GPIO
import time
import tkinter as tk

controllerWindow = tk.Tk()  # initializes this tk interpreter and creates the root window
controllerWindow.title("Servo Tester")    # define title of the root window
controllerWindow.geometry("380x410")    # define size of the root window
controllerWindow["bg"] = "lightgrey"     # define the background color of the root window
controllerWindow.resizable(0, 1)    # define if the root window is resizable or not for Vertical and horizontal
angleDefault = 90

FramePIDCoef = tk.LabelFrame(controllerWindow, text="Servo Test Slider")
FramePIDCoef.place(x=20, y=20, width=400)

angle = tk.Scale(FramePIDCoef, from_=0, to=180, orient="horizontal", label="Servo angle", length=350, tickinterval=0.01,
                       resolution=0.001)
angle.set(angleDefault)
angle.pack()

angle= angle/180*2.0

servoPIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
p.start(2.5) # Initialization
try:
  while True:
   p.ChangeDutyCycle(angle)
except KeyboardInterrupt:
  p.stop()
  GPIO.cleanup()

tk.mainloop()  