__author__ = 'sam'
__version__ = 3 # !!!

import otherfunctions as of
from math_stuff import findRoots,find_x
from ast import literal_eval
from decimal import Decimal

operators = '+m*/^'

'''
This version is incomplete. There is no functional version
at the moment due to an extremely large change in one of the
dependencies.

New Approach:

    First, the unseen things, such as testing the equation for
    validity and converting all terms to Coefficent-X-Exponet
    (CXE) form. In this version, an E value other than 1 will
    be supported for terms with any X value. Also, the equation will
    be split into left and right sides.

    After that:

    1) Simplify inside of all parentheses and on other terms. (possibly
    using something similar to equation_solver2's Solve().simplify() method.
    2) Distribute where applicable, and remove excess parentheses.
    3) This version will support all operators - the next step is
    applying PEMDAS to both sides.
    4) Combine like terms (mostly for ease of use)
    5) Solve for x in the simplified equation.

Old Approach:

    First, incomplete validity testing was performed, and this
    restricted a lot of common equations. Also, all terms were converted
    to CXE form and the equation was split into sides, but a term with a
    False X value could not have an E value other than 1.

    After that:

    1) Distibution was done on both sides, but it depended on an
    equation where parentheses were only present if distribution was
    neccesary. Also there were problems with mysterious extra spaces.
    2) A feeble attempt at PEMDAS: parentheses would raise an error,
    exponets were only supported on terms with an X value of 1. Multiplication
    was done, which worked, but was inefficient. Also, divsion could only be
    done by multiplying the dividend by the quotient of the divisor and one.
    Addition was successfully performed, and subtraction was done by adding the
    inverse of the second addend. More problems with spaces.
    3) Terms were combined on both sides successfully.
    4) The equation was 'prepared', meaning solving the equation until the left
    side equaled 0.

Other changes:

    1) A change in equation syntax: there will be no spaces between the
    operators and terms.
    2) Changes in one of the solver's dependencies, that allow for more
    efficient and simpler code.
    3) This code will also be better documented.
    4) Note that this version will still only support one variable.
    5) Variables with a coefficient of 1 will not need the actual 1 to be there.
    
'''

def partition_list(terms,partition,replacement):
    string=of.join(terms)
    part=of.join(partition)
    parted = string.partition(part)
    back = of.separateAllKeep(parted[0],'(',')',*operators)
    end = of.separateAllKeep(parted[2],'(',')',*operators)
    finals = back+replacement+end
    return finals

