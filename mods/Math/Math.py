"""
Math.py 
evaluates a string math expression recursively and returns the value

Matthew Russell
April 22, 2014

"""

#system import
import random
# Math import
import settings

class Math():
	def __init__(self):
		self.storedVals = []

	# solve a math equation
	def math(self, sender, string):
		string = string.replace(' ', '') # remove whitespace
		index = string.find('=')
		if index != -1:
			return self.setVal(string[:index], string[index+1:])
		else:
			return self.solveRecursively(string)

	# delete indicated vlaue from stored values
	def delVal(self, sender, string):
		for attr in self.storedVals:
			if attr[0] == string:
				self.storedVals.remove(attr)
		raise MathError("Could not delete " + string + ": attribute not found")

	# set a stored value to be used later
	def setVal(self, name, string):
		eqIndex = string.find('=')
		substr = str(self.solveRecursively(string[eqIndex+1:]))
		# find index of name if it exists, if it doesnt, it will = len() 
		i = 0
		while i < len(self.storedVals) and self.storedVals[i][0] != name:
			i = i + 1
		if i == len(self.storedVals):
			self.storedVals.append([name, substr])
		else:
			self.storedVals[i][1] = substr
		return name + " = " + substr

	# delete all stored values
	def flush(self, sender, string):
		self.storedVals = []
		return "Values flushed"

	# replace all indicated values into the expression before solving
	def repVals(self, string):
		for attr in self.storedVals:
			string = string.replace(attr[0], str(attr[1]))
		return string

	# print all stored values
	def printVals(self, sender, string):
		out = ""
		for a in self.storedVals:
			out = out + "[%s = %s] " % (a[0], a[1])
		return out

	# solves a string equation using recursion (this handles input, errors, output)
	def solveRecursively(self, string):
		string = self.repVals(string)
		try:
			a = recur(string)
		except ValueError as error:
			return "Bad Value Error: " + str(error)
		except MathError as error:
			return "Calculation Error: " + str(error)
		except Exception as error:
			return "Unhandled Error: " + str(error)
		else:
			# try to convert float to int if flat decimal
			if a % 1 == 0:
				a = int(a)
			# return string representation of value
			return str(a)

# recursively solve the equation
def recur(string):
	# see if string is blank
	if string == "":
		raise MathError("Expression invalid or missing variables")
	# see if string is a number
	try:
		val = float(string)
	except ValueError:
		# string not a number, therefore is an expression
		# for each character in the string, find the OP the program needs
		# to do with regards to order of operations
		opIndex = 0 # arbitrary max, must start larger than any key in self.order
		a = 0
		while a < len(string):
			# skip parenthesis, need to stay on this level
			if string[a] == "(":
				b = skipParen(string[a:])
				# if parenthesis encloses entire equation, solve it
				if (a == 0 and b == (len(string) - 1)):
					return recur(string[1:-1])
				# otherwise set a to b, skipping the parenthesis
				a = a + b # not setting properly
			else:
				# find index of last operation to do, because solving
				# recursively will do this last
				if indexOp(string[opIndex], string[a]):
					opIndex = a
			a = a + 1
		# once for loop is done, recursively solve both sides
		a = recur(string[:opIndex])
		b = recur(string[opIndex + 1:])
		# then solve the equation "a string[opIndex] b"
		return solve(string[opIndex], a, b)
	# string is a number, return it
	return val

# solve an individual operation
def solve(charOP, left, right):
	if charOP == 'd':
		return randSum(left, right)
	elif charOP == '^':
		return pow(left, right)
	elif charOP == '*':
		return left * right
	elif charOP == '/':
		return left / right
	elif charOP == '+':
		return left + right
	elif charOP == '-':
		return left - right
	raise MathError("Invalid Operation found, could not solve")

# boolean true if opIndex should be switched with a
def indexOp(charOP, charA):
	try:
		a = settings.ORDER[charOP]
	except KeyError:
		a = settings.MAXINDEX
	try:
		b = settings.ORDER[charA]
	except KeyError:
		b = settings.MAXINDEX
	if a >= b:
		return True
	return False

# returns index where matching ')' is found, string contains initial '('
# if matching parenthesis not found, raise matherror
def skipParen(string):
	for a in range(1, len(string)):
		if string[a] == '(':
			a = skipParen(string[a:])
		elif string[a] == ')':
			return a
	raise MathError("unmatched parenthesis")

#returnds the sum of n random integers
def randSum(rolls, sides):
	try:
		rolls = int(rolls)
		sides = int(sides)
	except ValueError as error:
		raise
	else:
		if (rolls < settings.MINROLLS or rolls > settings.MAXROLLS):
			raise MathError("number of rolls outside of range")
		if (sides < settings.MINSIDES or sides > settings.MAXSIDES):
			raise MathError("number of sides outside of range")
		out = 0
		for i in range(0, rolls):
			out = out + random.randint(1, sides)
		return out

#custom error output
class MathError(Exception):
	def __init__(self, value):
		self.value = value

	def __str__(self):
		return repr(self.value)


