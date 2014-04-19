
#system import
import random
# Math import
import settings

def eval(sender, string):
	return recur(string)

def recur(string):
	# for each character in the string, find the OP the program needs to do
	for a in len(string):
		# skip parenthesis, need to stay on this level
		if string[a] == "(":
			a = skip_parenthesis(string[a+1:])
			# if parenthesis occured and reaced end of string, evaluate parenthesis
			if a >= len(string):
				return recur(string[1:-1])
		b = recur(string[:a])
		c = recur(string[a+1:])

		if string[a] == "^":
			return b ^ c
		elif string[a] == "*":
			return b * c
		elif string[a] == "/":
			return b / c
		elif string[a] == "+":
			return b + c
		elif string[a] == "-":
			return b - c
		elif string[a] == "d":
			return rand_sum(b, c)

def skip_parenthesis(string):
	for a in len(string):
		if string[a] == "(":
			a = skip_parenthesis(string[a+1:])
		elif string[a] == ")":
			return a+1

def rand_sum(rolls, sides):
	out = 0
	for i in rolls:
		out = put + random.randint(1, sides)
	return out