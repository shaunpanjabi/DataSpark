#############################################################################################
# DataSpark API
# Author: Shaun Panjabi
#
# Description:
#   -Python API to allow interfacing with data.sparkfun.com
#
# See SparkFun docs for more info on how http requests are made:
#     http://phant.io/docs/
#
# License: MIT, see LICENSE for more details.
#
#############################################################################################

import matplotlib.pyplot as plt
from dateutil import tz
import requests
import datetime
import httplib
import json

# Data.SparkFun Constants
BASE_URL = "https://data.sparkfun.com/"

class DataSparker():
    """
    Send and receive data to a Phant server. This doesn't only have to be used for SparkFun. You can deploy your own
    Phant server if you prefer to keep your data to yourself. See link above for info on customizing your Phant Server.

    """
    def __init__(self, public_key, private_key, delete_key=None, base_url=BASE_URL,):
        """
        Constructor for DataSparker class

        :param public_key: {string} Public key for SparkFun data stream
        :param private_key: {string} Private key for SparkFun data stream.
        :param delete_key: {string} Delete key for SparkFun data stream.
        :param base_url: {string} SparkFun base URL (Only change if you're deploying your own Phant server).
        """
        self.base_url = base_url
        self.public_key = public_key
        self.private_key = private_key
        self.delete_key = delete_key

        self.available_formats = ['json', 'csv', 'sql', 'psql', 'atom']

    def send_data(self, **kwargs):
        """
        Send data to data stream.

        :param: Whatever data you want to send. For example, if your data stream has the fields duration and distance,
                you would do:
                    send_data(duration=value1, distance=value2)
        :return: Response from request. If not successful, False is returned.
        """
        request_type = "input/"
        url = self.base_url + request_type + self.public_key + '?' + 'private_key=' + self.private_key
        response = requests.post(url, kwargs)
        if response.status_code != 200:
            print ("Request was not successful:\n" + response.text)
            return False
        else:
            print "Data sent successfully."
            return response

    def download_data(self, data_format='json'):
        """
        Download all data from a data stream.

        :param data_format: {string} See available_formats, for allowed data formats.
        :return: If json is selected, a {dictionary} is returned. Otherwise the data is returned in a {string}.
                 This can be manually saved to a file. Eventually, save functionality will be added.
        """
        # TODO: Add save to file option
        # TODO: Add page selection option
        response_type = "output/"
        if data_format not in self.available_formats:
            raise Exception("Pick from available formats: " + str(self.available_formats))
        url = self.base_url + response_type + self.public_key + '.' + data_format
        response = requests.get(url)
        resp = response.text
        if data_format == 'json':
            resp = json.loads(resp)
        return resp

    def clear_stream(self):
        """
        CAUTION: USE AT YOUR OWN RISK!!
        This actually clears your entire stream, and cannot be undone. All data is wiped, however you can still upload
        new data to the stream if you would like.

        :return: {bool} If clear succeeds, True is returned
        """
        clear_status = False
        request_type = ['input/', '/clear']
        url = self.base_url + request_type[0] + self.public_key + request_type[1] + '?private_key=' + self.private_key
        response = requests.get(url)
        if response.status_code == httplib.ACCEPTED:
            clear_status = True
        return clear_status

    def delete_stream(self, confirm=False):
        """
        CAUTION: USE AT YOUR OWN RISK!!
        This actually deletes your entire stream, and cannot be undone. You will have to create a new stream with
        different public keys after delete your stream.

        :param confirm: {bool} set to True to confirm that you want to delete the stream.
        :return: {bool} If delete succeeds, True is returned
        """
        if not self.delete_key:
            raise Exception("No delete key specified.")
        if confirm:
            request_type = "delete/"
            url = self.base_url + 'streams/' + self.public_key + '/' + request_type + self.delete_key
            response = requests.get(url)
            if response == httplib.ACCEPTED:
                delete_status = True
            else:
                delete_status = False
            return delete_status
        else:
            raise Exception("Are you sure you want to do this?\n"
                            "If so, set the confirm parameter to True.")

    def get_stream_stats(self):
        """
        Returns stats of the current state of data stream

        :return: {dict} with keys:
                    pageCount - The number of pages your data will span when paging your data during output.
                    remaining - The number of bytes you have remaining before hitting your data cap.
                    used - The number of bytes your stream is currently using.
                    cap - The current cap setting for your stream in bytes.
        """
        request_type = ['output/', '/stats.json']
        url = self.base_url + request_type[0] + self.public_key + request_type[1]
        response = requests.get(url)
        return json.loads(response.text)
