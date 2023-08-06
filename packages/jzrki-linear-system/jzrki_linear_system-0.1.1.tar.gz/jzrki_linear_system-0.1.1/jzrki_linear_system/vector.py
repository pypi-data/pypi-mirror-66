from math import sqrt, sin, acos, degrees, pi
from decimal import Decimal, getcontext

getcontext().prec = 30

class Vector(object):
    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([Decimal(x) for x in coordinates])
            self.dimension = len(coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')
            
    def __len__(self):
        return len(self.coordinates)

    def __getitem__(self, i):
        return self.coordinates[i]


    def __str__(self):
        return 'Vector: {}'.format([float(x) for x in self.coordinates])

    def __iter__(self):
        pass

    def __eq__(self, v):
        return self.coordinates == v.coordinates
    
    def __add__(self, v):
        return Vector([x+y for x,y in zip(self.coordinates, v.coordinates)])
    
    def __sub__(self, v):
        return Vector([x-y for x,y in zip(self.coordinates, v.coordinates)])
    
    def __mul__(self, a):
        return Vector([x*Decimal(a) for x in self.coordinates])

    def __truediv__(self, a):
        try:
            return Vector([x/Decimal(a) for x in self.coordinates])
        except:
            raise Exception('Cannot divide by zero!!!')
    
    def __rmul__(self, a):
        return self*a
    
    def mag(self):
        return Decimal(sqrt(sum([x**2 for x in self.coordinates])))
    
    def norm(self):
        return self/self.mag()
    
    def dot(self, v):
        return sum([x*y for x,y in zip(self.coordinates, v.coordinates)])
    
    def angle(self, v, ind = 'r'):
        rad = acos(self.norm().dot(v.norm()))
        if ind == 'd':
            return degrees(rad)
        else:
            return rad
        
    def is_para(self, v):
        return abs(abs(self.dot(v))-self.mag()*v.mag()) < 0.0001
    def is_orthog(self, v):
        return abs(self.dot(v)) < 0.0001
    
    def proj_para(self, b):
        b_unit = b.norm()
        return self.dot(b_unit) * b_unit
    def proj_orthog(self,b):
        return self - self.proj_para(b)
    
    def xprod(self, v):
        x, y, z = zip(self.coordinates, v.coordinates)
        return Vector([y[0]*z[1]-y[1]*z[0], -x[0]*z[1]+x[1]*z[0], x[0]*y[1]-x[1]*y[0]])
    
    def is_zero(self):
        return sum(self.coordinates) == 0