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
R_contato_balde = 0.95  # [K/W] resistência de contato 
R_contato_lata = 1.25
R_cond_lata = e_lata / (k_lata * A_agua_leite)  # Resistência térmica da lata
R_conv_balde = 1 / (h_ar * A_lateral_balde)  # Resistência térmica do balde para o ar
R_conv_agua = 1 / (h_ar * A_sup_agua)  # Resistência de condução da água
R_conv_leite = 1 / (h_leite * A_sup_leite)  # Resistência de condução do leite de coco

T0 = [22.9, 22.1]  # Temperatura inicial (água a 22.9°C, leite a 22.1°C)

# Tempo contínuo de 1 em 1 segundo
tempo = np.arange(0, 8100+1, 1)  # 2h15min

# Modelo
def conclusivo1(T, t, espessura):
    T_agua = T[0]
    T_leite = T[1]
    R_cond_base = espessura/(k_aco*A_chapa_agua)
    R_total_base = R_cond_base + R_contato_balde
    R_cond_balde = espessura/(h_ar*A_lateral_balde)
    Q1 = (T_chapa - T_agua) / (R_total_base)  # Calor da chapa para a água
    Q2 = (T_agua - T_amb) / (R_cond_balde + R_conv_balde)  # Calor da água para o ambiente
    Q3 = (T_agua - T_leite) / (R_cond_lata + R_contato_lata) # Calor da água para o leite via lata
    Q4 = (T_agua - T_amb) / (R_conv_agua)  # Calor da água para o ambiente
    Q5 = (T_leite - T_amb) / (R_conv_leite)  # Calor do leite para o ambiente

    dT_agua_dt = (Q1-Q2-Q3-Q4) / (m_agua * c_agua)
    dT_leite_dt = (Q3-Q5) / (m_leite * c_leite_coco)
    return [dT_agua_dt, dT_leite_dt]

# Condições iniciais
T0 = [22.1, 22.1]
espessura = np.arange(0.91/1000, 0.91, 0.5/10)
# print(f'Aqui esta a lista {espessura}')
# Tempo contínuo
tempo = np.linspace(0, 8100, 1000)

#grafico conclusivo
for e in espessura:
    solucao = odeint(conclusivo1, T0, tempo, args=(e,))
    temps_leite = solucao[:,1] 
    plt.plot(tempo/60, temps_leite, label=(f'curva para espessura = {e:.2}mm'))
plt.xlabel("tempo (min)")
plt.ylabel("Temperatura (°C)")
plt.legend(fontsize = 5)
plt.title("Evolução Térmica")
plt.grid(True, which='major', linestyle='-', linewidth=0.5, alpha=0.7)
plt.show()
