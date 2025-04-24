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
e_balde = 0.91/5
e_lata = 0.08/5

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
k_aco = 16.2
k_lata = 226
h_ar = 1.77
leite_ar = 13.6

# Temperatura da chapa
T_chapa = 130
T_amb = 22.1
#Resistencias térmicas
R_cond_base = e_balde/(k_aco*A_chapa_agua)
R_cond_lata = e_lata/(k_lata*A_agua_leite)
R_conv_balde = 1/(h_ar*A_lateral_balde)
R_cond_balde = e_balde/(k_aco*A_lateral_balde)
R_conv_leite = 1/(h_ar*A_sup_leite)
R_conv_agua = 1/(h_ar*A_sup_agua)

# Modelo
def modelo(T, t):
    T_agua = T[0]
    T_leite = T[1]
    Q1 =  (T_chapa-T_agua)/(R_cond_base)
    Q2 = (T_agua-T_amb)/(R_cond_balde+R_conv_balde)
    Q3 = (T_agua-T_leite)/(R_cond_lata)
    Q4 = (T_agua-T_amb)/(R_conv_agua)
    Q5 = (T_leite-T_amb)/(R_conv_leite)
    dT_agua_dt = (Q1-Q2-Q3-Q4) / (m_agua * c_agua)
    dT_leite_dt = (Q3-Q5) / (m_leite * c_leite_coco)
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