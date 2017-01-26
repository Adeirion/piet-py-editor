import sys
import numpy as np

code_colors = {0:'white', 1: 'black',
			11:'lred', 12:'red', 13:'dred',
			21:'lyellow', 22:'yellow', 23:'dyellow',
			31:'lgreen', 32:'green', 33:'dgreen',
			41:'lcyan', 42:'cyan', 43:'dcyan',
			51:'lblue', 52:'blue', 53:'dblue',
			61:'lmagenta', 62:'magenta', 63:'dmagenta'}

color_codes = {'white':0, 'black':1,
			'lred':11, 'red':12, 'dred':13,
			'lyellow':21, 'yellow':22, 'dyellow':23,
			'lgreen':31, 'green':32, 'dgreen':33,
			'lcyan':41, 'cyan':42, 'dcyan':43,
			'lblue':51, 'blue':52, 'dblue':53,
			'lmagenta':61, 'magenta':62, 'dmagenta':63}

class Program():

	"""
	Piet program

	height : number of rows
	width : number of columns

	"""
	def __init__(self, height, width):
		self.height = height
		self.width = width

		self.program = np.zeros((height, width), dtype='int')

	def set_codel(self, row, column, color):
		self.program[row,column] = color_codes[color]

	def get_codel(self, row, column):
		return code_colors[self.program[row, column]]

	def get_colorblock(self, row, column):
		"""
		Returns a list of tuple with coordinates of the codels of the colorblock.
		"""

		block = [(row,column)]

		expand=True
		index=0
		while(index<len(block)):
			x=block[index][0]
			y=block[index][1]
			#to the top
			if x>0 and self.program[x-1,y]==self.program[row,column] and (x-1,y) not in block:
					block.append((x-1,y))
			#to the bottom
			if x<self.height-1 and self.program[x+1,y]==self.program[row,column] and (x+1,y) not in block:
					block.append((x+1,y))
			#to the left
			if y>0 and self.program[x,y-1]==self.program[row,column] and (x,y-1) not in block:
					block.append((x,y-1))
			#to the right
			if y<self.width-1 and self.program[x,y+1]==self.program[row,column] and (x,y+1) not in block:
					block.append((x,y+1))
			index = index+1
		return block

def main():

	program_file = sys.argv[1]

	#load program
	#program = load(program_file, codel_size)

	#run 

if __name__ == '__main__':
	main()
