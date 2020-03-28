import urllib
import re
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Function used to perform exponential regression
def exponenial_func(x, a, b): #, c):
    return a*np.exp(-b*x) #+c

def estimate_coef(x, y):
	n = np.size(x)
	m_x, m_y = np.mean(x), np.mean(y)
	SS_xy = np.sum(y*x) - n*m_y*m_x
	SS_xx = np.sum(x*x) - n*m_x*m_x
	
	b_1 = SS_xy / SS_xx
	b_0 = m_y - b_1*m_x
	
	return (b_0, b_1)


# Read in webpage
# link = "https://www.worldometers.info/coronavirus/country/us/"
# f = urllib.urlopen(link)
# print f
# myfile = f.read()
# 
# linenumber = 0
# 
# searchingCases = False
# searchingDeaths = False
# 
dates4cases = ["Feb 15","Feb 16","Feb 17","Feb 18","Feb 19","Feb 20","Feb 21","Feb 22","Feb 23","Feb 24","Feb 25","Feb 26","Feb 27","Feb 28","Feb 29","Mar 01","Mar 02","Mar 03","Mar 04","Mar 05","Mar 06","Mar 07","Mar 08","Mar 09","Mar 10","Mar 11","Mar 12","Mar 13","Mar 14","Mar 15","Mar 16","Mar 17","Mar 18","Mar 19","Mar 20","Mar 21","Mar 22","Mar 23","Mar 24","Mar 25","Mar 26","Mar 27"] 
dates4deaths = ["Feb 15","Feb 16","Feb 17","Feb 18","Feb 19","Feb 20","Feb 21","Feb 22","Feb 23","Feb 24","Feb 25","Feb 26","Feb 27","Feb 28","Feb 29","Mar 01","Mar 02","Mar 03","Mar 04","Mar 05","Mar 06","Mar 07","Mar 08","Mar 09","Mar 10","Mar 11","Mar 12","Mar 13","Mar 14","Mar 15","Mar 16","Mar 17","Mar 18","Mar 19","Mar 20","Mar 21","Mar 22","Mar 23","Mar 24","Mar 25","Mar 26","Mar 27"] 
cases = [15,15,15,15,15,15,35,35,35,53,57,60,60,63,68,75,100,124,158,221,319,435,541,704,994,1301,1630,2183,2770,3613,4596,6344,9197,13779,19367,24192,33592,43781,54856,68211,85435,104126]
deaths = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,6,9,11,12,15,19,22,26,30,38,41,48,57,69,87,110,150,206,255,301,414,555,780,1027,1295,1696]
dates = ["Mar 01","Mar 02","Mar 03","Mar 04","Mar 05","Mar 06","Mar 07","Mar 08","Mar 09","Mar 10","Mar 11","Mar 12","Mar 13","Mar 14","Mar 15","Mar 16","Mar 17","Mar 18","Mar 19","Mar 20","Mar 21","Mar 22","Mar 23","Mar 24","Mar 25","Mar 26","Mar 27","Mar 28","Mar 29","Mar 30","Mar 31", \
"Apr 01","Apr 02","Apr 03","Apr 04","Apr 05","Apr 06","Apr 07","Apr 08","Apr 09","Apr 10","Apr 11","Apr 12"] #,"Apr 13","Apr 14","Apr 15","Apr 16","Apr 17","Apr 18","Apr 19","Apr 20","Apr 21","Apr 22","Apr 23","Apr 24","Apr 25","Apr 26","Apr 27","Apr 28","Apr 29","Apr 30"]

