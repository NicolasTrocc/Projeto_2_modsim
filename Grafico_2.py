import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# Capacidades térmicas específicas
c_agua = 4186  # J/kg.K
c_leite_coco = 3500  # J/kg.K

# Raios (convertidos para metros)
raio_balde = 89.35 / 1000
raio_lata = 33.06 / 1000

# Alturas (em metros)
altura_lata = 6.69 / 100
altura_balde = 12.4 / 100

# Espessuras (em metros)
e_balde = 0.91 / 1000
e_lata = 0.68 / 1000

# Massas (em kg)
m_agua = 3.331
m_leite = 0.232

# Áreas reais (em m²)
A_chapa_agua = np.pi * raio_balde**2
A_agua_leite = 2 * np.pi * raio_lata * altura_lata + np.pi * raio_lata**2
A_sup_agua = (np.pi * raio_balde**2) - (np.pi * raio_lata**2)
A_sup_leite = np.pi * raio_lata**2
A_lateral_balde = np.pi * altura_balde * raio_balde * 2

# Coeficientes de troca térmica
k_aco = 16.2   # W/m.K
k_lata = 226   # W/m.K
h_ar = 10  # W/m².K (corrigido)
h_leite = 6  # Coeficiente de transferência de calor ajustado para o leite de coco

# Temperaturas
T_chapa = 130.0  # °C
T_amb = 22.1     # °C

# Resistências térmicas (em K/W)
R_cond_base = e_balde / (k_aco * A_chapa_agua)
R_contato_balde = 0.95  # [K/W] resistência de contato 
R_contato_lata = 1.25
R_total_base = R_cond_base + R_contato_balde  # resistência total entre chapa e água
R_cond_lata = e_lata / (k_lata * A_agua_leite)  # Resistência térmica da lata
R_cond_balde = e_balde / (k_aco * A_lateral_balde)  # Resistência térmica do balde
R_conv_balde = 1 / (h_ar * A_lateral_balde)  # Resistência térmica do balde para o ar
R_conv_agua = 1 / (h_ar * A_sup_agua)  # Resistência de condução da água
R_conv_leite = 1 / (h_leite * A_sup_leite)  # Resistência de condução do leite de coco

T0 = [22.9, 22.1]  # Temperatura inicial (água a 22.9°C, leite a 22.1°C)

# Tempo contínuo de 1 em 1 segundo
tempo = np.arange(0, 8100+1, 1)  # 2h15min


#modelo
temps_ambs = np.arange(100 , 230, 10)
def conclusivo2(T, t, T_chapa):
    T_agua, T_leite = T
    # Calor transferido
    Q1 = (T_chapa - T_agua) / (R_total_base)
    Q2 = (T_agua - T_amb) / (R_cond_balde + R_conv_balde) 
    Q3 = (T_agua - T_leite) / (R_cond_lata + R_contato_lata)
    Q4 = (T_agua - T_amb) / (R_conv_agua)  
    Q5 = (T_leite - T_amb) / (R_conv_leite)  

    dT_agua_dt = (Q1 - Q2 - Q3 - Q4) / (m_agua * c_agua) 
    dT_leite_dt = (Q3 - Q5) / (m_leite * c_leite_coco)  

    return [dT_agua_dt, dT_leite_dt]

for v in temps_ambs:
    Volta = odeint(conclusivo2, T0, tempo, args=(v,))
    resultados = Volta[:,1]
    plt.plot(tempo/60, resultados, label=(f'curva para temp da chapa = {v}°C'))
plt.xlabel("tempo (min)")
plt.legend(fontsize = 7)
plt.ylabel("Temperatura (°C)")
plt.title("Evolução Térmica")
plt.grid(True, which='major', linestyle='-', linewidth=0.5, alpha=0.7)
plt.show()