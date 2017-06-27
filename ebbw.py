#!/usr/bin/env python

import numpy as np

kB = 8.61733e-5
epsilon = 1e-10

def Tc(l, u, w, E, A=0.94, B=1.11, C=0.74, **ignore):
    u /= 1 + u * np.log(E / w)
    return w / (kB * A) * np.exp(-B * (1 + l) / (l - C * l * u - u))

def eigenvalue(matrix):
   N = len(matrix)

   shift = min(
      max(sum(abs(row)) for row in matrix),
      max(sum(abs(col)) for col in matrix.T))

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
   x, y = (x, 0) if x < 1 else (1 / x, np.log(x))

   for n in xrange(1000):
      dy = 2 / np.pi * (-1) ** n * x ** (2 * n + 1) / (2 * n + 1) ** 2
      y += dy

      if abs(dy) < epsilon:
         return y

def Eliashberg(T, l, u, w, E, cutoff=15, rescale=True, **ignore):
   T *= kB

   w /= 2 * np.pi * T

   N = int(np.ceil(cutoff * w - 0.5))

   l /= 1 + (np.arange(2 * N) / w) ** 2

   if u and rescale:
      u /= 1 + u * residue(E / ((2 * N + 1) * np.pi * T))

   I = np.empty((N, N))
   J = np.empty((N, N))

   for n in range(N):
      for m in range(N):
         I[n, m] = 2 * T * (l[abs(n - m)] - l[n + m + 1])
         J[n, m] = 2 * T * (l[abs(n - m)] + l[n + m + 1] - 2 * u)

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

def critical(variable='T', epsilon=1e-3, **more):
   parameters = dict(T=10.0, l=1.0, u=0.1, w=0.02, E=1.0)
   parameters.update(more)

   exponent = dict(T=2.3, l=-1.3, u=4.0, w=-2.3, E=-22.0)[variable]

   while True:
      x = parameters[variable] * Eliashberg(**parameters) ** exponent
      exponent *= 0.99

      if abs(x - parameters[variable]) < epsilon:
         return x

      parameters[variable] = x

if __name__ == '__main__':
   print critical()
