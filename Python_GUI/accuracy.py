import numpy as np
import matplotlib.pyplot as plt

# Model names
models = ['MobileFaceNet', 'MiniFASNetV1', 'MiniFASNetV2']

# Initial and final accuracy scores for each model
initial_accuracy = [0, 0, 0]
final_accuracy = [82, 93, 97]

# Time intervals
time_intervals = np.linspace(0, 1, 10)

# Generate random fluctuations for each model's accuracy
accuracy_fluctuations = []
for idx, model in enumerate(models):
    fluctuations = np.random.uniform(low=-5, high=5, size=len(time_intervals))
    accuracy_fluctuations.append(fluctuations)
    final_accuracy_point = [final_accuracy[idx]] * len(time_intervals)
    plt.plot(time_intervals, final_accuracy_point, linestyle='--', color='gray')  # Plot final accuracy line
    plt.text(1, final_accuracy[idx], f'{model} - {final_accuracy[idx]}%', va='center', ha='left')  # Annotate final accuracy

# Create line plot with fluctuations
plt.figure(figsize=(8, 6))
for model, init_acc, final_acc, fluctuations in zip(models, initial_accuracy, final_accuracy, accuracy_fluctuations):
    accuracy = init_acc + (final_acc - init_acc) * time_intervals + fluctuations
    plt.plot(time_intervals, accuracy, label=model)

# Add labels and title
plt.xlabel('Time')
plt.ylabel('Accuracy (%)')
plt.title('Accuracy Growth of Face Recognition Models with Fluctuations')
plt.xticks([0, 0.5, 1], ['Initial', 'Mid', 'Final'])
plt.ylim(0, 100)  # Set y-axis limit
plt.legend()

# Display the graph
plt.show()
