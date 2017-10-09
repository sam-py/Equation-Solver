#   --- Equation Solver 4 ---
__author__ = 'sam'
__version__ = 4.0

from otherfunctions import separateAllKeep,l_range,getPlacement,getOccurences, \
     separate_temp,index,begins,separateAll

variables = 'abcdfghjklmnopqrstuvwxyz'
operators = '+-*/^'
opandpar = operators+'()'

class Term():

    'base class for all terms.'

    def __init__(self,term):
        #print 'New Term Object: %s'%self
        self.initial_term = term
        self.opr = term in opandpar
        print 'a new Term (%s) was created then'%self
        #if term w/self.divisor value is divided again, multiply the current divisor and new one.

    def get_properties(self):
        string=''
        if not self.opr:
            self.coefficient = 1
            self.variables = []
            self.exponet = 1
            self.divisor = 1
            for componet in self.initial_term:
                if componet in variables:
                    self.variables.append(componet)
                    string+=' '
                else:
                    string+=componet
            numbers,number = separateAll(string,' '),1
            for num in numbers:
                number*=float(num)
            self.coefficient = number
        else:
            pass
        print 'the properties of Term (%s) were obtained then'%self

    def power(self,term):
        pass

    def multiply(self,term):
        if self.divisor == 1:
            self.coefficient*=term.coefficient
            self.variables+=term.variables
            self.exponet*=term.exponet
            self.divisor*=term.divisor
        else:
            divide(term)
        print 'Term (%s) was multiplied by Term (%s) then'%(self,term)
        del term
        

    def divide(self,term):
        #self.divisor*=term
        pass

    def add(self,term):
        pass

    def subtract(self,term):
        pass

    def __str__(self):
        return 'Term: %s Type - Opr=%d'%(self.initial_term,self.opr)

    def __repr__(self):
        return 'Term: %s Type - Opr=%d'%(self.initial_term,self.opr)

class Group():

    def __init__(self,max_terms):
        #print 'New Group Object: %s'%self
        for i in l_range(index(max_terms)):
            setattr(max_terms[i],'group',self)
            setattr(self,'term%d'%i,max_terms[i])
        print 'a Group was created (%s) then'%self

    def add(self,element):
        setattr(self,'term%d'%self.__len__()+1,element)
        print 'an element (%s) was added to Group (%s) then'%(str(element),self)

    def remove(self,location):
        print 'an element (%s) was removed from Group (%s) then'%(str(self.__dict__[location]),self)
        del self.__dict__[location]
        self.__dict__[location]='NONE'

    def replace(self,location,new):
        print 'an element (%s) was replaced by a new one (%s) in Group (%s) then'%(str(self.__dict__[location]),str(new),self)
        self.remove(location)
        self.__dict__[location] = new

    def clear(self):
        print 'all empty spaces were cleared from Group (%s) then'%(self)
        for key in self.__dict__.keys():
            if self.__dict__[key] == 'NONE':
                delattr(self,key)

    def terms(self):
        return self.__dict__.values()

    def __len__(self):
        return index(self.__dict__)

    def __getitem__(self,item):
        return self.__dict__['term%d'%item]

    def __str__(self):
        return str(self.terms())

    def __repr__(self):
        return str(self.terms())

class Solver():

    'main solve class.'

    def __init__(self,equation):
        print 'New Solver Object: %s'%self
        self.equation = equation

    def fix_errors(self):
        'add/remove characters, fix syntax and other problems.'
        pass

    def detect_pattern(self):
        'find the form of the equation: to be called after simplification.'
        pass

    def make_terms(self):
        'create a Term object for all terms.'
        self.left,self.right = [Term(term) for term in self.left],[Term(term) for term in self.right]
        self.left,self.right = Group(self.left),Group(self.right)
        for left,right in zip(self.left.terms(),self.right.terms()):
            left.get_properties()
            right.get_properties()
        print 'Term objects were created for each term in the equation (%s) then'%self.equation

    def solve(self):
        'stitch everything together.'
        sides = separate_temp(self.equation,'=')
        print 'the equation was split into left and right then'
        self.left = separateAllKeep(sides[0],*opandpar);self.right = separateAllKeep(sides[1],*opandpar)
        print self.left,'\n'
        self.make_terms()
        print 'the equation was solved.'
        return self.left

s = Solver('3x+4-7*5=4/2^3y+(5*3)')
