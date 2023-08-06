#!/usr/bin/env python
# [[file:~/Research/CFEDemands/Demands/engel_curves.org][No heading:1]]
# Tangled on Mon Apr 20 16:24:03 2020

"""
A collection of functions pertaining to graphing Engel Curves
"""

from itertools import cycle
from cfe import demands
from cfe._utils import check_args
import matplotlib.pyplot as plt
import matplotlib.transforms as transforms
from warnings import warn
import numpy as np

def line_to_axis(ax,x,y,xlabel=None,ylabel=None,fontsize=12):
    """
    Draw a line from a point x,y on to x and y axes ax.
    """
    v=ax.axis()

    if not (xlabel is None):
        ax.arrow(x,y,0,-(y-v[2])) # To x axis
        trans_x = transforms.blended_transform_factory(ax.transData, ax.transAxes)
        ax.text(x, -0.03, xlabel, transform=trans_x, fontsize=fontsize, va='center',ha='center')

    if not (ylabel is None):
        ax.arrow(x,y,-(x-v[0]),0.) # To y axis
        trans_y = transforms.blended_transform_factory(ax.transAxes, ax.transData)
        ax.text(-0.01, y, ylabel, transform=trans_y, fontsize=fontsize, va='center',ha='right')

def plot(p,alpha,beta,phi,labels=[],ybounds=[0,10],npts=100,fname=None,NegativeDemands=True,use_linestyles=False,shares=False,logs=True,use_figure=1,ax=None):
    """
    Plots ???
    """
    n,alpha,beta,phi = check_args(p,alpha,beta,phi)

    if not shares:
        foo=lambda y: demands.marshallian.demands(y,p,alpha,beta,phi,NegativeDemands=NegativeDemands)
    else:
        foo=lambda y: demands.marshallian.budgetshares(y,p,alpha,beta,phi,NegativeDemands=NegativeDemands)

    if NegativeDemands:
        ymin=-sum([p[i]*phi[i] for i in range(len(p))])
    else:
        ymin=0

    if ybounds[0]<=ymin: ybounds[0]=ymin+1e-12

    if ax is None:
        fig = plt.figure(use_figure)
        ax = fig.add_subplot(111)
    else: fig = ax.get_figure()

    if logs:
        Y = np.logspace(np.log10(ybounds[0]),np.log10(ybounds[1]),npts)
        D = [foo(y) for y in Y]
        lines = ax.semilogx(Y,D)
    else:
        Y = np.linspace(ybounds[0],ybounds[1],npts)
        D = [foo(y) for y in Y]
        lines = ax.plot(Y,D)

    if use_linestyles:
        ls=cycle(['-',':','--','-.'])  # See pl.Line2D.lineStyles.keys()
        for line in lines:
            line.set_ls(next(ls))

    if len(labels)>0:
        if shares: loc='upper right'
        else: loc='upper left'
        ax.legend(labels,loc=loc)

    if logs:
        ax.set_xlabel('Log Total Expenditures',x=1.,fontsize=16,ha='right')
    else:
        ax.set_xlabel('Total Expenditures',x=1.,fontsize=16,ha='right')

    if shares:
        label='Particular Expenditure Shares'
    else:
        label='Particular Expenditures'
    ax.set_ylabel(label,y=1.,fontsize=16,ha='right')

    if fname:
        fig.savefig(fname)
    else:
        fig.show()

    return lines,ax

def plot_demands(p,y,alpha,beta,phi,labels=[],ybounds=[0,10],npts=100,fname=None,NegativeDemands=True,use_linestyles=False,shares=False,logs=True,use_figure=1):
    """Plot demands for all goods as a function of price of good 0."""

    n,alpha,beta,phi = check_args(p,alpha,beta,phi)

    prices=lambda p0: [p0]+list(p[1:])
    if not shares:
        f=lambda p0: demands.marshallian.demands(y,prices(p0),alpha,beta,phi,NegativeDemands=NegativeDemands)
    else:
        f=lambda p0: demands.marshallian.budgetshares(y,prices(p0),alpha,beta,phi,NegativeDemands=NegativeDemands)

    if NegativeDemands:
        ymin=-sum([p[i]*phi[i] for i in range(len(p))])
    else:
        ymin=0

    if ybounds[0]<=ymin: ybounds[0]=ymin+1e-12

    plt.figure(use_figure)
    plt.clf()
    X=[]

    if logs:
        Y=plt.logspace(np.log10(ybounds[0]),np.log10(ybounds[1]),npts)
        D = [f(y) for y in Y]
        lines = plt.semilogx(Y,D)
    else:
        Y = plt.linspace(ybounds[0],ybounds[1],npts)
        D = [f(y) for y in Y]
        lines = plt.plot(Y,D)


    if use_linestyles:
        ls=cycle(['-',':','--','-.'])  # See plt.Line2D.lineStyles.keys()
        for line in lines:
            line.set_ls(next(ls))

    if len(labels)>0:
        if shares: loc='upper right'
        else: loc='upper left'
        plt.legend(labels,loc=loc)

    if logs:
        plt.xlabel(r'$\log p_1$',x=1.,fontsize=16,ha='right')
    else:
        plt.xlabel('$p_1$',x=1.,fontsize=16,ha='right')

    if shares:
        label='Particular Expenditure Shares'
    else:
        label='Particular Expenditures'
    plt.ylabel(label,y=1.,fontsize=16,va='center')

    if fname:
        plt.savefig(fname)
    else:
        plt.show()

    return p,ax

if __name__=='__main__':
    line = plot([1.,1.,1.],[1.,2.,3.],[1.,1.,1.],[-0.01,0.,0.])
# No heading:1 ends here
