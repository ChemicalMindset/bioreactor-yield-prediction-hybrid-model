import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

np.random.seed(42)

# Define bioreactor kinetics parameters
mu_max = float(input("Enter the maximum specific growth rate (mu_max in h^-1): "))
Ks = float(input("Enter the half-saturation constant or affinity constant (Ks in g/L): "))
Ki = float(input("Enter the inhibition constant (Ki in g/L): "))
Y = float(input("Enter the conversion factor: "))

# Define initial batch parameters
S0 = float(input("Enter the initial substrate concentration (S0 in g/L): "))
X0 = float(input("Enter initial biomass (X0 un g/L): "))

# Define operation parameters
T_opt = float(input("Enter the optimal temperature (T_opt in °C): "))
pH_opt = float(input("Enter the optimal pH (pH_opt): "))

# --- 1. Dynamic Simulation ---
def dynamic_simulation():

    time = np.linspace(0, 48, 100)  # Time in hours

    # Process evolution matrices
    S_hist = [S0]
    X_hist = [X0]

    # Simulate process evolution
    for i in range(1, len(time)):
        dt = time[i] - time[i-1]

        # Current status
        S_current = S_hist[-1]
        X_current = X_hist[-1]

        # Specific growth rate
        mu = mu_max * (S_current / (Ks + S_current + (S_current**2 / Ki)))

        dX = mu * X_current * dt  # Biomass growth rate
        dS = - (1 / Y) * dX  # Substrate consumption rate

        # Store new values
        X_hist.append(X_current + dX)
        S_hist.append(S_current + dS)

    # --- GRAPHIC 1: Evolution and Phase Portrait ---
    plt.figure(figsize=(14, 5))

    # Subplot 1: Concentration vs Time
    plt.subplot(1, 2, 1)
    plt.plot(time, X_hist, label='Biomass (X)', color='green', linewidth=2)
    plt.plot(time, S_hist, label='Substrate (S)', color='blue', linestyle='--')
    plt.xlabel('Time (h)')
    plt.ylabel('Concentration (g/L)')
    plt.title('Biomass Evolution Rate (Monod + Euler)')
    plt.legend()
    plt.grid(True)

    # Subplot 2: Substract vs Biomass
    plt.subplot(1, 2, 2)
    plt.plot(S_hist, X_hist, color='purple', linewidth=2)
    plt.xlabel('Substrate consumed (S)')
    plt.ylabel('Biomass produced (X)')
    plt.title('Phase Portrait of the Reactor')
    plt.grid(True)

    plt.tight_layout()
    plt.show()

# --- 2. Static Data Generation ---
def static_data():
    n_samples = 1000

    S_array = np.random.uniform(0.1, 15.0, n_samples)  # Substrate concentration in g/L

    T_array = np.random.normal(T_opt, 8.0, n_samples)  # Temperature in °C
    T_array = np.clip(T_array, 15.0, 50.0)  # Limit temperature to realistic range

    pH_array = np.random.normal(pH_opt, 1.5, n_samples)  # pH
    pH_array = np.clip(pH_array, 4.5, 9.5)  # Limit pH to realistic range

    # Andrews Kinetic (Monod with Inhibition)
    mu_andrews = mu_max * (S_array / (Ks + S_array + (S_array**2 / Ki)))

    # Environmental factors (T y pH)
    factor_T = np.exp(-((T_array - T_opt)**2) / (2 * 10**2))
    factor_pH = np.exp(-((pH_array - pH_opt)**2) / (2 * 0.8**2))

    # Effective speed
    mu_efective = mu_andrews * factor_T * factor_pH

    # Yield (Target)
    biomass_yield = (mu_efective * 12) + np.random.normal(0, 0.3, n_samples)
    biomass_yield = np.maximum(biomass_yield, 0.1)

    # DataFrame
    df = pd.DataFrame({
        'Substrate_S': S_array,
        'Temperature_T': T_array,
        'pH': pH_array,
        'biomass_yield': biomass_yield
    })

    # --- GRAPHIC 2 ---

    # --- Pairplot: Monod Saturation ---
    pair_plot = sns.pairplot(df,
                             vars=['Substrate_S', 'Temperature_T', 'pH', 'biomass_yield'], 
                             diag_kind='kde', 
                             height=2.5)
    pair_plot.fig.suptitle('Pairplot: Non-linear Saturation Effect (Monod/Andrews)', y=1.02)
    plt.show()

    # --- Matriz de Correlación Lineal ---
    plt.figure(figsize=(8, 6))
    corr = df[['Substrate_S', 'Temperature_T', 'pH', 'biomass_yield']].corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.3f', linewidths=0.5)
    plt.title('Linear Correlation Matrix')
    plt.show()

    # Inhibition curve
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=df['Substrate_S'], y=df['biomass_yield'], alpha=0.5)
    plt.axvline(x=2.0, color='red', linestyle='--', label='peak (S=2 g/L)')
    plt.axvline(x=Ks, color='orange', linestyle=':', label=f'Ks = {Ks} g/L')
    plt.xlabel('Substrate concentration (g/L)')
    plt.ylabel('biomass_yield (g/L)')
    plt.title(f'Substrate effect with Inhibition (Ki = {Ki} g/L)')
    plt.legend()
    plt.grid(True)
    plt.show()

    print(df.head())

def main():

    while True:

        print("\n" + "="*20)
        print("Select sistem:")
        print("1. Dynamic Simulation (Baych evolution over time)")
        print("2. Static Data (Generates 1000 samples)")
        print("3. Exit")
        print("\n" + "="*20)

        option = input("Option: ")

        if option == "1":
            dynamic_simulation()

        elif option == "2":
            static_data()

        elif option == "3":
            print("Exit")
            break

        else:
            print("Error")

if __name__ == "__main__":
    main()