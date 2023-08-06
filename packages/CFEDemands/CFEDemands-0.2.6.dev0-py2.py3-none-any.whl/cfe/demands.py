# [[file:~/Research/CFEDemands/Demands/demands.org::demands][demands]]
# Tangled on Mon Apr 20 16:24:02 2020
from __future__ import print_function
from . import frischian
from . import hicksian
from . import marshallian
from ._core import lambdavalue, relative_risk_aversion, excess_expenditures, excess_expenditures_derivative, excess_utility, lambdaforU, expenditures
from ._utils import derivative, check_args
from numpy import array, log

def utility(x,alpha,beta,phi):
    """
    Direct utility from consumption of x.
    """
    n,alpha,beta,phi = check_args(alpha=alpha,beta=beta,phi=phi)

    U=0
    for i in range(n):
        if beta[i]==1:
            U += alpha[i]*log(x[i]+phi[i])
        else:
            U += alpha[i]*((x[i]+phi[i])**(1-1./beta[i])-1)*beta[i]/(beta[i]-1)

    return U

def marginal_utilities(x,alpha,beta,phi):
    """
    Marginal utilities from consumption of x.
    """
    n,alpha,beta,phi = check_args(alpha=alpha,beta=beta,phi=phi)

    MU=[]
    for i in range(n):
        MU += [alpha[i]*((x[i]+phi[i])**(-1./beta[i]))]

    return MU
# demands ends here
