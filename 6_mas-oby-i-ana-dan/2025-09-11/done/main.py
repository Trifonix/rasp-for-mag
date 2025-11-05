import numpy as np
import matplotlib.pyplot as plt

np.set_printoptions(precision = 4, suppress = True)
print('NumPy', np.__version__)

VARIANT = 12

x0 = 4.0
eta = 0.0022062004
iters = 50

def f(x):
  if VARIANT == 12:
    return (x**2 - 1)**2
  else:
    raise ValueError('Неверный VARIANT')

def df(x):
  if VARIANT == 12:
    return 4*x*(x**2 - 1)
  else:
    raise ValueError('Неверный VARIANT')

def gradient_descent(x0, eta=0.1, iters=50):
  x = float(x0)
  traj = [x]
  for k in range(iters):
    x = x - eta*df(x)
    traj.append(x)
  return np.array(traj)

traj = gradient_descent(x0=x0, eta=eta, iters=iters)

xs = np.linspace(min(min(traj)-2, -6), max(max(traj)+2, 6), 600)
plt.figure(figsize=(6,4))
plt.plot(xs, f(xs))
plt.plot(traj, f(traj), 'o-')
plt.title(f'Gradient Descent (variant {VARIANT})')
plt.xlabel('x'); plt.ylabel('f(x)'); plt.grid(True)
plt.show()

print('Последнее значение x:', traj[-1])

def run_and_plot(x0_list=(4.0,), eta_list=(0.01, 0.1, 0.5), iters=50):
    xs = np.linspace(-8, 8, 1000)
    plt.figure(figsize=(6,4))
    plt.plot(xs, f(xs), alpha=0.7)
    for x0 in x0_list:
        for lr in eta_list:
            traj = gradient_descent(x0, lr, iters)
            plt.plot(traj, f(traj), 'o-', label=f'x0={x0}, eta={lr}')
    plt.title('Влияние шага / старта')
    plt.xlabel('x'); plt.ylabel('f(x)'); plt.grid(True)
    plt.legend()
    plt.show()

# Пример запуска эксперимента
run_and_plot(x0_list=(x0, ), eta_list=(0.01, 0.1, 0.5), iters=iters)

def gd_backtracking(x0, eta0=1.0, iters=50, beta=0.5, sigma=1e-4):
    x = float(x0)
    traj = [x]
    for k in range(iters):
        g = df(x)
        eta = eta0
        # Armijo rule
        while f(x - eta*g) > f(x) - sigma*eta*(g**2):
            eta *= beta
            if eta < 1e-12:
                break
        x = x - eta*g
        traj.append(x)
    return np.array(traj)

# Пример запуска
traj_bt = gd_backtracking(x0=x0, eta0=1.0, iters=iters)
xs = np.linspace(min(min(traj_bt)-2, -6), max(max(traj_bt)+2, 6), 600)
plt.figure(figsize=(6,4))
plt.plot(xs, f(xs))
plt.plot(traj_bt, f(traj_bt), 'o-')
plt.title('GD с backtracking (Armijo)')
plt.grid(True)
plt.show()
