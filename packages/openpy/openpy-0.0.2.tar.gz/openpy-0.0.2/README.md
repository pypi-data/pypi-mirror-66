# openpy

author: Oren Ovadia

## Overview

Just open files, local filesystem, s3 or online.
Decompresses any format automatically (currently only `gzip` is supported😀)

## Installation
```
pip install openpy
```

or: 

```
pip install git+git://github.com/orenovadia/openpy.git#egg=master
```

## Examples
```python
from openpy import read

# local files, uncompressed:
with read('data.gz') as f:
    print(f.read())

# s3:
with read('s3://bucket/path/to/file.gz') as f:
    print(f.read())
 
```

## Upload to pypi:
```
./publish.sh
```