# PY BASE MODEL

[![codecov](https://codecov.io/gh/guionardo/py-base-model/branch/develop/graph/badge.svg)](https://codecov.io/gh/guionardo/py-base-model)

Model data validator

## Examples

### Model with primitive type attributes

``` Python
from base_model.base_model import BaseModel

class PrimitiveFieldsModel(BaseModel):
    id: int
    name: str
    active: bool
    size: float
```

### Model with time type attributes

``` Python
from datetime import datetime, date, time

from base_model.base_model import BaseModel


class TimeFieldsModel(BaseModel):
    birthday: date
    register: datetime
    alarm: time

```

### Model with list type attributes

``` Python
from typing import List

from base_model.base_model import BaseModel


class ListFieldsModel(BaseModel):
    names: List[str]
    ages: List[int]
    enables: List[bool]
```

