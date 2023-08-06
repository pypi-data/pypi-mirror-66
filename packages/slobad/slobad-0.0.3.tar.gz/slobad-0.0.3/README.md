# slobad

Caching of pandas DataFrames.


## Setup

```
pip install slobad
```

Requires `pandas` and `pyarrow`.


## Usage


Create a `Slobad` object that has a `create` method. The `create` method must
return a non-empty `pandas` `DataFrame`.

```python
import pandas as pd
from slobad import Slobad

class CreateData(Slobad):
    #each Slobad class requires a create method
    def create(self):
        data = [[0] * 10] * (10 ** 6)
        cols = [f'{i}' for i in range(10)]
        df = pd.DataFrame(data, columns=cols)
        return df
```

Execute the built-in `run` method which calls `create` internally.

```python
>>> df = CreateData().run()
```
```
Running CreateData...
Execute create finished in 1.26s.
Write to cache finished in 0.09s.
Load from cache finished in 0.03s.
```

The second time `run` is executed for the identitical object, the DataFrame
is loaded from the cache.

```python
>>> cached = CreateData().run()
```
```
Running CreateData...
Load from cache finished in 0.03s.
```
```python
>>> df.equals(cached)
True
```

See the examples folder for more.
