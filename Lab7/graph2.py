import pandas as pd
import matplotlib.pyplot as plt

# Read the data from the file
data = pd.read_csv('data2.csv')

# Plot the data
plt.figure(figsize=(10,6))
plt.plot(data['node'], data['memory'],color='red')

# Add labels and title
plt.xlabel('Node')
plt.ylabel('memory(bytes)')
plt.title('Memory vs Node ')

# Show the plot
plt.show()