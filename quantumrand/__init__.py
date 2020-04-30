# Copyright (c) 2012-2013 Luke Macken <lmacken@redhat.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""
A Python interface to the ANU Quantum Random Numbers Server.

http://qrng.anu.edu.au
"""

import binascii
import requests
import math
import sys
import six
try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode
try:
    import json
except ImportError:
    import simplejson as json

# Until ANU Updates their SSL certificate, we will have to work around it.
# Please contact ANU to let them know their SSL certificate is expired so that
# they know we are still using this amazing API!
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# I will update the moment I find out it is valid again

VERSION = '2.1.1'
URL = 'https://qrng.anu.edu.au/API/jsonI.php'
DATA_TYPES = ['uint16', 'hex16']
MAX_LEN = 1024
INT_BITS = 16


def get_data(data_type='uint16', array_length=1, block_size=1):
    """Fetch data from the ANU Quantum Random Numbers JSON API"""
    if data_type not in DATA_TYPES:
        raise Exception("data_type must be one of %s" % DATA_TYPES)
    if array_length > MAX_LEN:
        raise Exception("array_length cannot be larger than %s" % MAX_LEN)
    if block_size > MAX_LEN:
        raise Exception("block_size cannot be larger than %s" % MAX_LEN)
    url = URL + '?' + urlencode({
        'type': data_type,
        'length': array_length,
        'size': block_size,
    })
    data = get_json(url)
    assert data['success'] is True, data
    assert data['length'] == array_length, data
    return data['data']


if sys.version_info[0] == 2:
    def get_json(url):
        return requests.get(url, verify=False).json()

    def _object_hook(obj):
        """We are only dealing with ASCII characters"""
        if obj.get('type') == 'string':
            obj['data'] = [s.encode('ascii') for s in obj['data']]
        return obj

    if sys.version_info[1] in (4, 5):
        _sentinel = object()
        def next(it, default=_sentinel):
            try:
                return it.next()
            except StopIteration:
                if default is _sentinel:
                    raise
                return default
else:
    def get_json(url):
        return requests.get(url, verify=False).json()


def binary(array_length=100, block_size=100):
    """Return a chunk of binary data"""
    return binascii.unhexlify(six.b(hex(array_length, block_size)))


def hex(array_length=100, block_size=100):
    """Return a chunk of hex"""
    return ''.join(get_data('hex16', array_length, block_size))


def randfloat(min=0, max=10, generator=None):
    """Return an int between min and max. If given, takes from generator instead.
    This can be useful to reuse the same cached_generator() instance over multiple calls."""
    rand_range = max - min
    if rand_range == 0:
        # raise ValueError("range cannot be zero")  # meh
        return min

    if generator is None:
        generator = cached_generator()

    source_bits = int(math.ceil(math.log(rand_range + 1, 2)))
    source_size = int(math.ceil(source_bits / float(INT_BITS)))
    source_max = 2 ** (source_size * INT_BITS) - 1

    modulos = source_max / rand_range
    too_big = modulos * rand_range
    while True:
        num = 0
        for x in range(source_size):
            num <<= INT_BITS
            num += next(generator)
        if num >= too_big:
            continue
        else:
            return num / modulos + min


def randint(min=0, max=10, generator=None):
    return int(round(randfloat(min=min-0.5, max=max+0.49, generator=generator)))


def list_picker (listx):
    """Choose a random item from the given list"""
    length = len(listx) - 1
    choosen = randint(0, length)
    return listx[choosen]


def dice_roll (d=6, n=1, min=1):
    """Roll a set number of dice with a set number of sides"""
    generator = cached_generator()
    if min > d:
        raise Exception("The 'min' argument is larger than the max number of 'd'")
    if n <= 0:
        raise Exception("The 'n' argument must be greater than 0")
    dice = []
    total = 0
    for x in range(0,n):
        z = randint(min,d,generator)
        dice.append(z)
        total += z
    return (dice, total)

def quick_dice (d=6, n=1, min=1):
    """Roll a set number of dice with a set number of sides
    This roll calculates min and max that can be rolled and makes a quick, single request"""
    if min > d:
        raise Exception("The 'min' argument is larger than the max number of 'd'")
    if n <= 0:
        raise Exception("The 'n' argument must be greater than 0")
    return randint(n * min, n * d)



def uint16(array_length=100):
    """Return a numpy array of uint16 numbers"""
    import numpy
    return numpy.array(get_data('uint16', array_length), dtype=numpy.uint16)


def cached_generator(data_type='uint16', cache_size=1024):
    """Returns numbers. Caches numbers to avoid latency."""
    while 1:
        for n in get_data(data_type, cache_size, cache_size):
            yield n


__all__ = ['get_data', 'binary', 'hex', 'uint16', 'cached_generator', 'randfloat', 'randint', 'list_picker', 'dice_roll', 'quick_dice']
