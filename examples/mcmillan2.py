#!/usr/bin/env python3

import ebbw2
import numpy as np
import matplotlib.pyplot as plt

N = 101

TcEB = np.empty(N)
TcMM = np.empty(N)

variables = [
    ('l1', np.linspace(0.50, 2.50, N), r'$\lambda_1$'),
    ('u', np.linspace(0.00, 0.30, N), r'$\mu$'),
    ('w1', np.linspace(0.01, 0.03, N), r'$\omega_1 / \mathrm{eV}$'),
    ('E1', np.linspace(0.10, 6.00, N), r'$E_1 / \mathrm{eV}$'),
]

defaults = dict(T=10.0, l1=0.5, l2=0.5, u=0.1, w1=0.02, w2=0.02,
    E1=6.0, E2=6.0, W=15.0)

A = 0.94
B = 1.11
C = 0.74

A *= ebbw2.Tc(**defaults, A=A, B=B, C=C)
A /= ebbw2.critical(**defaults)

figure = plt.figure()

for position, (key, x, label) in enumerate(variables, 221):
    parameters = defaults.copy()

    for i, parameters[key] in enumerate(x):
        print('%s = %g' % (key, parameters[key]))

        TcEB[i] = parameters['T'] = ebbw2.critical(**parameters)
        TcMM[i] = ebbw2.Tc(**parameters, A=A, B=B, C=C)

    plt.subplot(position)
    plt.autoscale(tight=True)

    plt.plot(x, TcEB, label='Eliashberg')
    plt.plot(x, TcMM, label='McMillan')

    plt.xlabel(label)
    plt.ylabel(r'$T_{\mathrm{c}} / \mathrm{K}$')

plt.legend()

plt.suptitle(r'defaults: '
    r'$\lambda_{1, 2} = %(l1)g$, '
    r'$\mu = %(u)g$, '
    r'$\omega_{1, 2} = %(w1)g\,\mathrm{eV}$, '
    r'$E_{1, 2} = %(E1)g\,\mathrm{eV}$, '
    r'$\omega_N = %(W)g\,\omega_\log$'
    % defaults, y=0)

plt.tight_layout()

figure.savefig('mcmillan2.png', bbox_inches='tight')
