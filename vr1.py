from fltk import *

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
		
	
	def but_press(self,wid,color):
		self.pressed.append(color)
		print(self.pressed)
	
	def play(self):
		print('work')
	
	def start_cb(self,wid):
		self.play()
		
app = game(400,400,'game')
app.show()
Fl.run()
