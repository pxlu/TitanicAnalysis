import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import pprint
import csv

def read_data(input_csv):
  data = pd.read_csv(input_csv)
  return (data, data.columns.values)

def get_direct_values(data):

  direct_values_dir = {}  

  # By Sex
  direct_values_dir['male_data'] = data[data['Sex'] == 'male']
  direct_values_dir['female_data'] = data.drop(data[data['Sex'] == 'male'].index.tolist())

  # By Age -- >18 vs <= 18
  direct_values_dir['child_data'] = data[data['Age'] <= 18]
  direct_values_dir['adult_data'] = data.drop(data[data['Age'] <= 18].index.tolist())

  # By Passenger Class
  direct_values_dir['class_1_data'] = data[data['Pclass'] == 1]
  direct_values_dir['class_2_data'] = data[data['Pclass'] == 2]
  direct_values_dir['class_3_data'] = data[data['Pclass'] == 3]

  return direct_values_dir

def get_indirect_values(data):

  indirect_values_dir = {}

  # By siblings or spouses, >0 vs 0
  indirect_values_dir['SibSp > 0'] = data[data['SibSp'] > 0]
  indirect_values_dir['SibSp == 0'] = data[data['SibSp'] == 0]

  # By parents or children, >0 vs 0
  indirect_values_dir['Parch > 0'] = data[data['Parch'] > 0]
  indirect_values_dir['Parch == 0'] = data[data['Parch'] == 0]

  return indirect_values_dir

def get_other_data(data):

  other_values_dir = {}

  # By fare, either lesser or equal, or greater than average fare
  other_values_dir['<= Average Fare'] = data[data.loc[:, 'Fare'] <= data.loc[:, 'Fare'].mean()]
  other_values_dir['> Average Fare'] = data.drop(data[data.loc[:, 'Fare'] <= data.loc[:, 'Fare'].mean()].index.tolist())

  # By Port of destination
  other_values_dir['Dest:Southhampton'] = data[data['Embarked'] == 'S']
  other_values_dir['Dest:Queenstown'] = data[data['Embarked'] == 'Q']
  other_values_dir['Dest:Cherbourg'] = data[data['Embarked'] == 'C']
  other_values_dir['Dest:UNKNOWN'] = data[data['Embarked'] == 'UNKNOWN']

  return other_values_dir

def describe_data(data):

  data_headers = list(set([value for value in data.keys()]))

  for d_index in range(len(data_headers)):
    print "Describing survival rates for " + str(data_headers[d_index])
    print data[data_headers[d_index]]['Survived'].mean()
    print data[data_headers[d_index]]['Survived'].count()

def compare_to_Pclass(data):

  data_headers = [header for header in list(set([value for value in data.keys()])) if 'class' not in header]

  for header in data_headers:
    print 'Survival rates for ' + str(header).upper() + ' & Pclass_1'
    x1 = data[header][data[header]['Pclass'] == 1]['Survived']
    print x1.mean(), x1.count()
    print 'Survival rates for ' + str(header).upper() + ' & Pclass_2'
    x2 = data[header][data[header]['Pclass'] == 2]['Survived']
    print x2.mean(), x2.count()
    print 'Survival rates for ' + str(header).upper() + ' & Pclass_3'
    x3 = data[header][data[header]['Pclass'] == 3]['Survived']
    print x3.mean(), x3.count()

def compare_to_Age(data):

  ex = ['adult_data', 'child_data']

  data_headers = [header for header in list(set([value for value in data.keys()])) if header not in ex]

  for header in data_headers:
    print 'Survival rates for ' + str(header).upper() + ' & Is_child'
    x1 = data[header][data[header]['Age'] <= 18]['Survived']
    print x1.mean(), x1.count()
    print 'Survival rates for ' + str(header).upper() + ' & Is_adult'
    x2 = data[header][data[header]['Age'] > 18]['Survived']
    print x2.mean(), x2.count()

def compare_to_Sex(data):

  ex = ['male_data', 'female_data']

  data_headers = [header for header in list(set([value for value in data.keys()])) if header not in ex]

  for header in data_headers:
    print 'Survival rates for ' + str(header).upper() + ' & Is_male'
    x1 = data[header][data[header]['Sex'] == 'male']['Survived']
    print x1.mean(), x1.count()
    print 'Survival rates for ' + str(header).upper() + ' & Is_female'
    x2 = data[header][data[header]['Sex'] == 'female']['Survived']
    print x2.mean(), x2.count()

def aggregate_direct_survival(data):

  compare_to_Pclass(data)
  compare_to_Age(data)
  compare_to_Sex(data)

def compare_to_SibSp(data):

  data_headers = list(set([value for value in data.keys()]))

  for header in data_headers:
    print 'Survival rates for ' + str(header).upper() + ' & SibSp == 0'
    x1 = data[header][data[header]['SibSp'] == 0]['Survived']
    print x1.mean(), x1.count()
    print 'Survival rates for ' + str(header).upper() + ' & SibSp > 0'
    x2 = data[header][data[header]['SibSp'] > 0]['Survived']
    print x2.mean(), x2.count()

def compare_to_Parch(data):

  data_headers = list(set([value for value in data.keys()]))

  for header in data_headers:
    print 'Survival rates for ' + str(header).upper() + ' & Parch == 0'
    x1 = data[header][data[header]['Parch'] == 0]['Survived']
    print x1.mean(), x1.count()
    print 'Survival rates for ' + str(header).upper() + ' & Parch > 0'
    x2 = data[header][data[header]['Parch'] > 0]['Survived']
    print x2.mean(), x2.count()

def aggregate_indirect_survival(data):

  compare_to_SibSp(data)
  compare_to_Parch(data)

def compare_other(data):

  print 'Fare & Pclass_1'
  print data['class_1_data']['Fare'].describe()
  print 'Fare & Pclass_2'
  print data['class_2_data']['Fare'].describe()
  print 'Fare & Pclass_3'
  print data['class_3_data']['Fare'].describe()

  print 'Is_male & SibSp and Parch'
  print data['male_data'][['SibSp', 'Parch']].mean()

  print 'Is_female & SibSp and Parch'
  print data['female_data'][['SibSp', 'Parch']].mean()

def main():
  data, headers = read_data('titanic_data.csv')
  # Fill in missing information from cabin NaNs
  data.fillna(value='UNKNOWN', inplace=True)
  data.loc[:, 'Age'].replace('UNKNOWN', 0, inplace=True)

  data2 = data.copy()
  data2.Sex.replace(['male','female'], [0, 1], inplace=True)

  # Split the data first into the direct influential categories
  direct_values = get_direct_values(data)
  indirect_values = get_indirect_values(data)
  other_values = get_other_data(data)

  print data['Fare'].corr(data['Pclass'])
  # describe_data(direct_values)
  # describe_data(indirect_values)
  # describe_data(other_values)

  # Find some combinations of variables --

  # aggregate_direct_survival(direct_values)
  # aggregate_indirect_survival(direct_values)

  # compare_other(direct_values)
  
  # plt.show()
  # print data2.corr()

if __name__=='__main__':
  main()