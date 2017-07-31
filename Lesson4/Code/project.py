import numpy as np
import pandas as pd

titanic_df = pd.read_csv('../titanic_data.csv')


# How many of the survivals where female and male
print 'How many of the survivals where female and male'
print titanic_df.groupby('Sex')['Survived'].sum()

# How many of the survivals per class
print 'How many of the survivals per class'
print titanic_df.groupby('Pclass')['Survived'].sum()

# Mean price for each class
print 'Mean price for each class'
print titanic_df.groupby('Pclass')['Fare'].mean()

# Graphical plot of tickets fare
print 'Graphical plot of tickets fare'

ticket_fare = titanic_df['Fare']
ticket_standarize = (ticket_fare - ticket_fare.mean()) / ticket_fare.std(ddof=0)
ticket_standarize.plot()