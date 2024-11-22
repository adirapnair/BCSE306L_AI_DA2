import numpy as np

# Define prior probabilities
P_A = {"yes": 0.8, "no": 0.2}
P_C = {"yes": 0.5, "no": 0.5}

# Define conditional probabilities
P_G_given_A_C = {
    ("Good", "yes", "yes"): 0.9,
    ("Good", "yes", "no"): 0.7,
    ("Good", "no", "yes"): 0.6,
    ("Good", "no", "no"): 0.3,
    ("OK", "yes", "yes"): 0.1,
    ("OK", "yes", "no"): 0.3,
    ("OK", "no", "yes"): 0.4,
    ("OK", "no", "no"): 0.7
}

# Monte Carlo simulation function
def monte_carlo_simulation(target_state="Good", evidence={"A": "yes", "C": "yes"}, num_samples=10000):
    count_target_given_evidence = 0
    count_evidence = 0

    for _ in range(num_samples):
        # Sample A and C based on the given evidence
        A = evidence.get("A", np.random.choice(["yes", "no"], p=[P_A["yes"], P_A["no"]]))
        C = evidence.get("C", np.random.choice(["yes", "no"], p=[P_C["yes"], P_C["no"]]))

        # Only consider samples that match the evidence
        if A == evidence["A"] and C == evidence["C"]:
            count_evidence += 1

            # Sample G based on P(G | A, C)
            P_G = [P_G_given_A_C[("Good", A, C)], P_G_given_A_C[("OK", A, C)]]
            G = np.random.choice(["Good", "OK"], p=P_G)

            # Check if the target state is reached
            if G == target_state:
                count_target_given_evidence += 1

    # Calculate conditional probability
    if count_evidence == 0:
        return 0  # Avoid division by zero
    return count_target_given_evidence / count_evidence

# Run simulation
estimated_probability = monte_carlo_simulation()
print(f"Estimated P(G=Good | A=yes, C=yes): {estimated_probability}")