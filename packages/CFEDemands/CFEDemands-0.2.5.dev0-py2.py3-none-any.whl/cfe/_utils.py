# [[file:~/Research/CFEDemands/Demands/demands.org::demand_utils][demand_utils]]
# Tangled on Mon Apr 20 12:53:12 2020
from scipy import optimize 
from numpy import array, ones, zeros, sum, log, Inf, dot, nan, all, max
import warnings

def check_args(p=None,alpha=None,beta=None,phi=None):
    """
    Perform sanity check on inputs.  Supply default values if these are missing.
    """

    N = []
    # Make sure all args are of type array:
    if p is not None:
        p=array(p,dtype=float)
        N.append(len(p))

    try: 
        len(alpha) # If len() not defined, then must be a singleton
        alpha=array(alpha,dtype=float)
        N.append(len(alpha))
    except TypeError: alpha=array([alpha],dtype=float)

    try:
        len(beta) # If len() not defined, then must be a singleton
        beta = array(beta,dtype=float)
        N.append(len(beta))
    except TypeError: beta = array([beta],dtype=float)

    try:
        len(phi) # If len() not defined, then must be a singleton
        phi=array(phi,dtype=float)
        N.append(len(phi))
    except TypeError: phi=array([phi],dtype=float)

    n = max(N)

    if len(alpha)==1<n:
        alpha=ones(n)*alpha
    else:
        if not alpha.all():
            raise ValueError

    if len(beta)==1<n:
        beta = ones(n)*beta
    else:
        if not beta.all():
            raise ValueError("Problem with beta?")
        if not all(beta>0):
            raise ValueError("Non-positive beta?")
    
    if len(phi)==1<n:
        phi=ones(n)*phi

    return (n,alpha,beta,phi)

def derivative(f,h=2e-5,LIMIT=False):
    """
    Computes the numerical derivative of a function with a single scalar argument.

    - h :: A precision parameter.  

    BUGS: Would be better to actually take a limit, instead of assuming that h 
    is infinitesimal.  
    """
    def df(x, h=h):
        return ( f(x+h/2) - f(x-h/2) )/h
    return df
# demand_utils ends here
