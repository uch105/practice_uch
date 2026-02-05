import numpy as np
import matplotlib.pyplot as plt

# Define critical points (Carbon wt%, Temperature in °C)
points = {
    'A': (0.0, 1538),     # Pure Iron melting point
    'B': (0.53, 1493),    # Peritectic liquid point
    'C': (4.3, 1147),     # Eutectic point
    'D': (6.67, 1227),    # Cementite melting point
    'E': (2.11, 1147),    # Maximum carbon solubility in Austenite
    'F': (6.67, 1147),    # Cementite at eutectic temperature
    'G': (0.0, 912),      # γ-Fe to α-Fe in pure iron
    'S': (0.76, 727),     # Eutectoid point
    'P': (0.022, 727),    # Maximum carbon solubility in Ferrite
    'Q': (6.67, 727),     # Cementite at eutectoid temperature
    'N': (0.0, 1394),     # δ-Fe to γ-Fe in pure iron
    'H': (0.09, 1493),    # Peritectic δ point
    'J': (0.17, 1493),    # Peritectic γ point
}

# Liquidus lines (L to L+δ and L to L+γ)
liquidus_L_delta_x = np.array([points['A'][0], points['B'][0]])
liquidus_L_delta_y = np.array([points['A'][1], points['B'][1]])
liquidus_L_gamma_x = np.array([points['B'][0], points['C'][0], points['D'][0]])
liquidus_L_gamma_y = np.array([points['B'][1], points['C'][1], points['D'][1]])

# Solidus lines (δ and γ)
solidus_delta_x = np.array([points['A'][0], points['H'][0]])
solidus_delta_y = np.array([points['A'][1], points['H'][1]])
solidus_gamma_x = np.array([points['J'][0], points['E'][0]])
solidus_gamma_y = np.array([points['J'][1], points['E'][1]])

# Peritectic line (L + δ → γ)
peritectic_x = np.array([points['H'][0], points['B'][0]])
peritectic_y = np.array([points['H'][1], points['B'][1]])

# Eutectic line (L → γ + Fe₃C)
eutectic_x = np.array([points['C'][0], points['F'][0]])
eutectic_y = np.array([points['C'][1], points['F'][1]])

# Eutectoid line (γ → α + Fe₃C)
eutectoid_x = np.array([points['P'][0], points['Q'][0]])
eutectoid_y = np.array([points['P'][1], points['Q'][1]])

# A₃ line (γ to γ + α)
A3_x = np.array([points['G'][0], points['S'][0]])
A3_y = np.array([points['G'][1], points['S'][1]])

# A₄ line (γ to γ + Fe₃C)
A4_x = np.array([points['S'][0], points['E'][0]])
A4_y = np.array([points['S'][1], points['E'][1]])

# δ to δ + γ boundary
delta_gamma_x = np.array([points['N'][0], points['H'][0]])
delta_gamma_y = np.array([points['N'][1], points['H'][1]])

# Cementite line (Fe₃C)
cementite_x = np.array([points['D'][0], points['F'][0], points['Q'][0]])
cementite_y = np.array([points['D'][1], points['F'][1], points['Q'][1]])

# Ferrite (α) boundary
ferrite_x = np.array([points['P'][0], points['G'][0]])
ferrite_y = np.array([points['P'][1], points['G'][1]])

# Plot setup
plt.figure(figsize=(12, 8))
plt.title('Iron-Iron Carbide (Fe-Fe$_3$C) Phase Diagram')
plt.xlabel('Carbon Content (wt%)')
plt.ylabel('Temperature (°C)')
plt.grid(True, linestyle='--', alpha=0.3)
plt.xlim(0, 7.0)
plt.ylim(600, 1600)

# Plot phase boundaries
plt.plot(liquidus_L_delta_x, liquidus_L_delta_y, 'b-', linewidth=2, label='Liquidus (L/δ)')
plt.plot(liquidus_L_gamma_x, liquidus_L_gamma_y, 'b-', linewidth=2, label='Liquidus (L/γ)')
plt.plot(solidus_delta_x, solidus_delta_y, 'r-', linewidth=2, label='Solidus (δ)')
plt.plot(solidus_gamma_x, solidus_gamma_y, 'r-', linewidth=2, label='Solidus (γ)')
plt.plot(peritectic_x, peritectic_y, 'm-', linewidth=2, label='Peritectic (L+δ→γ)')
plt.plot(eutectic_x, eutectic_y, 'g-', linewidth=2, label='Eutectic (L→γ+Fe$_3$C)')
plt.plot(eutectoid_x, eutectoid_y, 'k-', linewidth=2, label='Eutectoid (γ→α+Fe$_3$C)')
plt.plot(A3_x, A3_y, 'c-', linewidth=2, label='A$_3$ (γ/γ+α)')
plt.plot(A4_x, A4_y, 'y-', linewidth=2, label='A$_{cm}$ (γ/γ+Fe$_3$C)')
plt.plot(delta_gamma_x, delta_gamma_y, 'orange', linewidth=2, label='δ/(δ+γ) Boundary')
plt.plot(cementite_x, cementite_y, 'k:', linewidth=2, label='Cementite (Fe$_3$C)')
plt.plot(ferrite_x, ferrite_y, 'brown', linewidth=2, label='Ferrite (α) Boundary')

# Label critical points
for label, (x, y) in points.items():
    plt.plot(x, y, 'ro', markersize=6)
    plt.annotate(f'{label} ({x},{y})', (x, y), textcoords="offset points", xytext=(5,5), ha='left')

# Add phase regions
plt.text(0.5, 1450, 'Liquid (L)', fontsize=10, bbox=dict(facecolor='white', alpha=0.5))
plt.text(0.5, 1000, 'Ferrite (α)', fontsize=10, bbox=dict(facecolor='white', alpha=0.5))
plt.text(3.0, 1200, 'Austenite (γ)', fontsize=10, bbox=dict(facecolor='white', alpha=0.5))
plt.text(5.5, 800, 'Cementite (Fe$_3$C)', fontsize=10, bbox=dict(facecolor='white', alpha=0.5))

plt.legend(loc='upper right', fontsize=9)
plt.tight_layout()
plt.show()
