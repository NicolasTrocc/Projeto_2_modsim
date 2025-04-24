
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# --- Constantes físicas ---
c_agua = 4180
c_aluminio = 900
c_coco = 3900
rho_agua = 1000
rho_coco = 1000
rho_aluminio = 2700

# --- Geometria do balde ---
d_b = 0.25
h_agua = 0.25
A_fundo = np.pi * (d_b/2)**2
V_agua = A_fundo * h_agua
m_agua = V_agua * rho_agua
A_superficie = A_fundo

# --- Geometria da latinha ---
d_l = 0.065
h_l = 0.10
e_lata = 0.0004
A_lata_ext = np.pi * d_l * h_l
A_lata_int = A_lata_ext
V_coco = np.pi * (d_l/2)**2 * h_l
m_coco = V_coco * rho_coco
A_lata_topo = np.pi * d_l * max(0, h_l - h_agua)
A_lata_total = A_lata_ext + 2 * np.pi * (d_l/2)**2
V_lata = A_lata_total * e_lata
m_lata = V_lata * rho_aluminio

# --- Capacidade térmica ---
C_agua = m_agua * c_agua
C_lata = m_lata * c_aluminio
C_coco = m_coco * c_coco

# --- Propriedades térmicas ---
k_inox = 16      # chapa -> fundo do balde (inox)
e_inox = 0.001   # espessura do fundo do balde
k_alum = 205     # alumínio

# --- Convecção com o ar (mantida) ---
h_sup = 10
h_ar = 15

# --- Temperaturas ---
T_chapa = 130.0
T_amb = 25.0
T0 = [25.0, 25.0, 25.0]  # [água, lata, leite]

# --- Modelo com condução q1, q2, q3 ---
def modelo(t, y):
    T_agua, T_lata, T_coco = y

    # Condução: chapa → água
    q1 = (k_inox * A_fundo / e_inox) * (T_chapa - T_agua)

    # Condução: água → lata
    q2 = (k_alum * A_lata_ext / e_lata) * (T_agua - T_lata)

    # Condução: lata → leite
    q3 = (k_alum * A_lata_int / e_lata) * (T_lata - T_coco)

    # Convecção: água → ar
    q4 = h_sup * A_superficie * (T_agua - T_amb)

    # Convecção: topo da lata → ar
    q5 = h_ar * A_lata_topo * (T_lata - T_amb)

    # EDOs
    dT_agua = (q1 - q2 - q4) / C_agua
    dT_lata = (q2 - q3 - q5) / C_lata
    dT_coco = q3 / C_coco

    return [dT_agua, dT_lata, dT_coco]

# --- Simulação ---
t_span = (0, 8100)
t_eval = np.linspace(*t_span, 800)
sol = solve_ivp(modelo, t_span, T0, t_eval=t_eval)

# --- Plot ---

plt.plot(sol.t / 60, sol.y[0], label='Água')
plt.plot(sol.t / 60, sol.y[1], label='Lata')
plt.plot(sol.t / 60, sol.y[2], label='Leite de coco')
plt.xlabel('Tempo (min)')
plt.ylabel('Temperatura (°C)')
plt.title('Modelo')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()