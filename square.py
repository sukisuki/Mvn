#!/usr/bin/env python
"""
this module contains one function: square

I was surprisedm when it worked. the idea was based on these two lines from wikipedia
 
http://en.wikipedia.org/wiki/Square_root_of_a_matrix:
(math notation converted to local python standard)
    '''if T = A*A.H = B*B.H, then there exists a unitary U s.t. 
    A = B*U'''

a unitary matrix is a complex rotation matrix
http://en.wikipedia.org/wiki/Unitary_matrix
    '''In mathematics, a unitary matrix is an nxn complex matrix U 
    satisfying the condition U.H*U = I, U*U.H = I'''
"""

import numpy
from matrix import Matrix
from operator import ge
from helpers import ascomplex

def square(vectors=None,var=None):
    """
    given a series of vectors, this function calculates:
        (variances,vectors)=numpy.linalg.eigh(vectors.H*vectors)
    it's a seperate function because if there are less vectors 
    than dimensions the process can be accelerated, it just takes some dancing
    """
    vectors=Matrix(vectors)
    shape=vectors.shape

    var = numpy.ones(shape[0]) if var is None else numpy.real_if_close(var)

    eig = numpy.linalg.eigh if Matrix(var) == abs(Matrix(var)) else numpy.linalg.eig

    var=var[:,numpy.newaxis]

    vectorsH=vectors.H
    vectors=Matrix(var*numpy.array(vectors))

    if not numpy.all(shape):
        var=numpy.zeros([0])
        vec=numpy.zeros([0,shape[1]])
    elif ge(*shape):
        cov=vectorsH*vectors
        (var,vec)=eig(vectorsH*vectors)
        vec=vec.H
    else:
        Xcov=vectors*vectorsH
        
        (Xval,Xvec)=eig(Xcov)
        
        var=numpy.diag(Xcov)
        
        vec=(Xvec.H*vectors).T
        vec=Matrix(((var**(-0.5+0j))*numpy.array(vec)).T)
        
    return (var,vec)

if __name__=='__main__':
    for n in xrange(1,20):
        shape=(numpy.random.randint(1,10),numpy.random.randint(1,10),2)
        vectors=Matrix(ascomplex(numpy.random.randn(*shape)))
        
        (var,vec)=square(vectors)
        var=Matrix(numpy.diagflat(var))
        
        assert vec.H*(var)*vec==vectors.H*vectors
