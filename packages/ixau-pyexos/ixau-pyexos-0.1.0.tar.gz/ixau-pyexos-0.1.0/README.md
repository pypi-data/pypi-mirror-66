# pyexos

pyexos is a config manipulation utility for Extreme Networks devices, which enables the theory of config merge and replace.

##### Installation
```sh
$ pip install -e git+https://github.com/ixaustralia/pyexos#egg=pyexos
```

##### Usage
```python
from pyexos import EXOS
device = EXOS(ip='10.0.0.1', username='dev', password='dev')
device.get_running_config()
```