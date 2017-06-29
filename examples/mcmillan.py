#!/usr/bin/env python

import sys
sys.path.append('..')

import ebbw
import numpy as np
import matplotlib.pyplot as plt

N = 101

TcEB = np.empty(N)
TcMM = np.empty(N)

variables = [
   ('l', np.linspace(0.50, 2.50, N), r'$\lambda$'),
   ('u', np.linspace(0.00, 0.30, N), r'$\mu$'),
   ('w', np.linspace(0.01, 0.03, N), r'$\omega_{\mathrm{E}} / \mathrm{eV}$'),
   ('E', np.linspace(1e-1, 1e+1, N), r'$E / \mathrm{eV}$'),
   ]

defaults = dict(T=10.0, l=1.0, u=0.1, w=0.02, E=1.0, W=15.0)

figure = plt.figure()

for position, (key, x, label) in enumerate(variables, 221):
   parameters = defaults.copy()

   for i, parameters[key] in enumerate(x):
      print '%s = %g' % (key, parameters[key])

      TcEB[i] = parameters['T'] = ebbw.critical(**parameters)
      TcMM[i] = ebbw.Tc(**parameters)

   plt.subplot(position)

   plt.plot(x, TcEB, label='Eliashberg')
   plt.plot(x, TcMM, label='McMillan')

   plt.xlabel(label)
   plt.ylabel(r'$T_{\mathrm{c}} / \mathrm{K}$')

plt.legend(loc='lower right', frameon=False, prop={'size': 'medium'})

plt.suptitle(r'(The default parameters are $\lambda = %(l)g$, $\mu = %(u)g$, '
   r'$\omega_{\mathrm{E}} = %(w)g\,\mathrm{eV}$, $E = %(E)g\,\mathrm{eV}$ and '
   r'$\omega_N = %(W)g\,\omega_{\mathrm{E}}$)' % defaults, y=0)

plt.tight_layout()

figure.savefig('mcmillan.pdf', bbox_inches='tight')
