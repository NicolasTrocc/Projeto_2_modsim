
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

P = 500
T_amb = 298.15
m1, m2, m3, m4 = 0.5, 1.0, 0.3, 0.5
c1, c2, c3, c4 = 900, 4186, 900, 3800
A12, A23, A34 = 0.04, 0.03, 0.02
A1a, A2a, A4a = 0.06, 0.05, 0.03
k12, k23, k34 = 100, 80, 60
h1a, h2a, h4a = 10, 12, 12

def banho_maria(T, t):
    T1, T2, T3, T4 = T
    Q12 = k12 * A12 * (T1 - T2)
    Q23 = k23 * A23 * (T2 - T3)
    Q34 = k34 * A34 * (T3 - T4)
    Q1a = h1a * A1a * (T1 - T_amb)
    Q2a = h2a * A2a * (T2 - T_amb)
    Q4a = h4a * A4a * (T4 - T_amb)
    dT1dt = (P - Q12 - Q1a) / (m1 * c1)
    dT2dt = (Q12 - Q23 - Q2a) / (m2 * c2)
    dT3dt = (Q23 - Q34) / (m3 * c3)
    dT4dt = (Q34 - Q4a) / (m4 * c4)
    if T2>= 100 + 273.15:
        dT2dt = 0 
    return [dT1dt, dT2dt, dT3dt, dT4dt]

T0 = [T_amb, T_amb, T_amb, T_amb]
t = np.arange(0, 3600 + 1, 1)
sol = odeint(banho_maria, T0, t)
T1_C = sol[:, 0] - 273.15
T2_C = sol[:, 1] - 273.15
T3_C = sol[:, 2] - 273.15
T4_C = sol[:, 3] - 273.15

plt.figure(figsize=(10,6))
plt.plot(t/60, T1_C, label="Recipiente externo")
plt.plot(t/60, T2_C, label="Água")
plt.plot(t/60, T3_C, label="Recipiente interno")
plt.plot(t/60, T4_C, label="Líquido interno")
plt.axhline(100, color='gray', linestyle='--', label='Limite água')
plt.xlabel("Tempo (min)")
plt.ylabel("Temperatura (°C)")
plt.title("Simulação do Banho-Maria")
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()