import math
import operator

def map2Method(f):
	"""Return a function that implements a simple mapping
	 from a two argument function"""
	def method(self, other):
		return self.map2(f, other)
	return method

def mapMethod(f):
	"""get a function that implements a simple mapping
	 from a single argument function"""
	def method(self):
		return self.map(f)
	return method

class Point():
	"""Represents a point in 2D space"""
	
	def __init__(self, *args, **kwargs):
		#get the type to use from the kwargs, default to int
		self.type = kwargs.get("type", int)

		# was i passed keyword args?
		if 'x' in kwargs and 'y' in kwargs:
			self.set(kwargs['x'], kwargs['y'])
			
		# is it empty? init to 0
		elif len(args) == 0:
			self.set(0,0)
			
		# 1 argument:
		elif len(args) == 1:
			# is it a string:
			if type(args[0]) in (str, unicode):
				self.fromStr(args[0])
			# does it look like a point with x & y arrtibutes?
			elif hasattr(args[0], "x") and hasattr(args[0], "y"):
				self.set(args[0].x, args[0].y)
			# same, except caps
			elif hasattr(args[0], "X") and hasattr(args[0], "Y"):
				self.set(args[0].X, args[0].Y)
			# does it look like a list or tupple?
			elif hasattr(args[0], "__iter__"):
				self.set(args[0][0], args[0][1])
			# fail
			else:
				raise TypeError
			
		# was i passed an x & y value?
		elif len(args) == 2:
			self.set(args[0], args[1])
		# fail
		else:
			raise TypeError
		

	def fromStr(self,string):
		"""Loads from a string, which consists of two numbers, seperated
		by something(,;:-| ), possibly wrapped in brackets.
		It also handles any unnecesary spaces."""
		# space is last so that (4, 2) works
		for sep in ",;:-| ":
			if sep in string:
				# strip spaces & brakets, split on sep,
				# correct their type, then pass to set
				self.set(*string.strip("( )").split(sep))
				return
		raise ValueError("'%s' is not a valid point" % string)

	def new(self, x, y):
		"""create a new point obj with the same type"""
		return Point(x,y,type=self.type)

	def cast(self, type):
		"""Return a new point of type type."""
		return Point(self.x, self.y, type=type)

	def set(self, x, y):
		"""Set the x and y attributes, converting them the the corect type."""
		self.x = self.type(x)
		self.y = self.type(y)

	def copy(self):
		"""Return a new, but identical point."""
		return self.new(self.x, self.y)

	def map(self, f):
		"""returns a new point with f applied to x&y"""
		return self.new(f(self.x), f(self.y))

	def map2(self, f, other):
		"""return a new point with f applied to x&y,
		 using other as the second arg"""
		# other can be either a point or a number
		try:
			return self.new(f(self.x, other.x), f(self.y, other.y))
		except AttributeError:
			return self.new(f(self.x, other), f(self.y, other))

	
	#overload operators so that + - * / ** can be used.
	#Works with Point+Point and Point+number.
	#the operator module holds functions that have
	# the same effect as built in operators.
	# eg. x+y == operator.add(x,y)

	__add__ = map2Method(operator.add)
	__sub__ = map2Method(operator.sub)
	__mul__ = map2Method(operator.mul)
	__div__ = map2Method(operator.div)
	__pow__ = map2Method(operator.pow)
	__neg__ = mapMethod(operator.neg)
	## Round down
	floor = mapMethod(math.floor)
	
	def __eq__(self,other):
		"""is self equal to other?"""
		return self.x == other.x and self.y == other.y
	
	def __ne__(self,other):
		"""is self different from other?"""
		return self.x != other.x or self.y != other.y

	def __abs__(self):
		"""the distancefrom (0,0)"""
		return math.sqrt(self.x**2 + self.y**2)

	def dot(self, other):
		"""The dot product."""
		return (self.x * other.x) + (self.y * other.y)

	
	def withMagnitude(self, value):
		"""scale the magnitude of the point"""
		return self * (value/abs(self))

	def __iter__(self):
		"""return self as an iterator"""
		return iter((self.x, self.y))

	def __str__(self):
		"""get the user string representation"""
		return "(%s, %s)" % (self.x, self.y)

	def __repr__(self):
		"""get the pythonic string representation"""
		return "Point(%s, %s)" % (self.x, self.y)

	def round(self, n=0):
		"""Round both coords to n(0) decimal places"""
		return self.map2(round, n)

	@property
	def xmlStr(self):
		"""get the coords in the format 'x y'"""
		return "%s %s" % (self.x, self.y)

	def dist(self, other):
		"""Find the distance between self & other"""
		return abs(self-other)


def lineToPointDist(p1, p2, p):
	"""Find the distance between the line p1->p2 and point p
	, where p1!=p2
	"""
	# u is the distance along the line (from 0 to 1)
	u = (p - p1).dot(p2 - p1) / abs(p2-p1)**2

	if u<=0:
		# p is past the start
		return abs(p-p1)
	elif u>=1:
		# p is past the end
		return abs(p-p2)
	else:
		# p is in the middle somewhere
		return abs(p - p1 - (p2 - p1) * u)
