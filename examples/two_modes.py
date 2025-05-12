#!/usr/bin/env python3

import ebbw2
import matplotlib.pyplot as plt
import numpy as np

N = 101

l1 = [1.0, 0.0]
l2 = np.linspace(0.4, 1.4, N)

TcEB = np.empty((3, N))
TcMM = np.empty((3, N))

parameters = dict(T=20.0, u=0.0, l1=1.0, l2=0.0, w1=0.02, w2=0.08,
    E1=3.6, E2=4.4, W=50.0)

TcEB[2] = ebbw2.critical(**parameters)
TcMM[2] = ebbw2.Tc(**parameters)

for i, parameters['l1'] in enumerate(l1):
    print('l1 = %g' % parameters['l1'])

    for j, parameters['l2'] in enumerate(l2):
        print('l2 = %g' % parameters['l2'])

        TcEB[i, j] = parameters['T'] = ebbw2.critical(**parameters)
        TcMM[i, j] = ebbw2.Tc(**parameters)

        print('Tc = %g K' % parameters['T'])

figure = plt.figure()

plt.plot(l2, TcMM[2], 'g--', label='McMillan 1')
plt.plot(l2, TcMM[1], 'y--', label='McMillan 2')
plt.plot(l2, TcMM[0], 'k--', label='McMillan 1+2')
plt.plot(l2, TcEB[2], 'g', label='Eliashberg 1')
plt.plot(l2, TcEB[1], 'y', label='Eliashberg 2')
plt.plot(l2, TcEB[0], 'k', label='Eliashberg 1+2')

plt.xlabel(r'$\lambda_2$')
plt.ylabel(r'$T_{\mathrm{c}}$ (K)')

plt.legend()

plt.autoscale(tight=True)
figure.savefig('two_modes.png', bbox_inches='tight')
