import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# Capacidades térmicas específicas
c_agua = 4186
c_leite_coco = 4894

# Raio
raio_balde = 89.35 / 1000
raio_lata = 33.06 / 1000

# Altura
altura_lata = 6.69 / 100
altura_balde = 12.4 / 100

# Espessuras
e_balde = 0.91 / 1000
e_lata = 0.68 / 1000

# Massas
m_agua = 3.331
m_leite = 0.232

# Áreas reais
A_chapa_agua = np.pi * raio_balde**2
A_agua_leite = 2 * np.pi * raio_lata * altura_lata + np.pi * raio_lata**2
A_sup_agua = (np.pi * raio_balde**2) - (np.pi * raio_lata**2)
A_sup_leite = np.pi * raio_lata**2
A_lateral_balde = np.pi * altura_balde * raio_balde * 2

# Coeficientes de troca térmica
k_aco = 16.2 / 420
k_lata = 226 / 250
h_ar = 10.77
leite_ar = 13.6

# Temperatura da chapa
T_chapa = 130
T_amb = 22.1

# Resistências térmicas
R_cond_lata = e_lata / (k_lata * A_agua_leite)
R_conv_balde = 1 / (h_ar * A_lateral_balde)
R_conv_leite = 1 / (h_ar * A_sup_leite)
R_conv_agua = 1 / (h_ar * A_sup_agua)

# Modelo
def conclusivo(T, t, espessura):
    T_agua = T[0]
    T_leite = T[1]
    
    # Cálculo das resistências térmicas
    R_cond_base = espessura / (k_aco * A_chapa_agua)
    R_cond_balde = espessura / (h_ar * A_lateral_balde)
    
    # Fluxos de calor
    Q1 = (T_chapa - T_agua) / R_cond_base
    Q2 = (T_agua - T_amb) / (R_cond_balde + R_conv_balde)
    Q3 = (T_agua - T_leite) / R_cond_lata
    Q4 = (T_agua - T_amb) / R_conv_agua
    Q5 = (T_leite - T_amb) / R_conv_leite
    
    # Equações diferenciais
    dT_agua_dt = (Q1 - Q2 - Q3 - Q4) / (m_agua * c_agua)
    dT_leite_dt = (Q3 - Q5) / (m_leite * c_leite_coco)
    
    return [dT_agua_dt, dT_leite_dt]

# Condições iniciais
T0 = [22.1, 22.1]

# Intervalo de espessuras (de 0.91 mm a 0.91 mm com incremento de 0.01 mm)
espessura = np.arange(0.91 / 1000, 0.91, 0.01/100)

# Tempo contínuo (de 0 a 8100 s)
tempo = np.linspace(0, 8100, 1000)

# Gráfico conclusivo
for e in espessura:
    # Resolver a equação diferencial
    solucao = odeint(conclusivo, T0, tempo, args=(e,))
    
    # Temperatura do leite ao longo do tempo
    temps_leite = solucao[:, 1]
    
    # Plotar a solução para cada espessura
    plt.plot(tempo, temps_leite)

# Adicionar rótulos ao gráfico
plt.xlabel("Tempo (min)")
plt.ylabel("Temperatura (°C)")
plt.title("Evolução Térmica")
plt.grid(True, which='major', linestyle='-', linewidth=0.5, alpha=0.7)

# Exibir o gráfico
plt.show()