import numpy as np
from math import sqrt

def mul_dim_rosen(x):
	n = len(x) #number of dimensions
	if n < 2:
		return "Error, there need to be at least 2 dimensions"
	f = 0
	for i in range(0, n-1):
		f += 100*(x[i+1] - x[i]**2)**2 + (1-x[i])**2
	return f

def init_tetrahedron(x0, c):
	#x is a list (length n+1) of arrays (length n) which are the vertices of the hypertetrahedron
	x = [x0]
	n = len(x0)
	b = (c/(n*sqrt(2)))*(sqrt(n+1)-1)
	a = b + c/sqrt(2)
	var = b*np.ones(n)
	for i in range(0, n):
		var[i] = a
		x.append(x0+var)
		var[i] = b
	return x
	
def simplex(fun, x0, c):
	#fun takes as inputs x (a point with n design variables) and outputs function value
	
	#initialize hypertetrahedron and calculate function values at vertices
	n = len(x0)
	xin = init_tetrahedron(x0, c)
	vertices = np.array([]) #this is the function value at each vertice of the tetrahedron
	for i in range(n+1):
		vertices = np.append(vertices, fun(xin[i]))
		
	#calculate worst, best, and lousy points
	worst = np.argmax(vertices) #index of the worst point
	best = np.argmin(vertices) #index of the best point
	fw = vertices[worst] #function value of the worst point
	fb = vertices[best] #function value of the best point
	xw = xin[worst] #worst point
	xb = xin[best] #best point
	xin.pop(worst) #remove the worst point to calculate the lousy point
	vertices = np.delete(vertices, worst) #remove the worst function value to calculate the lousy point
	lousy = np.argmax(vertices) #index of the lousy point
	fl = vertices[lousy] #function value of the lousy point
	xl = xin[lousy] #lousy point
	
	#Evaluate x average and perform reflection
	xa = (1./n)*sum(xin) #average of points excluding the 1st
	alpha_r = 1.
	xr = xa + alpha_r*(xa-xw)
	fr = fun(xr)
	
	#If reflection is better than best, look at expanding
	if fr < fb:
		alpha_e = 1.
		xe = xr + alpha_e*(xr-xa)
		fe = fun(xe)
		if fe < fb: #accept expansion
			xin.append(xe)
			vertices = np.append(vertices, fe)
		else: #stick to the original reflection
			xin.append(xr)
			vertices = np.append(vertices, fr)
			
	#If reflection is better than lousy, accept reflection		
	elif fr <= fl:
		xin.append(xr)
		vertices = np.append(vertices, fr)
		
	#if reflection is worse than worst, perform contraction	
	else:	
		if fr > fw: #do an inside contraction
			beta = 0.5
			xc = xa - beta*(xa-xw)
			fc = fun(xc)
			if fc < fw: #accept contraction
				xin.append(xc)
				vertices = np.append(vertices, fc)
			else: #shrink the simplex
				#i need to add the shrink simplex code here
		else: #do an outside contraction
			beta = 0.5
			xo = xa + beta*(xa-xw)
			fo = fun(xo)
			if fo <= fr: #accept contraction
				xin.append(xo)
				vertices = np.append(vertices, fo)
			else: #shrink the simplex
				#add the shrink simplex code here
	return xin
	
if __name__=='__main__':
	x0 = np.array([0.0, 0.0, 0.0])
	c = 1.
	simplex(mul_dim_rosen, x0, c)
	
	