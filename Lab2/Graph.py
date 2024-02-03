import pandas as pd
import matplotlib.pyplot as plt

# Read the data from the file
data = pd.read_csv('time.csv')

# Plot the data
plt.figure(figsize=(10,6))
plt.plot(data['process_no'], data['time_taken'])

# Add labels and title
plt.xlabel('Error(%)')
plt.ylabel('Time Taken for 100 requests(milliseconds)')
plt.title('Time Delay over Error Rate')

# Show the plot
plt.show()