import numpy as np

def Delta(n0, lb, rb):
    # n0 is where Delta == 1
    # from left bound (lb) to right bound (rb)
    n = np.arange(lb, rb+1, 1)
    x = np.array((n - n0) == 0)
    x = x.astype('float')
    return x, n

def UnitStep(n0, lb, rb):
    # n0 is where UnitStep starting == 1
    # from left bound (lb) to right bound (rb)
    n = np.arange(lb, rb+1, 1)
    x = np.array((n - n0) >= 0)
    x = x.astype('float')
    return x, n

def Rectangle(n0, n1, lb, rb):
    # n0 is where UnitStep starting == 1
    # n1 is where UnitStep ending == 1
    # from left bound (lb) to right bound (rb)
    n = np.arange(lb, rb+1, 1)
    # numpy is stupid not me, I swear matlab does better here.
    temp1 = n - n0 >= 0
    temp2 = n1 - n >= 0
    x = np.array(temp1 * temp2)
    #>
    x = x.astype('float')
    return x, n

def Exp(a, b, c, lb, rb): # Should not be confused with numpy.exp()
    # a.b^(c.t)
    # from left bound (lb) to right bound (rb)
    n = np.arange(lb, rb+1, 1)
    x = a * (b ** (c*n))
    return x, n

def ComplexExp(a, phi, omega, lb, rb): # You can use dsp_py.Exp() instead but this is pure and better if you need complex exponential signal
    # a.e^((phi + j.omega).t)
    # from left bound (lb) to right bound (rb)
    n = np.arange(lb, rb+1, 1)
    x = a * np.exp((phi + 1j*omega)*n)
    return x, n

def Sin(A, w, p, lb, rb):
    # A is amplitude
    # w is omega
    # p is phase
    n = np.arange(lb, rb+1, 1)
    x = A * np.sin(w*n + p)
    return x, n

def Cos(A, w, p, lb, rb):
    # A is amplitude
    # w is omega
    # p is phase
    n = np.arange(lb, rb+1, 1)
    x = A * np.cos(w*n + p)
    return x, n
