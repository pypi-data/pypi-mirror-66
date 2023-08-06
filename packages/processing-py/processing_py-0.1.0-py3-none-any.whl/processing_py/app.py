from threading import Thread
from subprocess import Popen, PIPE
import sys
import datetime as date
import os

class App(Thread):

	def __init__(self,size_x,size_y):
		Thread.__init__(self)
		self.millis_ = 0
		self.mouseX = 0
		self.mouseY = 0
		self.key = ''
		print('Starting App...')
		stream = Popen('java -jar processing-py.jar i3_jython.py',cwd=os.path.dirname(os.path.realpath(__file__))+'\\processing',stdin=PIPE, stdout=PIPE,stderr=PIPE)
		self.stdout = stream.stdout
		self.stdin = stream.stdin
		self.stderr = stream.stderr
		self.waitAnswer()
		print('Ready!')
		self.start()
	
	def waitAnswer(self):
		#print(str(self.stdout.readline()))
		str(self.stdout.readline())

	def run(self):
		while(True):
			self.get_global_variables()

	def get_global_variables(self):
		try:
			file = open(os.path.dirname(os.path.realpath(__file__))+'\\processing\\global_variables.txt','r')
			lines = file.readlines()
			#global millis_,mouseX,mouseY,key
			self.millis_ = int(lines[0])
			self.mouseX = int(lines[1])
			self.mouseY = int(lines[2])
			self.key = str(lines[3])
			file.close()
		except BaseException as e:
			pass
			#print(e)

	def print_(self,*args):
		print(*args, file=sys.stderr)

	def millis(self):
		return self.millis_

	def sendLine(self,line):
		line += '\n'
		self.stdin.write(line.encode('utf-8'))
		self.stdin.flush()
		self.waitAnswer()

	def std_function(self,name,*args):
		s = name+'('
		l = list(args)
		if len(l) > 0:
			for i in range(len(l)-1):
				s += str(l[i])
				s += ','
			s += str(l[len(l)-1])
		s += ')'
		self.sendLine(s)

	def background(self,*args):
		self.std_function('background',*args)

	def ellipse(self,*args):
		self.std_function('ellipse',*args)

	def stroke(self,*args):
		self.std_function('stroke',*args)

	def arc(self,*args):
		self.std_function('arc',*args)

	def circle(self,*args):
		self.std_function('circle',*args)

	def rect(self,*args):
		self.std_function('rect',*args)

	def fill(self,*args):
		self.std_function('fill',*args)

	def scale(self,*args):
		self.std_function('scale',*args)

	def translate(self,*args):
		self.std_function('translate',*args)

	def pushMatrix(self,*args):
		self.std_function('pushMatrix',*args)

	def popMatrix(self,*args):
		self.std_function('popMatrix',*args)

	def redraw(self,*args):
		self.std_function('redraw',*args)

	def strokeWeight(self,*args):
		self.std_function('strokeWeight',*args)

	def text(self,text,x,y):
		self.sendLine('text(\''+str(text)+'\','+str(x)+','+str(y)+')')
	
	def textWidth(self,*args):
		self.std_function('textWidth',*args)

	def textSize(self,*args):
		self.std_function('textSize',*args)

	def point(self,*args):
		self.std_function('point',*args)

	def rotateX(self,*args):
		self.std_function('rotateX',*args)

	def rotateY(self,*args):
		self.std_function('rotateY',*args)

	def rotateZ(self,*args):
		self.std_function('rotateX',*args)

	def triangle(self,*args):
		self.std_function('triangle',*args)

	def beginShape(self,*args):
		self.std_function('beginShape',*args)

	def Shape(self,*args):
		self.std_function('Shape',*args)

	def vertex(self,*args):
		self.std_function('vertex',*args)

	def line(self,*args):
		self.std_function('line',*args)

	def quad(self,*args):
		self.std_function('quad',*args)

	def bezier(self,*args):
		self.std_function('bezier',*args)

	def square(self,*args):
		self.std_function('square',*args)

	def noFill(self):
		self.std_function('noFill')

	def noCursor(self):
		self.std_function('noCursor')

	def delay(self):
		self.std_function('delay')

	def frameRate(self):
		self.std_function('frameRate')

	def smooth(self):
		self.std_function('smooth')

	def day(self):
		import datetime
		now = datetime.datetime.now()
		return now.day

	def hour(self):
		import datetime
		now = datetime.datetime.now()
		return now.hour

	def minute(self):
		import datetime
		now = datetime.datetime.now()
		return now.minute

	def month(self):
		import datetime
		now = datetime.datetime.now()
		return now.month

	def second(self):
		import datetime
		now = datetime.datetime.now()
		return now.second

	def year(self):
		import datetime
		now = datetime.datetime.now()
		return now.year





