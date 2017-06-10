#!/usr/bin/env python

import numpy as np

kB = 8.61733e-5
epsilon = 1e-10

def Tc(l, mu, wE, D, A=0.94, B=1.11, C=0.74, **ignore):
    mu /= 1 + mu * np.log(D / wE)
    return wE / (kB * A) * np.exp(-B * (1 + l) / (l - C * l * mu - mu))

def power_method(matrix):
   N = len(matrix)

   shift = min(
      max(sum(abs(row)) for row in matrix),
      max(sum(abs(col)) for col in matrix.T))

   matrix.flat[::N + 1] += shift

   I = power_method

   if not hasattr(I, 'vector') or len(I.vector) != N:
      I.vector = np.random.rand(N)

   x0 = np.nan

   while True:
      I.vector = matrix.dot(I.vector)
      x = np.sqrt(I.vector.dot(I.vector))
      I.vector /= x

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

def eigenvalue(T, l, mu, wE, D, cutoff=15, rescale=True, **ignore):
   T *= kB

   nE = wE / (2 * np.pi * T)

   N = int(np.ceil(cutoff * nE - 0.5))

   lamda = l / (1 + (np.arange(2 * N) / nE) ** 2)

   if rescale:
      mu /= 1 + mu * residue(D / ((2 * N + 1) * np.pi * T))

   I = np.empty((N, N))
   J = np.empty((N, N))

   for n in range(N):
      for m in range(N):
         I[n, m] = 2 * T * (lamda[abs(n - m)] - lamda[n + m + 1])
         J[n, m] = 2 * T * (lamda[abs(n - m)] + lamda[n + m + 1] - 2 * mu)

   w = (2 * np.arange(N) + 1) * np.pi * T
   W0 = np.copy(w)

   while True:
      W = w + np.arctan2(D, W0).dot(I)

      if np.all(abs(W - W0) < epsilon):
         break

      W0 = W

   return power_method(np.arctan2(D, W) / W * J)

def critical(variable='T', epsilon=1e-3, **more):
   parameters = dict(T=10.0, l=1.0, mu=0.1, wE=0.02, D=1.0)
   parameters.update(more)

   exponent = dict(T=2.3, l=-1.3, mu=4.0, wE=-2.3, D=-22.0)[variable]

   while True:
      x = parameters[variable] * eigenvalue(**parameters) ** exponent
      exponent *= 0.99

      if abs(x - parameters[variable]) < epsilon:
         return x

      parameters[variable] = x

if __name__ == '__main__':
   print critical(epsilon=1e-3)
