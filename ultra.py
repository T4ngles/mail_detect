###################
#
# Ultrasonic Sensor
#
# TGCID
#
###################

#libaries
import RPi.GPIO as GPIO
import time
from datetime import datetime

#pin setup
GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER = 18
GPIO_ECHO = 24

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
c_speed = 343000 #speed of sound in mm/s
continuous = 0

def distance():
	#set trigger to high
	GPIO.output(GPIO_TRIGGER, True)
	#wait 0.01ms then set trigger to low
	time.sleep(0.00001)
	GPIO.output(GPIO_TRIGGER, False)

	#record times	
	StartTime = time.time()
	StopTime = time.time()

	#save emit time
	while GPIO.input(GPIO_ECHO) == 0:
		StartTime = time.time()
	#save echo detect time
	while GPIO.input(GPIO_ECHO) == 1:
		StopTime = time.time()
	#time diff
	TravelTime = StopTime - StartTime
	distance = (TravelTime*c_speed)/2

	return distance

def time_now():
	now = datetime.now()
	current_time = now.strftime("%H:%M:%S")
	return current_time

def main(continuous):
	continuous = continuous
	if continuous:
		try:
			dist = 1000
			count = 0
			while count < 10:
				dist = distance()			
				if dist > 100:
					print (time_now() + " Distance = %.1f mm" % dist)
				elif dist <= 100:
					count += 1
					print (time_now() + " Distance = %.1f mm!!! Count: %d" % (dist, count))
				time.sleep(60)
			print(time_now() + "count: %d whoa too close" % count )
			GPIO.cleanup()
		except KeyboardInterrupt:
			print ("Ultra stopped by User")
			GPIO.cleanup()
	else:
		dist = distance()
		f = open(time_now() + " distance.txt", "a")
		f.write(time_now() + " Distance = %.1f mm" % dist)
		f.close()


if __name__ == '__main__':
	main(continuous)