new_cases = [0,0,0,0,0,0,20,0,0,18,4,3,0,3,5,7,25,24,34,63,98,116,106,163,290,307,329,553,587,843,983,1748,2853,4582,5588,4825,9400,10189,11075,13355,17224,18691]
new_deaths = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,5,3,2,1,3,4,3,4,4,8,3,7,9,12,18,23,40,56,49,46,113,141,225,247,268,401]
# 
# 
# Extract data
# for line in myfile.split('\n'):
# 
# 	# Find the line where the "Total Cases" is found
# 	searchObj = re.search("Total Cases", line)
# 	if searchObj:
# 		print line
# 		searchingCases = True
# 		
# 	# Find the line where the "Total Deaths" is found
# 	searchObj = re.search("Total Deaths", line)
# 	if searchObj:
# 		print line
# 		searchingDeaths = True
# 		
# 	# Get the date and data values for the Total Cases
# 	if searchingCases:
# 		searchDates = re.search("categories: \[(.+)\]", line)
# 		if searchDates:
# 			dates4cases = searchDates.group(1).split(',')
# 		searchCases = re.search("data: \[([\d,]+)\]", line)
# 		if searchCases:
# 			cases = searchCases.group(1).split(',')
# 			searchingCases = False
# 			
# 	# Get the date and data values for the Total Deaths	
# 	if searchingDeaths:
# 		searchDates = re.search("categories: \[(.+)\]", line)
# 		if searchDates:
# 			dates4deaths = searchDates.group(1).split(',')
# 		searchCases = re.search("data: \[([\d,]+)\]", line)
# 		if searchCases:
# 			deaths = searchCases.group(1).split(',')
# 			searchingDeaths = False
# 	#print linenumber, line
# 	linenumber += 1
# print(myfile)

# Used to determine the index of March 01
startIndex = -1

# Format data
for i in range(len(cases)):
	# Convert strings to ints
	cases[i] = int(cases[i])
	deaths[i] = int(deaths[i])
	new_cases[i] = int(new_cases[i])
	new_deaths[i] = int(new_deaths[i])
	## Strip opening and closing double quotes if reading from webpage
	#dates4cases[i] = dates4cases[i][1:len(dates4cases[i])-1]
	#dates4deaths[i] = dates4deaths[i][1:len(dates4deaths[i])-1]
	# Get the index of "Mar 01"
	if dates4cases[i] == "Mar 01":
		startIndex = i
		
# Convert to numpy arrays for regression
cases = np.asarray(cases)
deaths = np.asarray(deaths)
new_cases = np.asarray(new_cases)
new_deaths = np.asarray(new_deaths)

# Perform exponential regression

# Initialize data starting at March 1
indices = np.asarray(range(0, len(cases)-startIndex))
total_cases = cases[startIndex:]
total_deaths = deaths[startIndex:]
new_cases = new_cases[startIndex:]
new_deaths = new_deaths[startIndex:]

# Used as input x-values for projections
proj_x = np.arange(0, 42)

# Compute exponential regression on total cases
(b_0, b_1) = estimate_coef(indices, np.log(total_cases))
# print "b_0 = ", b_0
# print "b_1 = ", b_1
# print "coef = ", np.exp(b_0)
proj_cases = np.exp(b_0) * np.exp(b_1*proj_x)

# Compute exponential regression for total deaths
(b_0, b_1) = estimate_coef(indices, np.log(total_deaths))
# print "b_0 = ", b_0
# print "b_1 = ", b_1
# print "coef = ", np.exp(b_0)
proj_deaths = np.exp(b_0) * np.exp(b_1*proj_x)

#Compute exponential regression on new cases
(b_0, b_1) = estimate_coef(indices, np.log(new_cases))
proj_new_cases = np.exp(b_0) * np.exp(b_1*proj_x)

#Compute exponential regression for new deaths
(b_0, b_1) = estimate_coef(indices, np.log(new_deaths+1))	# Add 1 here since some values are 0
proj_new_deaths = np.exp(b_0) * (np.exp(b_1*proj_x)-1)		# Subtract 1 here to reverse the previous addition

# Format the projection data (and zero out where existing data is)
for i in range(len(total_cases)):
	proj_cases[i] = 0
	proj_deaths[i] = 0
 	proj_new_cases[i] = 0
 	proj_new_deaths[i] = 0
for i in range(len(total_cases), len(proj_cases)):
	proj_cases[i] = int(proj_cases[i])
	proj_deaths[i] = int(proj_deaths[i])
 	proj_new_cases[i] = int(proj_new_cases[i])
 	proj_new_deaths[i] = int(proj_new_deaths[i])
	
print "estimated total cases on April 12: ", int(proj_cases[-1])
print "estimated total deaths on April 12: ", int(proj_deaths[-1])

LOG = True
LIN = True

