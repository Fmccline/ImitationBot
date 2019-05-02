import csv
import pandas as pd
import glob

filenames = []
path = 'csv/'
dates = [('08', '14'), ('14', '27')]
for date_range in dates:
	filename = f'{path}2019-04-{date_range[0]}_2019-04-{date_range[1]}-trajectories.csv'
	filenames.append(filename)
output_file = f'{path}2019-04-{dates[0][0]}_2019-04-{dates[1][1]}-trajectories.csv'

data_frames = []
for filename in filenames:
	print(f'Reading from {filename}')
	df = pd.read_csv(filename, index_col=None, header=0)
	data_frames.append(df)

frame = pd.concat(data_frames, axis=0, ignore_index=True)
print(f'Writing to {output_file}')
frame.to_csv(output_file)
print('Finished.')