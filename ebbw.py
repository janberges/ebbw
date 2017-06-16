#!/usr/bin/env python

import numpy as np

kB = 8.61733e-5
epsilon = 1e-10

def Tc(l, u, w, D, A=0.94, B=1.11, C=0.74, **ignore):
    u /= 1 + u * np.log(D / w)
    return w / (kB * A) * np.exp(-B * (1 + l) / (l - C * l * u - u))

def power_method(matrix):
   N = len(matrix)

   shift = min(
      max(sum(abs(row)) for row in matrix),
      max(sum(abs(col)) for col in matrix.T))

   matrix.flat[::N + 1] += shift

   i = power_method

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

def residue(x, N=10):
   if x < 1:
      return 2 / np.pi * sum((-1) ** n * x ** (2 * n + 1) / (2 * n + 1) ** 2
         for n in range(N))
   else:
      return 2 / np.pi * sum((-1) ** n / x ** (2 * n + 1) / (2 * n + 1) ** 2
         for n in range(N)) + np.log(x)

def eigenvalue(T, l, u, w, D, cutoff=15, rescale=True, **ignore):
   T *= kB

   w /= 2 * np.pi * T

   N = int(np.ceil(cutoff * w - 0.5))

   l /= 1 + (np.arange(2 * N) / w) ** 2

   if rescale:
      u /= 1 + u * residue(D / ((2 * N + 1) * np.pi * T))

   I = np.empty((N, N))
   J = np.empty((N, N))

   for n in range(N):
      for m in range(N):
         I[n, m] = 2 * T * (l[abs(n - m)] - l[n + m + 1])
         J[n, m] = 2 * T * (l[abs(n - m)] + l[n + m + 1] - 2 * u)

   W0 = w = (2 * np.arange(N) + 1) * np.pi * T

   while True:
      W = w + np.arctan2(D, W0).dot(I)

      if np.all(abs(W - W0) < epsilon):
         break

      W0 = W

   return power_method(np.arctan2(D, W) / W * J)

def critical(variable='T', epsilon=1e-3, **more):
   parameters = dict(T=10.0, l=1.0, u=0.1, w=0.02, D=1.0)
   parameters.update(more)

   exponent = dict(T=2.3, l=-1.3, u=4.0, w=-2.3, D=-22.0)[variable]

   while True:
      x = parameters[variable] * eigenvalue(**parameters) ** exponent
      exponent *= 0.99

      if abs(x - parameters[variable]) < epsilon:
         return x

      parameters[variable] = x

if __name__ == '__main__':
   print critical()
