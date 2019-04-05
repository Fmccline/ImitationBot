import boto3
import datetime

# Let's use Amazon S3
s3 = boto3.resource('s3')

# Upload a new file
today = datetime.date.today()
file_extension = '.log'
bot_names = ['ReliefBot', 'ReliefBot(2)', 'ReliefBot(3)', 'ReliefBot(4)']
for bot_name in bot_names:
    file_name = f'{bot_name}-{today}{file_extension}'
    data = open(file_name, 'rb')
    s3.Bucket('rlbot-logs').put_object(Key=file_name, Body=data)