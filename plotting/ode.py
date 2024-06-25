import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt


def seird_odes(t, y, beta_e, beta_i, sigma, phi_e, phi_r, phi_d, mu):
    S, E, I, R, D = y
    N = S + E + I + R
    dSdt = -beta_e * S * E / N - beta_i * S * I / N + mu * (N - S)
    dEdt = beta_e * S * E / N + beta_i * S * I / N - sigma * E - phi_e * E - mu * E # noqa
    dIdt = sigma * E - phi_d * I - phi_r * I - mu * I
    dRdt = phi_r * I + phi_e * E - mu * R
    dDdt = phi_d * I
    return [dSdt, dEdt, dIdt, dRdt, dDdt]


# Initial conditions and parameters
y0 = [989, 10, 1, 0, 0]
t_span = [0, 200]
params = (0.0003, 0.0003, 1/7, 1/6, 1/24, 1/160, 0)
sol = solve_ivp(seird_odes, t_span, y0, args=params, method='RK45', t_eval=np.linspace(0, 200, 200)) # noqa

# Plot results
# plt.plot(sol.t, sol.y[0], label='Susceptible')
plt.plot(sol.t, sol.y[1], label='Exposed')
plt.plot(sol.t, sol.y[2], label='Infected')
plt.plot(sol.t, sol.y[3], label='Recovered')
plt.plot(sol.t, sol.y[4], label='Deceased')
plt.legend()
plt.xlabel('Days')
plt.ylabel('Population')
plt.show()
