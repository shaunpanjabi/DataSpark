#############################################################################################
# DataSpark Example
# Author: Shaun Panjabi
#
# Description:
#   -Example script for DataSpark.py. Shows normal usage of DataSpark.py.
#
# See SparkFun docs for more info on how http requests are made:
#     http://phant.io/docs/
#
#############################################################################################

from DataSpark import *

PRIVATE_KEY = 'b5JNAPGqMmfmxjBk5KRx'
PUBLIC_KEY = '4JL93NYp7yi4a9mJL7Wa'

ds = DataSparker(public_key=PUBLIC_KEY, private_key=PRIVATE_KEY)
url = ds.base_url + 'streams/' + PUBLIC_KEY

print('/*-------------------------------------------------*/')

print("Clear stream so that it is at a known state.")
if not ds.clear_stream():
    raise Exception("CLEAR STREAM FAILED!")

print('/*-------------------------------------------------*/')

print("Send a few points to the data stream.")
for i in xrange(10):
    print("Sending packet# {}....").format(i)
    ds.send_data(test=i)

print("Display stream stats:")
stream_stats = ds.get_stream_stats()
print("Number of Pages:....................{}").format(stream_stats['pageCount'])
print("Number of Bytes Remaining:..........{}").format(stream_stats['remaining'])
print("Numer of Bytes Used:................{}").format(stream_stats['used'])
print("Current Cap Setting (Bytes):........{}").format(stream_stats['cap'])

print('/*-------------------------------------------------*/')

print("Download data from data stream.")
received_data_1 = ds.download_data()

print('/*-------------------------------------------------*/')

print("Check if data shows up at this link: {}").format(url)
raw_input("Press enter to continue...")

print('/*-------------------------------------------------*/')

print("Clear data stream.")
ds.clear_stream()

print("Attempt to download data.")
received_data_2 = ds.download_data()

print("Verify that data was not recieved:")
if not received_data_2['success']:
    print("Clear data stream, was a success!")
else:
    raise Exception("DATA WAS NOT CLEARED, SOMETHING WENT WRONG!")

print('/*-------------------------------------------------*/')

print("Check if data was cleared from link: {}").format(url)
raw_input("Press enter to continue...")

print('/*-------------------------------------------------*/')

print("Display stream stats:")
stream_stats = ds.get_stream_stats()
print("Number of Pages:....................{}").format(stream_stats['pageCount'])
print("Number of Bytes Remaining:..........{}").format(stream_stats['remaining'])
print("Numer of Bytes Used:................{}").format(stream_stats['used'])
print("Current Cap Setting (Bytes):........{}").format(stream_stats['cap'])

print("Clear stream to return back to normal state.")
ds.clear_stream()