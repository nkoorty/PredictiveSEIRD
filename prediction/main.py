from devito import Grid, TimeFunction, Eq, Operator

# Define the grid
shape = (10, 10)  # Grid shape
extent = (1.0, 1.0)  # Physical dimensions
grid = Grid(shape=shape, extent=extent)

# Define time dimension
time = grid.time_dim
# testing

# Define Functions for each SEIRD compartment
S = TimeFunction(name="S", grid=grid, time_order=1, space_order=2)
E = TimeFunction(name="E", grid=grid, time_order=1, space_order=2)
I = TimeFunction(name="I", grid=grid, time_order=1, space_order=2)  # noqa
R = TimeFunction(name="R", grid=grid, time_order=1, space_order=2)
D = TimeFunction(name="D", grid=grid, time_order=1, space_order=2)


alpha = 0  # Birth rate
mu = 0  # Natural death rate
beta_e = 0.0003  # Transmission rate (exposed)
beta_i = 0.0003  # Transmission rate (infected)
sigma = 1/7  # Rate of exposed to infected
phi_e = 1/6  # Recovery rate (exposed)
phi_r = 1/24  # Recovery rate (infected)
phi_d = 1/160  # Death rate

# Define equations
eqs = [
    Eq(S.forward, S - (beta_e * E * S + beta_i * I * S) + alpha * S - mu * S),
    Eq(E.forward, E + (beta_e * E * S + beta_i * I * S) - sigma * E - phi_e *
       E - mu * E),
    Eq(I.forward, I + sigma * E - phi_r * I - phi_d * I - mu * I),
    Eq(R.forward, R + phi_r * I + phi_e * E - mu * R),
    Eq(D.forward, D + phi_d * I)
]

# Initial conditions
S.data[:] = 0.99  # 99% susceptible
E.data[:] = 0.01  # 1% exposed
I.data[:] = 0.0
R.data[:] = 0.0
D.data[:] = 0.0

# Operator to solve the equations
op = Operator(eqs, time_order=1)

# Run the simulation
op(time_M=1)  # Run for 100 time steps

# Print final values
print("S:", S.data)
print("E:", E.data)
print("I:", I.data)
print("R:", R.data)
print("D:", D.data)
