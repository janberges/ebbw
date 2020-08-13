#!/usr/bin/env python3

import sys
sys.path.append('..')

import ebbw
import ebbw2
import numpy as np

epsilon = 1e-2

T0 = lambda: 1.0 + 100.0 * np.random.rand()

l = 1.0
u = 0.1
w = 0.02
E = 1.0
W = 15.0

Tc0 = 19.734507869 # ebbw.epsilon = 1e-30, critical(epislon=1e-16)

Tc1 = ebbw.critical(T=T0(), l=l, u=u, w=w, E=E, W=W)

Tc2 = ebbw2.critical(T=T0(), l1=l/2, l2=l/2, u=u, w1=w, w2=w, E1=E, E2=E, W=W)

if abs(Tc0 - Tc1) > epsilon:
  print('ebbw does not yield expected result')

elif abs(Tc1 - Tc2) > epsilon:
  print('ebbw and ebbw2 disagree')

else:
  print('All tests passed')
