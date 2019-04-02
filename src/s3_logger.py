import boto3

# Let's use Amazon S3
s3 = boto3.resource('s3')

# Upload a new file
file_names = ['ReliefBot.log', 'ReliefBot(2).log', 'ReliefBot(3).log', 'ReliefBot(4).log']
for file_name in file_names:
    data = open(file_name, 'rb')
    s3.Bucket('rlbot-logs').put_object(Key=file_name, Body=data)