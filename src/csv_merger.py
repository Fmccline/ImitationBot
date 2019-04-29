import csv
import pandas as pd
import glob

filenames = []
path = 'csv/'
dates = [(14, 21), (21, 27)]
for date_range in dates:
	filename = f'{path}2019-04-{date_range[0]}_2019-04-{date_range[1]}-trajectories.csv'
	filenames.append(filename)
output_file = path + '2019-04-14_2019-04-27-trajectories.csv'

li = []
for filename in filenames:
	print(f'Reading from {filename}')
	df = pd.read_csv(filename, index_col=None, header=0)
	li.append(df)

frame = pd.concat(li, axis=0, ignore_index=True)
print(f'Writing to {output_file}')
frame.to_csv(output_file)
print('Finished.')