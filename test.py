#!/usr/bin/env python

import ebbw
import numpy as np
import matplotlib.pyplot as plt

N = 100

TcEB = np.empty(N)
TcMM = np.empty(N)

variables = [
   ('l', np.linspace(0.50, 2.50, N), r'$\lambda$'),
   ('u', np.linspace(0.00, 0.30, N), r'$\mu$'),
   ('w', np.linspace(0.01, 0.03, N), r'$\omega_{\mathrm{E}} / \mathrm{eV}$'),
   ('E', np.linspace(1e-1, 1e+1, N), r'$E / \mathrm{eV}$'),
   ]

figure = plt.figure()

defaults = dict(l=1.0, u=0.1, w=0.02, E=1.0)

for n, (key, x, label) in enumerate(variables, 1):
   parameters = defaults.copy()

   for i, parameters[key] in enumerate(x):
      print '%s = %g' % (key, parameters[key])

      TcEB[i] = parameters['T'] = ebbw.critical(**parameters)
      TcMM[i] = ebbw.Tc(**parameters)

   plt.subplot(2, 2, n)

   plt.plot(x, TcEB, label='Eliashberg')
   plt.plot(x, TcMM, label='McMillan')

   plt.legend(loc=0, frameon=False)

   plt.xlabel(label)
   plt.ylabel(r'$T_{\mathrm{c}} / K$')

plt.suptitle(r'(The default parameters are $\lambda = %(l)g$, $\mu = %(u)g$, '
   r'$\omega_{\mathrm{E}} = %(w)g\,\mathrm{eV}$ and $E = %(E)g\,\mathrm{eV}$)'
   % defaults, y=0)

plt.tight_layout()

figure.savefig('test.pdf', bbox_inches='tight')