class Solver():

    'main solve class take 2'

    def __init__(self,equation,identifier=0):
        self.equation = equation
        self.identifier = identifier

    def testEquation(self):
        if not self.identifier:
            pass
        else:
            pass

    def getSides(self):
        'gets the sides'
        sides = of.separate_temp(self.equation,'=')
        self.left = sides[0]
        self.right = sides[1]

    def CXE(self,string):
        raw_terms,terms = [of.separateAllKeep(string,'(',')',*operators),[]]
        for raw_term in raw_terms:
            if raw_term not in operators+'()' and '_' not in raw_term:
                if 'x' in raw_term:
                    if raw_term[0]=='x':
                        C = 1
                    else: 
                        C = float(raw_term[:of.getPlacement(raw_term,'x')[0]])
                    X = '1'
                else:
                    C = float(raw_term.partition('^')[0])
                    X = '0'
                raw_term = '%f_%s_%s'%(C, X, '1')
            terms.append(raw_term)
        return terms

    def sCXE(self,term):
        'splits CXE into C, X, and E.'
        return of.separateAll(term,'_')

    def unCXE(self,string):
        'returns terms to readable form from CXE'
        initial,finals = [of.separateAllKeep(string,'(',')',*operators),[]]
        for element in initial:
            if element not in operators+'()':
                CXE = self.sCXE(element)
                C = '' if (float(CXE[0]) == 1.0 and CXE[1]=='x') else CXE[0]
                X = 'x' if int(CXE[1]) else ''
                E = '' if CXE[2]=='1' else '^'+CXE[2]
                finals.append(C+X+E)
            else:
                finals.append(element)
        return finals

    def getInside(self,terms):
        tl,rl,number,append = [[],[],0,False]
        for term in terms:
            if term == '(':
                number += 1
                append = True
            elif term == ')':
                number-=1
                if not number:
                    tl.append(term)
                    rl.append(tl[1:][:-1])
                    append = False
                    tl = []
            if append: tl.append(term)
        return rl

    def trace(self,terms,start):
        direction = 1 if terms[start]=='(' else -1
        copystart,tf=[start,direction==1]
        begin,end,finals=[1 if tf else 0,0 if tf else 1,[]]
        while begin!=end:
            start+=direction
            term = terms[start]
            if term=='(':
                begin+=1
            elif term==')':
                end+=1
        if direction == 1:
            finals = [terms[x] for x in of.l_range(start,copystart+1)]
        else:
            finals = [terms[x] for x in of.l_range(copystart,start+1)]
        return finals

    def combineLikeTerms(self,terms):
        pass

    def exponets(self,inside,exponet):
        finals,C = [[],float(self.sCXE(exponet)[0])]
        for element in inside:
            if element not in operators:
                start = element # because otherwise its (x^2)^2 instead of x^3
                for i in of.l_range(C-1):
                    element = self.multiplication(element,start)
            finals.append(element)
        return finals

    def multiplication(self,term1,term2):
        CXE1,CXE2 = [[float(cxe1) for cxe1 in self.sCXE(term1)],
                     [float(cxe2) for cxe2 in self.sCXE(term2)]]
        C1,X1,E1 = CXE1
        C2,X2,E2 = CXE2
        VX = X1+X2
        if not C1 or not C2:
            return '0_0_1'
        elif not VX:
            return '%f_%d_%d'%(C1*C2,0,1)
        elif VX == 1:
            return '%f_%d_%d'%(C1*C2,1,1)
        else:
            return '%f_%d_%d'%(C1*C2,1,E1+E2)

    def multmult(self,term1s,term2s):
        terms=[]
        locop = operators+'()'
        for term1 in term1s:
            if term1 not in locop:
                for term2 in term2s:
                    if term2 not in locop:
                        terms.append(self.multiplication(term1,term2))
                    else:
                        pass #because the only thing you do is add them all together
            else:
                pass #same reason
        return of.separateAllKeep(of.join(terms,'+'),'+')

    def division(self,term1,term2):
        CXE1,CXE2 = [[float(cxe1) for cxe1 in self.sCXE(term1)],
                     [float(cxe2) for cxe2 in self.sCXE(term2)]]
        C1,X1,E1 = CXE1
        C2,X2,E2 = CXE2
        VX = X1+X2
        if not C1:
            return '0_0_1'
        elif not VX:
            return '%f_%d_%d'%(C1/C2,0,1)
        elif VX == 1: #assuming no division C0E/CXE, so if VX == 1 it means term1 X is 1.
            return '%f_%d_%d'%(C1/C2,1,E1)
        elif VX == 2:
            VE = E1-E2
            X = 1 if VE else 0
            if not VE: VE=1
            return '%f_%d_%d'%(C1/C2,X,VE)
        else:
            return [tuple(term1,term2),'the else condition was hit here.']

    def addition(self,term1,term2):
        CXE1,CXE2 = [[float(cxe1) for cxe1 in self.sCXE(term1)],
                     [float(cxe2) for cxe2 in self.sCXE(term2)]]
        C1,X1,E1 = CXE1
        C2,X2,E2 = CXE2
        if E1!=E2 or X1!=X2:
            return [term1,'+',term2]
        else:
            return '%f_%d_%d'%(C1+C2,X1,E1)#]
        
    def subtraction(self,term1,term2):
        return self.addition(term1,self.multiplication('-1_0_1',term2))

    def PEMDAS(self,terms):
        'do parentheses exponets multiplication division addition subtraction to simplify.'
        parents = self.getInside(terms)
        for parent in parents:
            new=self.PEMDAS(parent)
            if of.index(new)==1:
                terms = partition_list(terms,['(']+parent+[')'],new)
            else:
                terms = partition_list(terms,parent,new)
        terms=self.E(terms)
        #print terms
        terms=self.M(terms)
        #print terms
        terms=self.D(terms)
        #print terms
        terms=self.A(terms)
        #print terms
        terms=self.S(terms)
        #print terms
        return terms

    def E(self,terms):
        pows = of.getPlacement(terms,'^')
        for power in pows:
            try:
                before = terms[power-1]
                after = terms[power+1]
            except:
                break #remove !!!!!!!!!!!!!!!!!!!!!!!!1
            if before == ')':
                eterms = self.trace(terms,power-1)
            else:
                eterms = before
            if type(eterms)==list:
                terms=partition_list(terms,['(']+eterms+[')']+['^']+[after],self.exponets(eterms,after)) #no....
            else:
                terms=partition_list(terms,[eterms]+['^']+[after],self.exponets([eterms],after))
        return terms

    def M(self,terms):
        mults = of.getPlacement(terms,'*')
        for mult in mults:
            try:
                before = terms[mult-1]
                after = terms[mult+1]
            except:
                break #remove !!!!!!!!!!!!!!!!!!!!
            if before == ')':
                bterms = self.trace(terms,mult-1)
            else:
                bterms = before
            if after == '(':
                aterms = self.trace(terms,mult+1)
            else:
                aterms=after
            if type(bterms)==list:
                if type(aterms)==list:
                    terms=partition_list(terms,['(']+bterms+[')']+['*','(']+aterms+[')'],self.multmult(bterms,aterms))
                else:
                    terms=partition_list(terms,['(']+bterms+[')']+['*']+[aterms],self.multmult(bterms,[aterms]))
            else:
                if type(aterms)==list:
                    terms=partition_list(terms,[bterms]+['*','(']+aterms+[')'],self.multmult([bterms],aterms))
                else:
                    terms=partition_list(terms,[bterms]+['*']+[aterms],self.multmult([bterms],[aterms]))
        return terms

    def D(self,terms):
        divs = of.getPlacement(terms,'/')
        for div in divs:
            try:
                before = terms[div-1]
                after = terms[div+1]
            except:
                break  #remove !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
            terms=partition_list(terms,[before]+['/']+[after],[self.division(before,after)])
        return terms

    def A(self,terms):
        adds = of.getPlacement(terms,'+')
        for add in adds:
            try:
                before = terms[add-1]
                after = terms[add+1]
                terms=partition_list(terms,[before]+['+']+[after],[self.addition(before,after)])
            except IndexError:
                pass
        return terms

    def S(self,terms):
        subs = of.getPlacement(terms,'m')
        for sub in subs:
            #try:
            before = terms[sub-1]
            after = terms[sub+1]
            terms=partition_list(terms,[before]+['m']+[after],[self.subtraction(before,after)])
            terms = terms[0] if type(terms[0])==list else terms
            #except IndexError:
             #   pass
        return terms

    def combineLikeTerms(self,terms):
        locop,finals = operators+'()',{}
        for term in terms:
            if term not in locop:
                CXE = self.sCXE(term)
                C,X,E = CXE
                if (X,E) not in finals.keys():
                    finals[X,E] = term
                else:
                    finals[X,E]=self.addition(finals[X,E],term)
            else:
                pass
        return finals.values()

    def sort(self):
        finalleft,finalright=[[],[]]
        for term in self.right:
            CXE=self.sCXE(term)
            if int(CXE[1]):
                finalleft.append(self.multiplication(term,'-1_0_1'))
            else:
                finalright.append(term)
        for term in self.left:
            CXE = self.sCXE(term)
            if not int(CXE[1]):
                finalright.append(self.multiplication(term,'-1_0_1'))
            else:
                finalleft.append(term)
        self.highest_exponet = 1
        for term in finalleft:
            CXE=self.sCXE(term)
            if int(CXE[2])>self.highest_exponet:
                self.highest_exponet=int(CXE[2])
            else:
                pass
        return [self.combineLikeTerms(finalleft),self.combineLikeTerms(finalright)]

    def finish(self):
        for element in self.left:
            if element[0] == '0' and '.' not in element:
                self.left.remove(element)
        if self.highest_exponet == 1:
            CXE=self.sCXE(self.left[0])
            divisor=self.CXE(CXE[0])[0]
            left = self.division(self.left[0],divisor)
            right = self.division(self.right[0],divisor)
            return [left,right]
        else:
            return [['1_1_1'],[str(float(self.sCXE(self.right[0])[0])**(1.0/self.highest_exponet))+'_0_1']]

    def solve(self):
        self.getSides()
        if not self.identifier:
            self.left = self.CXE(self.left)
            self.right = self.CXE(self.right)
            self.left=self.PEMDAS(self.left)
            self.right=self.PEMDAS(self.right)
            self.left = self.combineLikeTerms(self.left)
            self.right = self.combineLikeTerms(self.right)
            self.left,self.right = self.sort()
            self.left,self.right = self.finish()
        else:
            'NOTE: FOR RIGHT NOW, THIS IS ONLY USABLE OUTSIDE OF INTERFACE MODE.'
            types=[find_x,findRoots]
            return 'x='+str(types[self.identifier-1](*literal_eval(self.equation)))
        return [self.left,self.right]

interface=int(raw_input('Interface? > '))

def interface_():
    while True:
        try:
            equation=raw_input('Type Equation: ')
            #identifier=int(raw_input('Identifier: '))
            instance=Solver(equation)#identifier)
            solution = instance.solve()
            solution = of.join([instance.unCXE(solution[0])[0],'=',instance.unCXE(solution[1])[0]])
            print solution
        except KeyboardInterrupt:
            print 'Interface exit.'
            break


if interface:
    interface_()

######################################################################

a=Solver('3x+2x*(5+4)+(2+3)+5^3=4x+(1+6)')
s=Solver('1x+60m3x*60*5x=1x+60m3x*60*6x')
terms_1 = ['(','2_1_1','+','4_0_1','+','5_1_1',')']
terms_2 = ['(','3_1_1','+','2_0_1',')']
