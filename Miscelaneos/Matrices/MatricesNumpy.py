from numpy import *

A= matrix([[1,1,1,1], [1,1,1,1], [1,1,1,1], [1,1,1,1]])
#A= ones([4,4])
print(A)
print()
B= matrix([[1,2,3,4]])
L= B.shape
K= ones([L[0]+1,4],dtype=int)
print(B)
print()
K[0]= B
B=K
print(B)
print(K)


#for punto in A:
#        print(punto)    
        #punto.append(1)
#print(B)

C= A.dot(B.T)
#print(C)

D= dot(A,B.T).T
#print(D)


