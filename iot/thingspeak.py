"""
thingspeak.py

Adapted from SYSC3010 project

Notes
-----
- Docstrings follow the numpydoc style:
  https://numpydoc.readthedocs.io/en/latest/format.html
- Code follows the PEP 8 style guide:
  https://www.python.org/dev/peps/pep-0008/
"""
import http.client
import urllib
import requests
import logging
import constants as c


def write_to_channel(key, fields):
    """
    Writes to a given ThingSpeak channel

    Parameters
    ----------
    key : str
    fields : dict
        fields to write to ThingSpeak channel

    Returns
    -------
    status : int
        status of write
    reason : str
        reason for status of write
    """
    headers = {'Content-typZZe': 'application/x-www-form-urlencoded',
               'Accept': 'text/plain'}
    fields['key'] = key
    status = None
    reason = None
    params = urllib.parse.urlencode(fields)
    logging.debug('Fields to write: {}'.format(fields))

    try:
        conn = http.client.HTTPConnection('api.thingspeak.com:80')
        conn.request('POST', '/update', params, headers)
        response = conn.getresponse()
        status = response.status
        reason = response.reason
        conn.close()
    except Exception:
        logging.error("Connection failed!")

    logging.debug('{response_status}, {response_reason}'.format(
        response_status=status,
        response_reason=reason))

    return status, reason


def read_from_channel(key, feed):
    """
    Reads data from a given ThingSpeak channel

    Parameters
    ----------
    key : str
    feed : str

    Returns
    -------
    fields : dict
        fields read from ThingSpeak channel
    """
    read_url = c.READ_URL.format(CHANNEL_FEED=feed, READ_KEY=key)
    fields = requests.get(read_url).json()
    return fields
