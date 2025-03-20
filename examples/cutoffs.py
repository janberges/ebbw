#!/usr/bin/env python3

import ebbw
import numpy as np
import matplotlib.pyplot as plt

N = 101

Tc = np.empty(N)

variables = [
   ('E', 10, np.linspace(-1, 1, N), r'$E / \mathrm{eV}$'),
   ('W', 2, np.linspace(3, 5, N), r'$\omega_N / \omega_{\mathrm{E}}$'),
]

parameters = dict(T=10.0, l=1.0, u=None, w=0.02, E=None, W=None, rescale=None)

figure = plt.figure()

position = 221

for parameters['u'] in 0.1, 0.0:
   for v in 0, 1:
      vkey, vbase, vx, vlabel = variables[v]
      ckey, cbase, cx, clabel = variables[1 - v]

      vx = vbase ** vx
      cx = cbase ** cx[::N // 2]

      plt.subplot(position)
      position += 1

      for color, parameters[ckey] in zip('rgb' if v else 'cmy', cx):
         print('%s = %g' % (ckey, parameters[ckey]))

         for parameters['rescale'], options in [
               (True, dict(linestyle='-', label='%g' % parameters[ckey])),
               (False, dict(linestyle=':')),
            ]:
            print('rescale = %s' % parameters['rescale'])

            for i, parameters[vkey] in enumerate(vx):
               print('%s = %g' % (vkey, parameters[vkey]))

               Tc[i] = parameters['T'] = ebbw.critical(**parameters)

            plt.plot(vx, Tc, color=color, **options)

            if not parameters['u']:
               break

         plt.title(r'$\mu = %g$' % parameters['u'])

         if not parameters['u']:
            plt.legend()

         plt.autoscale(tight=True)
         plt.xscale('log', base=vbase)

         plt.xlabel(vlabel)
         plt.ylabel(r'$T_{\mathrm{c}} / \mathrm{K}$')

plt.suptitle(
   r'dotted lines w/o rescaling, '
   r'$\lambda = %(l)g$, '
   r'$\omega_{\mathrm{E}} = %(w)g\,\mathrm{eV}$'
   % parameters, y=0)

plt.tight_layout()
figure.savefig('cutoffs.png', bbox_inches='tight')
