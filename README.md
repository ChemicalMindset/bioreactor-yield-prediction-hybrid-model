# bioreactor-yield-prediction-hybrid-model
Bioreactor modeling combining enzyme kinetics (Andrews with Ki inhibition) and real-time biomass yield prediction.

---

This project simulates a batch bioreactor for biomass production and generates synthetic dada rooted in real ennzymatic kinetics (Andrews/Monod model with substrate inhibition) and adds realistic instrumental noise.

---

1. Implement specific growth rate models mu, temperature/pH inhibition factors, and numerical integration (Euler method).
2. Generate a static dataset

---

**Dynamic Simulation:** Solves the ODE system (Euler method) for a single batch. Plots Concentration vs Time and the Phase Portrait (X vs S).
**Static Data Generation:** Generates 1,000 random batches with varying S0, T, and pH. 

---

You will be prompted to enter the kinetic parameters (e.g., mu_max, Ks, Ki, Y, S0, etc.). Once entered, the menu will allow you to:

Run Dynamic Simulation – Watch a single batch evolve over 48 hours.

Generate Static Data – Create the 1,000-sample dataset and view the EDA plots (Pairplot, Correlation Heatmap, Inhibition Scatter).

Exit – Close the program.

---

Pairplot: The relationship between Substrate_S and biomass_yield is a plateau/camp, not a straight line.

Correlation Matrix: Temperature_T and pH show a correlation coefficient near 0 with the target.

Inhibition Curve: Maximum yield occurs at S ≈ 2 g/L. Beyond this, substrate toxicity (Ki) reduces biomass production.

---

Future Commits:

Add a third menu option to train and compare Linear Regression vs. Random Forest using Scikit-learn.

Deploy a real-time dashboard using Streamlit to interact with S0, T, and pH sliders.

---

Clone the repository:

git clone https://github.com/ChemicalMindset/bioreactor-hybrid-modelling.git
cd bioreactor-hybrid-modelling

python Fermentation_Optimization.py
