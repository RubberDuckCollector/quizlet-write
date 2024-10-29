import matplotlib.pyplot as plt  # type: ignore
import numpy as np

# Example: Creating data for n lines
n = 10  # Number of lines
x = np.linspace(0, 10, 100)  # Shared x-axis values for simplicity

# Generate different y-values for each line
y_data = [np.sin(x + i) for i in range(n)]  # Example: Sine waves with phase shifts

# Plot each line
plt.figure(figsize=(10, 6))  # Adjust figure size as needed
for i in range(n):
    plt.plot(x, y_data[i], label=f'Line {i+1}')  # Plot with a label for each line

# Labels and legend
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title(f'Line Graph with {n} Lines')
plt.legend()  # Add legend to distinguish lines

plt.show()

