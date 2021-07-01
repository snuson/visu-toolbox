## Visualization toolbox

This library gives the tools to easily visualize scatter/line graphs, 
bar plots and pie charts.

### How-to
Requires only pyQt5.

Example calls:
```python
from core import *

# data is the only mandatory parameter
# either from file or from two lists
# Legends must contain correct amount of strings.
# Test/example data shows how to format data.
# e.g.
scatterplot(src='path\data.csv', title='title',
            xlab='X axis', ylab='Y axis', 
            legends=['line1', 'line2', 'line3'])
# optional parameters with their default values are:
# grid=True, points=True,
# lines=True, axis=True, xlab='', 
# ylab='', title='My Plot',
# legends=None, ngridx=4, ngridy=2


# e.g.
barplot(src='path\data.csv', ngridy=3)
# optional parameters with their default values are:
# grid=True, axis=True, xlab='', 
# ylab='', title='My Plot', ngridy=2

# e.g.
pieplot(src='path\data.csv')
# only optional parameter with its default value is is:
# title='My Plot' 

```


### Other
Data format is critical in order for this library to work but 
the example data should give a good idea as to how it should look.
Pics folder gives an idea of what the plots look like.


