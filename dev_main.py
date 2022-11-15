from fltk import *
import subprocess
import os
import random
import signal

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
		self.temp = 0
		self.sound = 0
		self.resizable(self)
	
	
	def kill_last_process(self,name):
		for line in os.popen("ps ax | grep " + name + " | grep -v grep"):
			fields = line.split()
			 
			# extracting Process ID from the output
			pid = fields[0]
			 
			# terminating process
			os.kill(int(pid), signal.SIGKILL)
			print(f'sucessfully terminated {pid}')
			

	def reactive(self):
		self.red.activate()
		self.blue.activate()
		self.green.activate()
		self.yellow.activate()
		
	def flash(self):
		print(self.temp)
		self.sound = str(os.path.join(self.working_dir,f'{self.sequence[self.temp]}.mp3'))
		self.sound = subprocess.Popen(['vlc','--intf','dummy',self.sound])
		Fl.add_timeout(1.0,self.kill_last_process,f'{self.sequence[self.temp]}.mp3')
		
		if self.sequence[self.temp] == 'red':
			self.red.color(FL_WHITE)
		elif self.sequence[self.temp] == 'blue':
			self.blue.color(FL_WHITE)
		elif self.sequence[self.temp] == 'yellow':
			self.yellow.color(FL_WHITE)
		elif self.sequence[self.temp] == 'green':
			self.green.color(FL_WHITE)
		self.redraw()
		Fl.add_timeout(0.4,self.change_back)
		self.temp += 1
		
	def change_back(self):
		self.red.color(FL_RED)
		self.blue.color(FL_BLUE)
		self.yellow.color(FL_YELLOW)
		self.green.color(FL_GREEN)
		self.redraw()
	
	def next_sequence(self):
		self.red.deactivate()
		self.blue.deactivate()
		self.green.deactivate()
		self.yellow.deactivate()
		self.temp = 0
		self.pressed = []
		self.sequence.append(random.choice(['yellow','blue','red','green']))
		print(self.sequence)
		for x in range(len(self.sequence)):
			Fl.add_timeout(1.0+ 1.0*x,self.flash)
			Fl.add_timeout(1.0+1.0*len(self.sequence),self.reactive)
		
		
	def but_press(self,wid,color):
		Fl.remove_timeout(self.notime)
		correct = False
		self.pressed.append(color)
		self.sound = str(os.path.join(self.working_dir,f'{color}.mp3'))
		self.sound = subprocess.Popen(['vlc','--intf','dummy',self.sound])
		if len(self.sequence) == 0:
			fl_message("please start the game first")
			return None
		
		for x in range(len(self.pressed)):
			if self.pressed[x] == self.sequence[x]:
				if len(self.pressed) == len(self.sequence):
					correct = True
			
			else:
				self.kill_last_process(f'{color}.mp3')
				self.sound = str(os.path.join(self.working_dir,'error.mp3'))
				self.sound = subprocess.Popen(['vlc','--intf', 'dummy',self.sound])
				fl_message(f'your score is: {len(self.sequence)}')
				correct = False
				self.pressed = []
				self.sequence = []
				break
		
		Fl.add_timeout(1.0,self.kill_last_process,f'{color}.mp3')
		Fl.add_timeout(5.0,self.notime)
		
		if correct is True:
			Fl.remove_timeout(self.notime)
			self.next_sequence()
				
		print('self.pressed: ' + str(self.pressed))
	
	def notime(self):
		fl_message(f'your score is: {len(self.sequence)}')
		self.sound = str(os.path.join(self.working_dir,'error.mp3'))
		self.sound = subprocess.Popen(['vlc','--intf','dummy',self.sound])
		self.sequence = []
		self.pressed = []
		
	
	def start_cb(self,wid):
		Fl.remove_timeout(self.notime)
		if self.sequence != []:
			fl_message(f'your score is: {len(self.sequence)}')
		Fl.remove_timeout(self.flash)
		Fl.remove_timeout(self.change_back)
		Fl.remove_timeout(self.reactive)
		self.reactive()
		self.change_back()
		Fl.add_timeout(2.0,self.next_sequence)
		self.pressed = []
		self.sequence = []
		Fl.add_timeout(5.0,self.notime)
		
		
		print('work')
		
app = game(400,400,'game')
app.show()
Fl.run()
