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

# Modelo de transferência de calor
def modelo(T, t):
    T_agua, T_leite = T

    
    # Calor transferido
    Q1 = (T_chapa - T_agua) / (R_total_base)  # Calor da chapa para a água
    Q2 = (T_agua - T_amb) / (R_cond_balde + R_conv_balde)  # Calor da água para o ambiente
    Q3 = (T_agua - T_leite) / (R_cond_lata + R_contato_lata) # Calor da água para o leite via lata
    Q4 = (T_agua - T_amb) / (R_conv_agua)  # Calor da água para o ambiente
    Q5 = (T_leite - T_amb) / (R_conv_leite)  # Calor do leite para o ambiente

    # Equações de variação de temperatura
    dT_agua_dt = (Q1 - Q2 - Q3 - Q4) / (m_agua * c_agua)  # Variação da temperatura da água
    dT_leite_dt = (Q3 - Q5) / (m_leite * c_leite_coco)  # Variação da temperatura do leite (mais lento)

    return [dT_agua_dt, dT_leite_dt]

# Condições iniciais - Temperatura da água e do leite são diferentes desde o início
T0 = [22.9, 22.1]  # Temperatura inicial (água a 22.9°C, leite a 22.1°C)

# Tempo contínuo de 1 em 1 segundo
tempo = np.arange(0, 8100+1, 1)  # 2h15min

# Resolvendo a ODE
solucao = odeint(modelo, T0, tempo)

# Dados experimentais (medição a cada 5 min)
tempo_medido = np.arange(0, 8100+1, 300)
Temps_MedAgua = [
    22.9, 25.8, 28.1, 30.6, 33.1, 34.9, 37, 38.7, 40.4, 42.2,
    43.8, 45.3, 46.4, 47.9, 49, 50.2, 51.3, 52.3, 52.9, 54,
    54.8, 55.5, 56.3, 56.9, 57.4, 58.1, 58.5, 58.9
]
Temps_MedLeite = [
    22.7, 23, 23.8, 25, 26.6, 28.3, 30.1, 31.8, 33.5, 35.4,
    36.8, 38.4, 40.1, 41.5, 42.8, 44.1, 45.7, 46.6, 47.8, 48.8,
    49.8, 50.7, 51.5, 52.2, 52.9, 53.6, 54.2, 54.4
]

# Plotando o gráfico
plt.figure(figsize=(10, 6))

# Simulação (curvas contínuas)
plt.plot(tempo / 60, solucao[:, 0], color="blue", label="Água (Simulado)")
plt.plot(tempo / 60, solucao[:, 1], color="orange", label="Leite de coco (Simulado)")

# Dados medidos (pontos)
plt.plot(tempo_medido / 60, Temps_MedAgua, 'bo', label="Água (Medido)")
plt.plot(tempo_medido / 60, Temps_MedLeite, 'ro', label="Leite de coco (Medido)")

# Linha da chapa
plt.axhline(T_chapa, linestyle="--", color="red", label="Chapa (130°C)")

plt.xlabel("Tempo (minutos)")
plt.ylabel("Temperatura (°C)")
plt.title("Evolução Térmica - Simulação com Resistência de Contato")
plt.xticks(np.arange(0, 140, 5))
plt.yticks(np.arange(20, 140, 10))
plt.legend(loc='lower right')
plt.grid(True, which='major', linestyle='-', linewidth=0.5, alpha=0.7)
plt.tight_layout()
plt.show()

# Interpolando a solução nos tempos medidos (a cada 5 minutos)
solucao_interp = solucao[::300]  # pegar a cada 300 segundos

# Listas de erro ponto a ponto
lista_erros_percentuais_agua = []
lista_erros_percentuais_leite = []

# Percorrer todos os pontos medidos
for i in range(len(tempo_medido)):
    # Erro da água
    erro_abs_agua = abs(solucao_interp[i, 0] - Temps_MedAgua[i])
    erro_percent_agua = 100 * erro_abs_agua / Temps_MedAgua[i]
    lista_erros_percentuais_agua.append(erro_percent_agua)
    
    # Erro do leite
    erro_abs_leite = abs(solucao_interp[i, 1] - Temps_MedLeite[i])
    erro_percent_leite = 100 * erro_abs_leite / Temps_MedLeite[i]
    lista_erros_percentuais_leite.append(erro_percent_leite)

# Exibir as listas de erro
print("\nLista de erros percentuais - Água (%):")
print(lista_erros_percentuais_agua)

print("\nLista de erros percentuais - Leite de Coco (%):")
print(lista_erros_percentuais_leite)

# Agora calcular também o máximo, mínimo e médio baseado nas listas
print("\nErros relativos (%) - Água:")
print(f"Erro máximo: {max(lista_erros_percentuais_agua):.2f}%")
print(f"Erro mínimo: {min(lista_erros_percentuais_agua):.2f}%")
print(f"Erro médio: {np.mean(lista_erros_percentuais_agua):.2f}%")

print("\nErros relativos (%) - Leite de Coco:")
print(f"Erro máximo: {max(lista_erros_percentuais_leite):.2f}%")
print(f"Erro mínimo: {min(lista_erros_percentuais_leite):.2f}%")
print(f"Erro médio: {np.mean(lista_erros_percentuais_leite):.2f}%")