if LOG:

	fig1 = plt.figure()
	plt.suptitle('US Coronavirus Statistics')

	# Step size for x-axis ticks
	step = 4
	ann_step = 3
	len1 = len(total_cases)
	len2 = len(proj_cases)

	plt.subplot(2,1,1)
	plt.title("Total Cases & Deaths")
	plt.yscale("log")

	# Plot total cases, deaths, and projections
	plt.plot(total_cases, '.', label="Total Cases")
	plt.plot(proj_cases, '+', label="Projected Cases")
	plt.plot(total_deaths, '.', label="Total Deaths")
	plt.plot(proj_deaths, '+', label="Projected Deaths")

	for x,y in zip(proj_x[0:len1:ann_step], total_cases[::ann_step]):                                       # <--
		plt.annotate('%s' % y, xy=(x,y), textcoords='data') # <--# Logarithmic y-axis
	for x,y in zip(proj_x[len1:len2:ann_step], proj_cases[len1:len2:ann_step]):                                       # <--
		plt.annotate('%s' % int(y), xy=(x,y), textcoords='data') # <--# Logarithmic y-axis
	for x,y in zip(proj_x[0:len1:ann_step], total_deaths[::ann_step]):                                       # <--
		plt.annotate('%s' % y, xy=(x,y), textcoords='data') # <--# Logarithmic y-axis
	for x,y in zip(proj_x[len1:len2:ann_step], proj_deaths[len1:len2:ann_step]):                                       # <--
		plt.annotate('%s' % int(y), xy=(x,y), textcoords='data') # <--# Logarithmic y-axis
	plt.annotate('%s' % int(proj_cases[-1]), xy=(proj_x[-1],proj_cases[-1]), textcoords='data')
	plt.annotate('%s' % int(proj_deaths[-1]), xy=(proj_x[-1],proj_deaths[-1]), textcoords='data')
	# Display dates on x-axis
	plt.xticks(np.arange(0,42,step), dates[0:len(dates):step])
	# Display legend
	plt.legend(loc=4)
	#plt.title("US Coronavirus Statistics")

	plt.subplot(2,1,2)
	plt.title("New Cases & Deaths")
	plt.yscale("log")

	# Plot total cases, deaths, and projections
	plt.plot(new_cases, '.', label="New Cases")
	plt.plot(proj_new_cases, '+', label="Projected New Cases")
	plt.plot(new_deaths, '.', label="New Deaths")
	plt.plot(proj_new_deaths, '+', label="Projected New Deaths")

	for x,y in zip(proj_x[0:len1:ann_step], new_cases[::ann_step]):                                       # <--
		plt.annotate('%s' % y, xy=(x,y), textcoords='data') # <--# Logarithmic y-axis
	for x,y in zip(proj_x[len1:len2:ann_step], proj_new_cases[len1:len2:ann_step]):                                       # <--
		plt.annotate('%s' % int(y), xy=(x,y), textcoords='data') # <--# Logarithmic y-axis
	for x,y in zip(proj_x[0:len1:ann_step], new_deaths[::ann_step]):                                       # <--
		plt.annotate('%s' % y, xy=(x,y), textcoords='data') # <--# Logarithmic y-axis
	for x,y in zip(proj_x[len1:len2:ann_step], proj_new_deaths[len1:len2:ann_step]):                                       # <--
		plt.annotate('%s' % int(y), xy=(x,y), textcoords='data') # <--# Logarithmic y-axis
	plt.annotate('%s' % int(proj_new_cases[-1]), xy=(proj_x[-1],proj_new_cases[-1]), textcoords='data')
	plt.annotate('%s' % int(proj_new_deaths[-1]), xy=(proj_x[-1],proj_new_deaths[-1]), textcoords='data')
	# Display dates on x-axis
	plt.xticks(np.arange(0,42,step), dates[0:len(dates):step])
	# Display legend
	plt.legend(loc=4)

