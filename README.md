# QuantumRand

[![PyPI version](https://badge.fury.io/py/quantumrand.svg)](https://pypi.org/project/quantumrand/) [![PyPI - License](https://img.shields.io/pypi/l/quantumrand)](https://pypi.org/project/quantumrand/) [![Bitcoin](https://img.shields.io/badge/BTC-143TbUxTB9XPqBKu565acFXCHWSdsRLnKK-blue)](https://www.blockchain.com/btc/address/143TbUxTB9XPqBKu565acFXCHWSdsRLnKK)

### maintained fork of [lmacken/quantumrandom](https://github.com/lmacken/quantumrandom)

This project provides tools for interacting with The ANU Quantum Random Number Generator ([qrng.anu.edu.au](http://qrng.anu.edu.au>`)). It communicates with their JSON API and provides a `qrand` command-line tool, a Python API, ~~and a Linux `/dev/qrand` character device.~~ (This has to be fixed. Python 2 has reached EOL and the original repo did not support a Python 3 version of this feature).

QuantumRand was made to work with Python 3. Python 2 support has been dropped as it is now reached End of Life.

> As of 2.0, QuantumRand has had to adapt to ANU's SSL certificate expiring. QuantumRand is still able to connect via SSL by default, but please be aware that QuantumRand cannot securely validate ANU's SSL authenticity until they update their certificate.

## Installation

`pip install quantumrand`

## Python API

### Low Level API

The QuantumRand Python module contains a low-level `get_data`
function, which is modelled after the ANU Quantum Random Number
Generator's JSON API. It returns variable-length lists of either
`uint16` or `hex16` data.

Valid `data_type` values are `uint16` and `hex16`.

The `array_length` and `block_size` cannot be larger than `1024`.

If for some reason the API call is not successful, or the incorrect amount of data is returned from the server, this function will raise an exception.

* `quantumrand.get_data()`

```
[26646]
```

* `quantumrand.get_data(data_type='uint16', array_length=5)`

```
[42796, 32457, 9242, 11316, 21078]
```

* `quantumrand.get_data(data_type='hex16', array_length=5, block_size=2)`

```
['f1d5', '0eb3', '1119', '7cfd', '64ce']
```

### High Level API

Based on the above `get_data` function, quantumrand also provides a bunch
of higher-level helper functions that make easy to perform a variety of
tasks.

* `quantumrand.randint(0, 20)`

```
5
```

* `quantumrand.hex()[:10]`

```
'8272613343'
```

* `quantumrand.binary()[0]`

```
'\xa5'
```

* `len(quantumrand.binary())`

```
10000
```

* `quantumrand.uint16()`

```
numpy.array([24094, 13944, 22109, 22908, 34878, 33797, 47221, 21485, 37930, ...], dtype=numpy.uint16)
```

* `quantumrand.uint16().data[:10]`

```
'\x87\x7fY.\xcc\xab\xea\r\x1c`'
```


## Using the Command Line Tool

Getting a random integer within a range:

* `qrand --int --min 5 --max 15`

```
7
```

Getting random binary values:

* `qrand --binary`

```
���I�%��e(�1��c��Ee�4�������j�Կ��=�^H�c�u
oq��G��Z�^���fK�0_��h��s�b��AE=�rR~���(�^Q�)4��{c�������X{f��a�Bk�N%#W
+a�a̙�IB�,S�!ꀔd�2H~�X�Z����R��.f
```

Getting random hex values:

* `qrand --hex`

```
1dc59fde43b5045120453186d45653dd455bd8e6fc7d8c591f0018fa9261ab2835eb210e8
e267cf35a54c02ce2a93b3ec448c4c7aa84fdedb61c7b0d87c9e7acf8e9fdadc8d68bcaa5a
```

## Creating /dev/qrand

This will have to be updated, as it is not working for any supported version of Python currently.