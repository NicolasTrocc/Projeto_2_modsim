import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# Capacidades térmicas específicas
c_agua = 4186
c_leite_coco = 4235

#raios
raio_balde = 89.35/1000
raio_lata = 33.06/1000

#altura
altura_lata = 6.69/100
altura_balde = 12.4/100

#espessuras
e_balde = 0.91/1000
e_lata = 0.08/1000

# Massas
m_agua = 3.331
m_leite = 0.232

# Áreas reais
A_chapa_agua = np.pi * raio_balde**2
A_agua_leite = 2 * np.pi * raio_lata *  + np.pi * raio_lata**2
A_sup_agua = (np.pi*raio_balde**2)-(np.pi * raio_lata**2)
A_sup_leite = np.pi * raio_lata**2
A_lateral_balde = np.pi*altura_balde*raio_balde*2

# Coeficientes de troca térmica
h_chapa_agua = 500
h_agua_leite = 100
h_agua_ar = 14
leite_ar = 0

# Temperatura da chapa
T_chapa = 130

# Modelo
def modelo(T, t):
    T_agua, T_leite = T
    Q1 = h_chapa_agua * A_chapa_agua * (T_chapa - T_agua)
    Q2 = (16.2*A_lateral_balde)+(h_chapa_agua*A_chapa_agua)/e_balde
    Q3 = h_agua_leite * A_agua_leite * (T_agua - T_leite)
    Q4 = ()
    dT_agua_dt = (Q1 - Q2) / (m_agua * c_agua)
    dT_leite_dt = Q2 / (m_leite * c_leite_coco)
    return [dT_agua_dt, dT_leite_dt]

# Condições iniciais
T0 = [22.1, 22.1]

# Tempo contínuo
tempo = np.linspace(0, 8100, 1000)
solucao = odeint(modelo, T0, tempo)

# Tempo de medição de 5 em 5 min
tempo_medicao = np.arange(0, 8100+1, 300)  # de 0 a 8100 s, passo 300 s
solucao_medicao = odeint(modelo, T0, tempo_medicao)

# Plot
plt.figure(figsize=(10, 6))

plt.plot(tempo_medicao / 60, solucao_medicao[:, 0], color="blue", label="Água")
plt.plot(tempo_medicao / 60, solucao_medicao[:, 1], color="orange", label="Leite de coco")

plt.axhline(T_chapa, linestyle="--", color="red", label="Chapa (130°C)")

plt.xlabel("Tempo (min)")
plt.ylabel("Temperatura (°C)")
plt.title("Evolução Térmica")
plt.xticks(np.arange(0, 140, 5))  # de 0 a 60 min de 5 em 5
plt.yticks(np.arange(0, 140, 10))  # de 0 a 120°C de 10 em 10
plt.legend(loc = 'lower right')
plt.grid(True, which='major', linestyle='-', linewidth=0.5, alpha=0.7)
plt.tight_layout()
plt.show()