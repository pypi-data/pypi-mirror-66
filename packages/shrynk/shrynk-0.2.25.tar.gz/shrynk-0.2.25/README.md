<p align="center">
  <img src="./Shrynk.png" width="400rem"/>
</p>

[![Build Status](https://travis-ci.org/kootenpv/shrynk.svg?branch=master)](https://travis-ci.org/kootenpv/shrynk)
[![PyPI](https://img.shields.io/pypi/pyversions/shrynk.svg?style=flat-square&logo=python)](https://pypi.python.org/pypi/shrynk/)
[![PyPI](https://img.shields.io/pypi/v/shrynk.svg?style=flat-square&logo=pypi)](https://pypi.python.org/pypi/shrynk/)
[![HitCount](http://hits.dwyl.io/kootenpv/shrynk.svg)](http://hits.dwyl.io/kootenpv/shrynk)

You can read the [introductory blog post](https://vks.ai/2019-12-05-shrynk-using-machine-learning-to-learn-how-to-compress) or try it live at https://shrynk.ai

### Features

- ✓ Compress your data smartly based on **Machine Learning**
- ✓ Takes **User Requirements** in the form of weights for `size`, `write_time` and `read_time`
- ✓ Trains & caches a model based on **compression methods available** in the system, using packaged data
- ✓ **CLI** for compressing and decompressing
- ✓ Works with `CSV`, `JSON` and `Bytes` in general

### CLI

    shrynk compress myfile.json       # will yield e.g. myfile.json.gz or myfile.json.bz2
    shrynk decompress myfile.json.gz  # will yield myfile.json

    shrynk compress myfile.csv --size 0 --write 1 --read 0

    shrynk benchmark myfile.csv                  # shows benchmark results
    shrynk benchmark --predict myfile.csv        # will also show the current prediction
    shrynk benchmark --save --predict myfile.csv # will add the result to the training data too

### Usage

Installation:

    pip install shrynk

Then in Python:

```python
import pandas as pd
from shrynk import save, load

# save dataframe compressed
my_df = pd.DataFrame({"a": [1]})
file_path = save(my_df, "mypath.csv")
# e.g. mypath.csv.bz2

# load compressed file
loaded_df = load(file_path)
```

If you just want the prediction, you can also:

```python
import pandas as pd
from shrynk import infer

infer(pd.DataFrame({"a": [1]}))
# {"engine": "csv", "compression": "bz2"}
```

### Add your own data

If you want more control you can do the following:

```python
import pandas as pd
from shrynk import PandasCompressor

df = pd.DataFrame({"a": [1, 2, 3]})

pdc = PandasCompressor("default")
pdc.run_benchmarks(df) # adds data to the default

pdc.train_model(size=3, write=1, read=1)

pdc.predict(df)
```
