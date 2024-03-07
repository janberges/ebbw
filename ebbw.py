#!/usr/bin/env python3

# Copyright (C) 2017-2024 Jan Berges
# This program is free software under the terms of the GNU GPLv3 or later.

__version__ = '2021.1'

import numpy as np

kB = 8.61733e-5
epsilon = 1e-10

def Tc(l, u, w, E, A=1.20, B=1.04, C=0.62, **ignore):
    u /= 1 + u * np.log(E / w)
    return w / (kB * A) * np.exp(-B * (1 + l) / (l - C * l * u - u))

def eigenvalue(matrix):
   N = len(matrix)

   absolute = abs(matrix)
   shift = min(absolute.sum(axis=0).max(), absolute.sum(axis=1).max())

   matrix.flat[::N + 1] += shift

   i = eigenvalue

   if not hasattr(i, 'vector') or len(i.vector) != N:
      i.vector = np.random.rand(N)

   x0 = np.nan

   while True:
      i.vector = matrix.dot(i.vector)
      x = np.sqrt(i.vector.dot(i.vector))
      i.vector /= x

      if abs(x - x0) < epsilon:
         return x - shift

      x0 = x

def residue(x):
   base, series = (1 / x, np.log(x)) if x > 1 else (x, 0)

   n = 1
   pre = 2 / np.pi

   while True:
      term = base ** n / n ** 2
      series += pre * term

      if term < epsilon:
         return series

      n += 2
      pre *= -1

def Eliashberg(T, l, u, w, E, W, rescale=True, N=1e4, **ignore):
   T *= kB

   w /= 2 * np.pi * T

   N = int(min(N, np.ceil(W * w - 0.5)))

   l /= 1 + (np.arange(2 * N) / w) ** 2

   if u and rescale:
      u /= 1 + u * residue(E / ((2 * N + 1) * np.pi * T))

   I = np.empty((N, N))
   J = np.empty((N, N))

   l *= 2 * T
   u *= 4 * T
   for n in range(N):
      I[n:, n] = I[n, n:] = l[:N - n] - l[2 * n + 1:N + n + 1]
      J[n:, n] = J[n, n:] = l[:N - n] + l[2 * n + 1:N + n + 1] - u

   w = (2 * np.arange(N) + 1) * np.pi * T

   i = Eliashberg

   if not hasattr(i, 'w') or len(i.w) != N:
      i.w = w

   while True:
      w0 = i.w
      i.w = w + np.arctan2(E, i.w).dot(I)

      if np.all(abs(i.w - w0) < epsilon):
         break

   return eigenvalue(np.arctan2(E, i.w) / i.w * J)

def critical(variable='T', epsilon=1e-3, exponent=None, **parameters):
   if exponent is None:
      exponent = dict(T=2.3, l=-1.3, u=4.0, w=-2.3, E=-22.0)[variable]

   while True:
      x = parameters[variable] * Eliashberg(**parameters) ** exponent
      exponent *= 0.99

      if abs(x - parameters[variable]) < epsilon:
         return x

      parameters[variable] = x

if __name__ == '__main__':
   print(critical(T=10.0, l=1.0, u=0.1, w=0.02, E=1.0, W=15.0))
