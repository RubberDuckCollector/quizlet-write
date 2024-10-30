import matplotlib.pyplot as plt  # type: ignore
import numpy as np

x_axes = [0.0, 25.0, 50.0, 75.0, 100]

y_axes = [[0.0, 100.0, 100.0, 67.0, 100],
          [0.0, 0.0, 100.0, 67.0, 100]]

plt.xlim(0, 100)
plt.xticks([i for i in range(0, 105, 5)])

# Plot each line
for i, y_data in enumerate(y_axes):
    plt.plot(x_axes, y_data, label=f'Round {i + 1}')

# Set plot titles and labels
plt.title("Quiz Accuracy Over Progress")
plt.xlabel("% Progress")
plt.ylabel("% Accuracy")
plt.legend(loc="lower right")

# Display the plot
plt.show()
