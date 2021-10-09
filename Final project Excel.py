import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress
from scipy.stats import pearsonr
# Importing necessary extensions to complete this second half of the project.
koalapoints = pd.read_excel(r"C:\Users\dsmcm\Desktop\Final project Programming\result_table.xls")
print(koalapoints)
# Establishing a link to the excel spreadsheet, following with printing the values that are in each cell.
x = list(koalapoints['Metres'])
y = list(koalapoints['Koala_Num'])
# Assigning the x & y values to the length of the road within each location and the number of koalas.
plt.figure(figsize=(10,10))
# Creating the plot graph to be a size of 10 by 10, with the default value of inches. So it will be 10 inches by 10 inches.
plt.scatter(x,y)
# Making the plot graph to be a scatter plot
plt.title("Road Impact on Koala Distribution")
# Creating the title name of the project.
plt.show()
# Displaying the scatter plot along with the title.
corr, _ = pearsonr(x,y)
print('Pearsons correlation: %.3f' % corr)
# Following formula of pearsonr is used to calculate a Pearson correlation coefficient.



