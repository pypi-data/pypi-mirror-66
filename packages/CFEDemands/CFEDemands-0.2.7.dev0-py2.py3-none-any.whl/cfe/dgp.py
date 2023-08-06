# [[file:~/Research/CFEDemands/Empirics/cfe_estimation.org::lambdas_dgp][lambdas_dgp]]
# Tangled on Fri Apr 24 13:45:39 2020
from scipy.stats.distributions import lognorm
import numpy as np
import xarray as xr

def geometric_brownian(sigma=1.):
    return lognorm(s=sigma,scale=np.exp(-(sigma**2)/2))

def lambdabar(T,M,Fbar):
    return xr.DataArray(np.cumprod(Fbar.rvs(size=(T,M)),axis=0),
                        dims=('t','m'),
                        coords={'t':range(T),'m':range(M)})

def lambdas(N,T,M=1,G0=lognorm(.5),Fbar=geometric_brownian(.1),F=geometric_brownian(.2)):

    L0 = xr.DataArray(G0.rvs(size=(N,1,M)),dims=('j','t','m'),
                    coords={'j':range(N),'t':range(1),'m':range(M)})  # Initial lambdas
    innov = xr.DataArray(F.rvs(size=(N,T-1,M)),dims=('j','t','m'),
                             coords={'j':range(N),'t':range(1,T),'m':range(M)})

    L = xr.concat((L0,innov),dim='t').transpose('j','t','m')
  
    # Add aggregate shocks Lbar:
    return L*lambdabar(T,M,Fbar=Fbar)
# lambdas_dgp ends here

# [[file:~/Research/CFEDemands/Empirics/cfe_estimation.org::characteristics_dgp][characteristics_dgp]]
# Tangled on Fri Apr 24 13:45:39 2020
def characteristics(N,T,M=1): 
    z = lambdas(N,T,M,Fbar=geometric_brownian(.05),F=geometric_brownian(0.1))
    return z
# characteristics_dgp ends here

# [[file:~/Research/CFEDemands/Empirics/cfe_estimation.org::prices_dgp][prices_dgp]]
# Tangled on Fri Apr 24 13:45:39 2020
def prices(T,M,n,G0=lognorm(.5),Fbar=geometric_brownian(.05),F=geometric_brownian(.2)):

    P0 = xr.DataArray(G0.rvs(size=(n,1,M)),dims=('i','t','m'),
                      coords={'i':range(n),'t':range(1),'m':range(M)})  # Initial lambdas
    innov = xr.DataArray(F.rvs(size=(n,T-1,M)),dims=('i','t','m'),
                               coords={'i':range(n),'t':range(1,T),'m':range(M)})

    P = xr.concat((P0,innov),dim='t').transpose('t','m','i')
    
    # Add aggregate shocks L0:
    return P*lambdabar(T,M,Fbar=Fbar)
# prices_dgp ends here

# [[file:~/Research/CFEDemands/Empirics/cfe_estimation.org::expenditures_dgp][expenditures_dgp]]
# Tangled on Fri Apr 24 13:45:39 2020
import pandas as pd
from scipy.stats import distributions
import numpy as np

def measurement_error(N,T,M,n,mu_phi=0.,sigma_phi=0.,mu_eps=0.,sigma_eps=1.):
    """Return samples from two measurement error processes; one additive, the other  multiplicative.
  
    - The additive error (phi) is a normal distribution with mean
      =mu_phi= and standard deviation =sigma_phi=.
    
    - The multiplicative error (eps) is a log-normal distribution with mean
      =mu_eps= and standard deviation =sigma_eps=.
    """

    def additive_error(N=N,T=T,M=M,n=n,sigma=sigma_phi):
        return xr.DataArray(distributions.norm.rvs(scale=sigma,size=(N,T,M,n)) + mu_phi,dims=('j','t','m','i'))

    def multiplicative_error(N=N,T=T,M=M,n=n,sigma=sigma_eps):
        return xr.DataArray(np.exp(distributions.norm.rvs(loc=-sigma/2.,scale=sigma,size=(N,T,M,n)) + mu_eps),dims=('j','t','m','i'))

    phi=additive_error(N,T,M,n,sigma=sigma_phi)
    eps=multiplicative_error(N,T,M,n,sigma=sigma_eps)

    return phi,eps

def expenditures(N,T,M,n,k,beta,mu_phi=0,sigma_phi=0.,mu_eps=0,sigma_eps=0.,Fbar=geometric_brownian(.001),p=None):
    """Generate artificial expenditures for $N$ households in $M$ markets
    over $T$ periods on $n$ items.  Return dataframe of expenditures
    and a dictionary of "true" underlying variables, the latter as
    type =xarray.DataArray=.

    Households are distinguished by a $k$-vector of characteristics,
    but common Frisch elasticities expressed as an $n$-vector beta.

    If supplied, optional arguments
    (mu_phi,sigma_phi,mu_eps,sigma_eps) describe the parameters of two
    different measurement error processes.  The first is a normally
    distributed additive measurement error process, with mean =mu_phi=
    and standard deviation =sigma_phi=.  The second is a
    multiplicative log-normal error process, with (log) mean =mu_eps=
    and (log) standard deviation =sigma_eps=.

    An optional xarray of prices =p= can also be provided.

    Ethan Ligon                                                     January 2018
    """

    if len(beta.shape)<2:
        Theta=xr.DataArray(np.diag(beta),dims=('i','ip'))
    else:
        Theta=xr.DataArray(beta,dims=('i','ip'))

    beta=Theta.sum('ip') # Row sum of elasticity matrix

    l = lambdas(N,T,M,Fbar=Fbar)
    
    foo = xr.DataArray(data=[chr(i) for i in range(ord('a'),ord('a')+k)],name='k',dims='k')

    dz = xr.concat([characteristics(N,T,M) for i in range(k)],dim=foo)

    L = np.reshape(l,(N,T,M)) 
    
    if p is None:
        p = prices(T,M,n)

    # Build x in steps
    #x = np.kron(np.log(L),-beta)
    x = np.log(L)*(-beta)
    x = x + np.log(p) - (Theta*np.log(p)).sum('ip') 
    x = x + np.log(dz).sum('k')

    x = np.exp(x)

    phi,e=measurement_error(N,T,M,n,mu_phi=mu_phi,sigma_phi=sigma_phi,mu_eps=mu_eps,sigma_eps=sigma_eps)

    truth = xr.Dataset({'beta':beta,'lambdas':l,'characteristics':dz,'prices':p,'x0':x})

    x = (x + p*phi) # Additive error
    x = x*e # Multiplicative error

    x = x*(x>0) # Truncation

    return x,truth
# expenditures_dgp ends here
