import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter
from devito import Grid, TimeFunction, Eq, Operator

# Define the grid
shape = (100, 100)
extent = (13.0, 12.0)
grid = Grid(shape=shape, extent=extent)

# Define time dimension
time = grid.time_dim

# Defining Functions for each SEIRD compartment
S = TimeFunction(name="S", grid=grid, time_order=1, space_order=2)
E = TimeFunction(name="E", grid=grid, time_order=1, space_order=2)
I = TimeFunction(name="I", grid=grid, time_order=1, space_order=2)
R = TimeFunction(name="R", grid=grid, time_order=1, space_order=2)
D = TimeFunction(name="D", grid=grid, time_order=1, space_order=2)

# Params
alpha = 0  # Birth rate
mu = 0  # Natural death rate
beta_e = 0.0003  # Transmission rate (exposed)
beta_i = 0.0003  # Transmission rate (infected)
sigma = 1/7  # Rate of exposed to infected
phi_e = 1/6  # Recovery rate (exposed)
phi_r = 1/24  # Recovery rate (infected)
phi_d = 1/160  # Death rate
nu = 1e-4  # Small diffusion parameter

# Define equations with diffusion
eqs_with_diffusion = [
    Eq(S.forward, S - (beta_e * E * S + beta_i * I * S) + alpha * S - mu * S + nu * S.laplace),
    Eq(E.forward, E + (beta_e * E * S + beta_i * I * S) - sigma * E - phi_e * E - mu * E + nu * E.laplace),
    Eq(I.forward, I + sigma * E - phi_r * I - phi_d * I - mu * I + nu * I.laplace),
    Eq(R.forward, R + phi_r * I + phi_e * E - mu * R + nu * R.laplace),
    Eq(D.forward, D + phi_d * I)
]

# Update initial conditions with Gaussian distributed population densities
population_density = np.ones(shape)
population_density = gaussian_filter(population_density, sigma=1)
S.data[:] = 0.89 * population_density
E.data[:] = 0.10 * population_density
I.data[:] = 0.01  # Decrease initial infected to avoid instability
R.data[:] = 0.0
D.data[:] = 0.0

# Initialize arrays to record daily changes
time_steps = 120
daily_new_infections = np.zeros(time_steps)
daily_new_deaths = np.zeros(time_steps)
daily_new_recoveries = np.zeros(time_steps)

# Operator to solve the equations with diffusion
op_diffusion = Operator(eqs_with_diffusion, time_order=1, dt=0.01)  # Use smaller time step

# Run the simulation with diffusion and record daily changes
previous_I = I.data.copy()
previous_D = D.data.copy()
previous_R = R.data.copy()

for t in range(time_steps):
    op_diffusion.apply(time_M=t+1)
    
    # Ensure no negative values
    I.data[I.data < 0] = 0
    D.data[D.data < 0] = 0
    R.data[R.data < 0] = 0
    
    daily_new_infections[t] = np.sum(I.data - previous_I)
    daily_new_deaths[t] = np.sum(D.data - previous_D)
    daily_new_recoveries[t] = np.sum(R.data - previous_R)
    previous_I = I.data.copy()
    previous_D = D.data.copy()
    previous_R = R.data.copy()

# Print final values with diffusion
print("S with diffusion:", S.data)
print("E with diffusion:", E.data)
print("I with diffusion:", I.data)
print("R with diffusion:", R.data)
print("D with diffusion:", D.data)

# Plotting the results in subplots
def plot_compartment(ax, data, title):
    cax = ax.imshow(data[0, :, :], extent=(0, extent[0], 0, extent[1]), origin='lower', cmap='viridis')
    ax.set_title(title)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    plt.colorbar(cax, ax=ax)

fig, axs = plt.subplots(1, 5, figsize=(20, 4))

plot_compartment(axs[0], S.data, 'Susceptible with diffusion')
plot_compartment(axs[1], E.data, 'Exposed with diffusion')
plot_compartment(axs[2], I.data, 'Infected with diffusion')
plot_compartment(axs[3], R.data, 'Recovered with diffusion')
plot_compartment(axs[4], D.data, 'Deceased with diffusion')

plt.tight_layout()
plt.show()

# Plot daily new infections, deaths, and recoveries over time
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(daily_new_infections, label='Daily New Infections')
ax.plot(daily_new_deaths, label='Daily New Deaths')
ax.plot(daily_new_recoveries, label='Daily New Recoveries')
ax.set_xlabel('Days')
ax.set_ylabel('Daily Count')
ax.set_title('Daily New Infections, Deaths, and Recoveries Over Time')
ax.legend()
plt.show()