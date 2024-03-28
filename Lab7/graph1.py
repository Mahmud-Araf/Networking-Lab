import pandas as pd
import matplotlib.pyplot as plt

# Read the data from the file
data = pd.read_csv('data1.csv')

# Plot the data
plt.figure(figsize=(10,6))
plt.plot(data['node'], data['time'],color='green')

# Add labels and title
plt.xlabel('Node')
plt.ylabel('Time(microseconds)')
plt.title('Time vs Node ')

# Show the plot
plt.show()