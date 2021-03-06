import math
from OpenGL.GL import GLfloat
# todo python 2 - 3 compatibility fixes

def zero_vector(size):
    ''' Return a zero filled vector of the requested size '''
    return [0.0 for i in range(size)]

def identity(size):
    ''' Return an identity matrix of the requested size '''
    return [[1.0 if x==y else 0.0 for y in xrange(size)] for x in xrange(size)]

def zero_matrix(size):
    ''' Return a zero filled matrix of the requested size '''
    return [[0.0 for y in xrange(size)] for x in xrange(size)]

def matrix_multiply(matrixA, matrixB):
    ''' Multiplys matrixA with matrixB '''
    sizeA = len(matrixA)
    matOut = zero_matrix(sizeA)
    for i in range(sizeA):
        for j in range(sizeA):
            for k in range(sizeA):
                matOut[i][j] += matrixA[i][k] * matrixB[k][j]

    return matOut

def matrix_vector_multiply(matrix, vector):
    matSize = len(matrix)
    vecSize = len(vector)
    vecOut = vector.zero_vector(vecSize)
    for i in xrange(matSize):
        for j in xrange(matSize):
            vecOut[i] += vector[j] * matrix[i][j]
    return vecOut

def ortho(left, right, bottom, top, zNear, zFar):
    rtnMat = zero_matrix(4)
    rtnMat[0][0] = 2.0 / (right - left)
    rtnMat[1][1] = 2.0 / (top - bottom)
    rtnMat[2][2] = - 2.0 / (zFar - zNear)
    rtnMat[3][0] = - (right + left) / (float(right) - left)
    rtnMat[3][1] = - (top + bottom) / (float(top) - bottom)
    rtnMat[3][2] = - (zFar + zNear) / (float(zFar) - zNear)
    rtnObj = Matrix(4)
    rtnObj.matrix = rtnMat
    return rtnObj

def convert_to_1d_matrix(matrix):
    ''' Converts a 2d matrix list to be used with PyOpenGL '''
    length = len(matrix)
    tempMatrix = (GLfloat * (length * length))()
    for x in xrange(length):
        for y in xrange(length):
            print (x*length+y)
            tempMatrix[x*length+y] = matrix[x][y]
    return tempMatrix

def convert_matrix(matrix):
    ''' Converts a 2d matrix to be used with ctypes '''
    length = len(matrix)
    tempMatrix = (GLfloat * length * length)()
    for x in range(length):
        for y in range(length):
            tempMatrix[x][y] = matrix[x][y]
    return tempMatrix

class Vector(object):
    def __init__(self, size):
        self.size = size
        self.vector = zero_vector(size)

# Wrapper matrix object
class Matrix(object):
    def __init__(self, size=4):
        self.size = size
        # Initiaize identity Matrix
        self.matrix = identity(size)

    @property
    def c_matrix(self):
        return convert_matrix(self.matrix)
    
    def __mul__(self, other):

        if isinstance(other, Vector):
            result = matrix_vector_multiply(self.matrix, other.vector)
            vecOut = Vector(len(result))
            vecOut.vector = result
            return vecOut

        elif isinstance(other, Matrix):

            if other.size != self.size:
                errText = 'size {}, expected {}'.format(other.size, self.size)
                raise ValueError(errText)
            else:
                return matrix_multiply(self.matrix, other.matrix)

        else:
            return NotImplemented

    def __imul__(self, other):
        if isinstance(other, Matrix):

            if other.size != self.size:
                errText = 'size {}, expected {}'.format(other.size, self.size)
                raise ValueError(errText)
            else:
                self.matrix = matrix_multiply(self.matrix, other.matrix)
                return self
        else:
            return NotImplemented
