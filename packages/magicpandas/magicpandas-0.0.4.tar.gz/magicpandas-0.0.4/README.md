\#\#\#\#\# UNDER CONSTRUCTION \#\#\#\#\# 

### magicpandas
*magicpandas* makes working with pandas dead simple.

### Main Features
* MagicDataFrame subclasses DataFrame to make existing methods more intuitive as well as add new methods
* MagicDataFrame adds verbose labels that are used by default when displaying data
* MagicDataFrame supports Django ORM  
  * inspectdf uses DataFrame column types to produce a Django model class (cf. [inspectdb](https://docs.djangoproject.com/en/3.0/howto/legacy-databases/#auto-generate-the-models))
  * to_django saves the DataFrame to SQL using Django ORM's [bulk_update](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#bulk-update) and [bulk_create](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#bulk-create).

##### Installation
`pip install magicpandas`

##### Examples
```python
from magicpandas import MagicDataFrame
mdf = MagicDataFrame(df)
mdf2 = mdf.drop('*e', axis=1) # df2 drops all columns ending in "e"
mdf.browse() # opens the DataFrame in MS Excel with nice formatting
mdf.browse(client='webbrowser') # opens the DataFrame as html displayed in Chrome with nice formatting
mdf.graph()  # Opens a graph in Chrome using the excellent Altair library using sensible encodings
mdf.inspect_for_django()  # prints text that corresponds to a Django model definition
```

### Philosophy
* Convention over configuration
* Employs Altair rather than than matplotlib because it's web first and based on 
the [Grammar of Graphics](https://idl.cs.washington.edu/papers/vega-lite/)
* Employs MS Excel for data browsing
* There should be little gap between intention and implementation
