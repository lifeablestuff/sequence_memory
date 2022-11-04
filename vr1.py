from fltk import *
import subprocess
import os
import random

class game(Fl_Window):
	def __init__(self,w,h,l):
		Fl_Window.__init__(self,500,300,w,h,l)
		self.begin()
		
		self.start = Fl_Button(170,150,60,60,'start')
		self.yellow = Fl_Button(230,210,100,100)
		self.yellow.color(FL_YELLOW)
		self.blue = Fl_Button(230,50,100,100)
		self.blue.color(FL_BLUE)
		self.red = Fl_Button(70,50,100,100)
		self.red.color(FL_RED)
		self.green = Fl_Button(70,210,100,100)
		self.green.color(FL_GREEN)
		Fl.scheme('plastic')
		self.end()
		self.start.callback(self.start_cb)
		self.yellow.callback(self.but_press,'yellow')
		self.blue.callback(self.but_press,'blue')
		self.red.callback(self.but_press,'red')
		self.green.callback(self.but_press,'green')
		self.pressed = []
		self.sequence = []
		self.correctbut = iter(self.sequence)
		#mp3 assingment
		self.working_dir = os.getcwd()
		self.working_dir = str(os.path.abspath(self.working_dir))
		self.sound = 0
		
	def next_sequence(self):
		self.sequence.append(random.choice(['yellow','blue','red','green']))
	
	def but_press(self,wid,color):
		self.pressed.append(color)
		if color == next(self.correctbut):
			next_sequence()
		self.sound = str(os.path.join(self.working_dir,f'{color}.mp3'))
		self.sound = subprocess.Popen(['vlc','--intf','dummy',self.sound])
		
		print(self.pressed)
	
	def play(self):
		self.next_sequence
		print('work')
	
	def start_cb(self,wid):
		self.play()
		
app = game(400,400,'game')
app.show()
Fl.run()