if LIN:

	fig2 = plt.figure()
	plt.suptitle('US Coronavirus Statistics')
	
	# Step size for x-axis ticks
	step = 4
	ann_step = 3
	len1 = len(total_cases)
	len2 = len(proj_cases)

	plt.subplot(2,2,1)
	plt.title("Total Cases")

	# Plot total cases, deaths, and projections
	plt.plot(total_cases, '.', label="Total Cases")
	plt.plot(proj_cases, '+', label="Projected Cases")
	

	for x,y in zip(proj_x[0:len1:ann_step], total_cases[::ann_step]):                                       # <--
		plt.annotate('%s' % y, xy=(x,y), textcoords='data') # <--# Logarithmic y-axis
	for x,y in zip(proj_x[len1:len2:ann_step], proj_cases[len1:len2:ann_step]):                                       # <--
		plt.annotate('%s' % int(y), xy=(x,y), textcoords='data') # <--# Logarithmic y-axis
	
	plt.annotate('%s' % int(proj_cases[-1]), xy=(proj_x[-1],proj_cases[-1]), textcoords='data')
	# Display dates on x-axis
	plt.xticks(np.arange(0,42,step), dates[0:len(dates):step])
	# Display legend
	plt.legend(loc=2)
	#plt.title("US Coronavirus Statistics")

	plt.subplot(2,2,2)
	plt.title("New Cases")

	plt.plot(new_cases, '.', label="New Cases")
	plt.plot(proj_new_cases, '+', label="Projected New Cases")
	
	for x,y in zip(proj_x[0:len1:ann_step], new_cases[::ann_step]):                                       # <--
		plt.annotate('%s' % y, xy=(x,y), textcoords='data') # <--# Logarithmic y-axis
	for x,y in zip(proj_x[len1:len2:ann_step], proj_new_cases[len1:len2:ann_step]):                                       # <--
		plt.annotate('%s' % int(y), xy=(x,y), textcoords='data') # <--# Logarithmic y-axis
	plt.annotate('%s' % int(proj_new_cases[-1]), xy=(proj_x[-1],proj_new_cases[-1]), textcoords='data')
	# Display dates on x-axis
	plt.xticks(np.arange(0,42,step), dates[0:len(dates):step])
	# Display legend
	plt.legend(loc=2)
	
	
	plt.subplot(2,2,3)
	plt.title("Total Deaths")
	
	plt.plot(total_deaths, '.', label="Total Deaths")
	plt.plot(proj_deaths, '+', label="Projected Deaths")
	
	for x,y in zip(proj_x[0:len1:ann_step], total_deaths[::ann_step]):                                       # <--
		plt.annotate('%s' % y, xy=(x,y), textcoords='data') # <--# Logarithmic y-axis
	for x,y in zip(proj_x[len1:len2:ann_step], proj_deaths[len1:len2:ann_step]):                                       # <--
		plt.annotate('%s' % int(y), xy=(x,y), textcoords='data') # <--# Logarithmic y-axis
	plt.annotate('%s' % int(proj_deaths[-1]), xy=(proj_x[-1],proj_deaths[-1]), textcoords='data')

	# Display dates on x-axis
	plt.xticks(np.arange(0,42,step), dates[0:len(dates):step])
	# Display legend
	plt.legend(loc=2)
	
	plt.subplot(2,2,4)
	plt.title("New Deaths")
	
	plt.plot(new_deaths, '.', label="New Deaths")
	plt.plot(proj_new_deaths, '+', label="Projected New Deaths")
	
	for x,y in zip(proj_x[0:len1:ann_step], new_deaths[::ann_step]):                                       # <--
		plt.annotate('%s' % y, xy=(x,y), textcoords='data') # <--# Logarithmic y-axis
	for x,y in zip(proj_x[len1:len2:ann_step], proj_new_deaths[len1:len2:ann_step]):                                       # <--
		plt.annotate('%s' % int(y), xy=(x,y), textcoords='data') # <--# Logarithmic y-axis
	plt.annotate('%s' % int(proj_new_deaths[-1]), xy=(proj_x[-1],proj_new_deaths[-1]), textcoords='data')
	# Display dates on x-axis
	plt.xticks(np.arange(0,42,step), dates[0:len(dates):step])
	# Display legend
	plt.legend(loc=2)

plt.show()

# print "Dates for cases: ", dates4cases
# print "     Cases: ", total_cases
# print "Proj Cases: ", print_proj_cases
# print "Dates for deaths: ", dates4deaths
# print "     Deaths: ", deaths
# print "Proj Deaths: ", proj_deaths

#print "startIndex = ", startIndex