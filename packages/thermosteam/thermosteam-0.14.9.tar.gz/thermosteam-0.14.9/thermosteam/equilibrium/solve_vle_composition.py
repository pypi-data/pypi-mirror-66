# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 21:40:59 2019

@author: yoelr
"""
from flexsolve import wegstein
from ..functional import normalize

__all__ = ('solve_x', 'solve_y')

def x_iter(x, x_gamma_poyinting, gamma, poyinting, T):
    x = normalize(x)
    # Add back trace amounts for activity coefficients at infinite dilution
    mask = x < 1e-16
    x[mask] = 1e-16
    denominator = gamma(x, T) * poyinting(x, T)
    try:
        x = x_gamma_poyinting / denominator
    except FloatingPointError: 
        x[mask] = 0
        x = normalize(x)
    return x

def solve_x(x_gamma_poyinting, gamma, poyinting, T, x_guess=None):
    if x_guess is None: x_guess = x_gamma_poyinting
    return wegstein(x_iter, x_guess, 1e-6, args=(x_gamma_poyinting, gamma, poyinting, T))

def y_iter(y, y_phi, phi, T, P):
    y = normalize(y)
    return y_phi / phi(y, T, P)

def solve_y(y_phi, phi, T, P, y_guess):
    if y_guess is None: y_guess = y_phi
    return wegstein(y_iter, y_phi, 1e-6, args=(y_phi, phi, T, P))