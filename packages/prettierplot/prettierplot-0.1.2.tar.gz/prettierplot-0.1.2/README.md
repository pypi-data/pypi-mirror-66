[![PyPI version](https://badge.fury.io/py/prettierplot.svg)](https://badge.fury.io/py/prettierplot)

# prettierplot

<i>"prettierplot is a Python library that makes it easy to create high-quality, polished data visualizations with minimal code."</i>

## Installation

```
pip install prettierplot
```

## Example(s)

```
from prettierplot.plotter import PrettierPlot
from prettierplot import data
import numpy as np

df = data.attrition()

# capture unique EmployeeField values and frequency counts
unique_vals, unique_counts = np.unique(
    df[df["EducationField"].notnull()]["EducationField"], return_counts=True
)

# create plotting instance
p = PrettierPlot(chart_scale=10)

# create Axes object and decorate
ax = p.make_canvas(title="Educational field category counts", y_label="Category counts", y_shift=0.47)

# add plots
p.bar_v(
    x=unique_vals,
    counts=unique_counts,
    label_rotate=45,
    x_tick_wrap=True
)
```

![ex1](/examples/bar_v.png)

