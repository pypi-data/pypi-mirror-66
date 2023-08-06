# PYMLTUILS

### About
This repository provides various functions useful for python and machine learning. The goal is to keep your code cleaner, keeping business logic out of your primary functions. For example, formatting paths is common, can often turn into many lines of code, and is done frequently throughout a script. Often people do the path formatting multiple times, mid-function, convoluting the code and distracting from the functions purpose. Further, paths aren't always formatted consistently and error handling is poor. Thus, I created the following function to format all paths consistently:

```python
def format_path(path):
  """ Format paths into a consistent format. Expand user paths.
      Relative paths are converted to full paths. Directories 
      should all end in forward slashes. Note this will format even if
      the paths don't actually exist yet.
  Args:
    path: Full or relative path of directory or file in question.
  Returns:
    Formatted full paths, relative to 
  """
  # If path is None (e.g. when no --arg from parser), default to same dir as the script
  if path is None:
    path = ""

  # Expand paths
  path = os.path.expanduser(path)

  # Handle relative paths
  path = os.path.abspath(path)

  # Check if path *could be* a valid file or dir 
  # Note, files like MAKE or LICENCE that don't actually exist
  # will be considered as dirs.
  is_dir = os.path.isdir(path) or is_dir_like(path) and not os.path.isfile(path)

  # Make sure dirs end with a slash
  if is_dir and not path.endswith('/'):
    path += "/"

  return path  
```

This function can take relative or full paths to files or directories. It ensures that empty paths and paths that are type None are handled, paths are expanded, and that directories end with a trailing slash. Using this function removes clutter from your other functions and ensures that paths are formatted consistently, resulting in cleaner, more robust code.

### How to Install
`pip install pymlutils`

### How to Use
In your script, import `pymlutils`. Some example usage:

```python
import pymlutils.pymlutils as pyml

formatted_path = pyml.format_path(path)
```

```python
from pymlutils.pymlutils import *

formatted_path = format_path(path)
```

```python
import pymlutils.yolo as yolo

label_list = yolo.read_label(path)
```

```python
from pymlutils.yolo import *

label_list = read_label(path)
```
