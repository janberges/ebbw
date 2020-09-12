#!/usr/bin/env python3

import numpy as np

kB = 8.61733e-5
epsilon = 1e-10

def Tc(l1, l2, u, w1, w2, E1, E2, A=1.20, B=1.04, C=0.62, **ignore):
    l = l1 + l2
    w = np.exp((l1 * np.log(w1) + l2 * np.log(w2)) / l)
    E = np.sqrt(E1 * E2)
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

def Eliashberg(T, l1, l2, u, w1, w2, E1, E2, W, rescale=True, N=1e4, **ignore):
   T *= kB

   w1 /= 2 * np.pi * T
   w2 /= 2 * np.pi * T

   w = np.exp((l1 * np.log(w1) + l2 * np.log(w2)) / (l1 + l2))
   N = int(min(N, np.ceil(W * w - 0.5)))

   l = (l1 / (1 + (np.arange(2 * N) / w1) ** 2)
      + l2 / (1 + (np.arange(2 * N) / w2) ** 2))

   if u and rescale:
      u /= 1 + u * 0.5 * (
         residue(E1 / ((2 * N + 1) * np.pi * T)) +
         residue(E2 / ((2 * N + 1) * np.pi * T)))

   I = np.empty((N, N))
   J = np.empty((N, N))

   l *= T
   u *= 2 * T
   for n in range(N):
      I[n:, n] = I[n, n:] = l[:N - n] - l[2 * n + 1:N + n + 1]
      J[n:, n] = J[n, n:] = l[:N - n] + l[2 * n + 1:N + n + 1] - u

   w = (2 * np.arange(N) + 1) * np.pi * T

   i = Eliashberg

   if not hasattr(i, 'w') or len(i.w) != N:
      i.w = w

   while True:
      w0 = i.w
      i.w = w + (np.arctan2(E1, i.w) + np.arctan2(E2, i.w)).dot(I)

      if np.all(abs(i.w - w0) < epsilon):
         break

   return eigenvalue((np.arctan2(E1, i.w) + np.arctan2(E2, i.w)) / i.w * J)

def critical(variable='T', epsilon=1e-3, exponent=None, **parameters):
   if exponent is None:
      exponent = dict(T=2.3, l1=-1.3, l2=-1.3, u=4.0, w1=-2.3, w2=-2.3,
         E1=-22.0, E2=-22.0)[variable]

   while True:
      x = parameters[variable] * Eliashberg(**parameters) ** exponent
      exponent *= 0.99

      if abs(x - parameters[variable]) < epsilon:
         return x

      parameters[variable] = x

if __name__ == '__main__':
   print(critical(T=10.0, l1=0.5, l2=0.5, u=0.1, w1=0.02, w2=0.02,
      E1=1.0, E2=1.0, W=15.0))
