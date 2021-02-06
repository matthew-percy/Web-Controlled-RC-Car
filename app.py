#!/usr/bin/env python

# app.py
# Matthew Percy and Mark Brierley
# TPJ655 - Raspberry Pi Car with Camera and Web App Control
# April 3, 2020
# Main python script which launches website and waits for AJAX calls from index.html 
# Runs methods which control GPIO output to the motor control circuit

import RPi.GPIO as GPIO
from datetime import datetime
import time
from flask import Flask, render_template, Response

# Emulated camera
# Raspberry Pi camera module (requires picamera package)
from camera_pi import Camera

# Initiate Flask
app = Flask(__name__)

# GPIO Pin Assignment
ENA, IN1, IN2, ENB, IN3, IN4 = 22, 27, 17, 18, 23, 24 
GPIO.setwarnings(False)

# GPIO Initialization
GPIO.setmode(GPIO.BCM)
GPIO.setup(ENA, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(IN1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN2, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ENB, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(IN3, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN4, GPIO.OUT, initial=GPIO.LOW)

# GPIO.PWM(channel, frequency)
pwm_ENA_A = GPIO.PWM(ENA, 200) 
pwm_ENA_B = GPIO.PWM(ENB, 200)

# Duty cycle 0.0 <= dc <= 100.0
dc_A = 50 
dc_B = 50

# LEFT MOTOR
pwm_ENA_A.start(dc_A)

# RIGHT MOTOR 
pwm_ENA_B.start(dc_B) 

# Flask: Launch web page
@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

# Flask: Stop motors
@app.route('/stop')
def stop():
    pwm_ENA_A.ChangeDutyCycle(dc_A)
    pwm_ENA_B.ChangeDutyCycle(dc_B)
    GPIO.output(IN1, GPIO.LOW) 
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    print("stopping")
    return("nothing")

# Flask: Move car forward
@app.route('/forward')
def forward():
    pwm_ENA_A.ChangeDutyCycle(dc_A)
    pwm_ENA_B.ChangeDutyCycle(dc_B)
    GPIO.output(IN1, GPIO.HIGH) #LEFT side forward
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH) #RIGHT side forward
    print('going forward')
    return("nothing")

# Flask: Move car forward and right
@app.route('/right')
def right():
    pwm_ENA_A.ChangeDutyCycle(90)
    pwm_ENA_B.ChangeDutyCycle(10)
    GPIO.output(IN1, GPIO.HIGH) #LEFT side forward
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH) #RIGHT side forward    
    print('going right')
    return("nothing")

# Flask: Move car forward and left
@app.route('/left')
def left():
    pwm_ENA_A.ChangeDutyCycle(10)
    pwm_ENA_B.ChangeDutyCycle(90)
    GPIO.output(IN1, GPIO.HIGH) #LEFT side forward
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH) #RIGHT side forward
    print('going left')
    return("nothing")

# Flask: Move car backwards
@app.route('/reverse')
def reverse():
    pwm_ENA_A.ChangeDutyCycle(dc_A)
    pwm_ENA_B.ChangeDutyCycle(dc_B)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH) #LEFT side reverse
    GPIO.output(IN3, GPIO.HIGH) #RIGHT side reverse
    GPIO.output(IN4, GPIO.LOW)
    print('going backwards')
    return("nothing")

# Flask: Move car backwards and to the right
@app.route('/rev_right')
def rev_right():
    pwm_ENA_A.ChangeDutyCycle(90)
    pwm_ENA_B.ChangeDutyCycle(10)
    GPIO.output(IN1, GPIO.LOW) 
    GPIO.output(IN2, GPIO.HIGH)#LEFT side reverse
    GPIO.output(IN3, GPIO.HIGH)#RIGHT side reverse
    GPIO.output(IN4, GPIO.LOW)    
    print('reversing right')
    return("nothing")

# Flask: Move car backwards and the left
@app.route('/rev_left')
def rev_left():
    pwm_ENA_A.ChangeDutyCycle(10)
    pwm_ENA_B.ChangeDutyCycle(90)
    GPIO.output(IN1, GPIO.LOW) 
    GPIO.output(IN2, GPIO.HIGH)#LEFT side reverse
    GPIO.output(IN3, GPIO.HIGH)#RIGHT side reverse
    GPIO.output(IN4, GPIO.LOW) 
    print('reversing left')
    return("nothing")

# Acquires camera frames
def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Flask: Delivers video feed to index.html
@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# Run on localhost port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)

#Clean up GPIO pins on exit    
GPIO.cleanup()
