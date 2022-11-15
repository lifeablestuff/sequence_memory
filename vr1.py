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
	
	
	def kill_process(self,pid):
		'''
		for line in os.popen("ps ax | grep " + name + " | grep -v grep"):
			fields = line.split()
			pid = None
			# extracting Process ID from the output
			pid = fields[0]
			'''
			 
			# terminating process
		os.kill(int(pid), signal.SIGTERM)
	'''
	def set_widget_color(self,widget,color):
        if widget == color:
            if widget == 'red':
                self.red.color(FL_RED)
            elif widget == 'blue':
                self.blue.color(FL_BLUE)
            elif widget == 'yellow':
                self.yellow.color(FL_YELLOW)
            else:
                self.green.color(FL_GREEN)
    '''
    

                    # make setters and getters
	def set_color(self,widget_and_color):
		
		if len(widget_and_color) == 1:
			if widget_and_color[0] == 'red':
				self.red.color(FL_RED)
			elif widget_and_color[0] == 'blue':
				self.blue.color(FL_BLUE)
			elif widget_and_color[0] == 'yellow':
				self.yellow.color(FL_YELLOW)
			else:
				self.green.color(FL_GREEN)
				
		else:
			if widget_and_color[0] == 'red':
				self.red.color(FL_WHITE)
			
			elif widget_and_color[0] == 'blue':
				self.blue.color(FL_WHITE)
			
			elif widget_and_color[0] == 'yellow':
				self.yellow.color(FL_WHITE)
	
			else:
				self.green.color(FL_WHITE)

		self.redraw()
	
	

	def activate_buttons(self):
		self.red.activate()
		self.blue.activate()
		self.green.activate()
		self.yellow.activate()

	def flash(self):
		self.sound = str(os.path.join(self.working_dir,f'{self.sequence[self.temp]}.mp3'))
		self.sound = subprocess.Popen(['vlc','--intf','dummy',self.sound])
		Fl.add_timeout(5.0,self.kill_process,self.sound.pid)

		self.set_color([self.sequence[self.temp],'white'])
		Fl.add_timeout(0.5,self.set_color,[self.sequence[self.temp]])
		
		self.redraw()
		self.temp += 1
		
	def next_sequence(self):
		self.red.deactivate()
		self.blue.deactivate()
		self.green.deactivate()
		self.yellow.deactivate()
		self.temp = 0
		self.pressed = []

		self.sequence.append(random.choice(['yellow','blue','red','green']))
		for x in range(len(self.sequence)):
			Fl.add_timeout(1.25+ 1.025*x,self.flash)
			Fl.add_timeout(1.0+1.0*len(self.sequence),self.activate_buttons)

		Fl.add_timeout(1.0+1.0*len(self.sequence)+5.0,self.after_5_seconds_and_no_input)


	def but_press(self,wid,color):

		Fl.remove_timeout(self.after_5_seconds_and_no_input)
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
				Fl.add_timeout(3.0,self.kill_process,self.sound.pid)
				self.sound = str(os.path.join(self.working_dir,'error.mp3'))
				self.sound = subprocess.Popen(['vlc','--intf', 'dummy',self.sound])
				Fl.add_timeout(5.0,self.kill_process,self.sound.pid)
				Fl.remove_timeout(self.after_5_seconds_and_no_input)
				fl_message(f'your score is: {len(self.sequence)}')
				correct = False
				self.pressed = []
				self.sequence = []
				return None
				break

		Fl.add_timeout(1.0,self.kill_process,self.sound.pid)
		Fl.add_timeout(5.0,self.after_5_seconds_and_no_input)

		if correct == True:
			Fl.remove_timeout(self.after_5_seconds_and_no_input)
			self.next_sequence()


	def after_5_seconds_and_no_input(self):
		Fl.remove_timeout(self.after_5_seconds_and_no_input)
		fl_message(f'your score is: {len(self.sequence)}')
		self.sound = str(os.path.join(self.working_dir,'error.mp3'))
		self.sound = subprocess.Popen(['vlc','--intf','dummy',self.sound])
		self.sequence = []
		self.pressed = []


	def start_cb(self,wid):
		Fl.remove_timeout(self.after_5_seconds_and_no_input)
		if self.sequence != []:
			fl_message(f'your score is: {len(self.sequence)}')
		Fl.remove_timeout(self.flash)
		Fl.remove_timeout(self.activate_buttons)
		self.activate_buttons()
		Fl.add_timeout(1.0,self.next_sequence)
		self.pressed = []
		self.sequence = []
		
		
app = game(400,400,'game')
app.show()
Fl.run()
