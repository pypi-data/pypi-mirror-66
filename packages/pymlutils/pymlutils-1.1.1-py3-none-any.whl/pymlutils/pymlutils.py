import os
import re
import json
import sys
from collections import Mapping

### PATHS (FILE & DIR) ###
def check_path(path):
  """ Kill script if file or dir doesn't exist.
  Args:
    path: Full path of file or dir in question.
  Return:
    True if path is ok.
  """
  if not os.path.isfile(path) and not os.path.isdir(path):
    print(f"The file {path} does not exist.")
    sys.exit(1)
  else:
    return True

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


### DIRECTORIES ###
def check_dir(path):
  """ Kill script if dir doesn't exist
  Args:
    path: Full path of dir in question.
  Return:
    True if dir is ok.
  """
  if not os.path.isdir(path):
    print(f"The dir {path} does not exist.")
    sys.exit(1)
  else:
    return True

def check_or_mk_dir(path):
  """ Create directories recursively at specified path if it doesn't exist.
  Args:
    path: Full path of directory in question.
  Return True if dir exists and False if it doesn't.
  """
  if not os.path.isdir(path):
    os.makedirs(path, exist_ok=True)
    print(f"{path} doesn't exist. Creating...\n")
    return False
  else:
    return True

def is_dir_like(path):
  """ Check if full path is "dir-like," that is, *could* be a valid dir. 
      The dir doesn't actually have to exist.
  Args:
    path: Theoretical full path to a dir.
  Returns:
    Formatted True for strings with are dir-like and False for those
    that aren't.
  """
  return len(os.path.basename(path).split('.')) == 1


### FILES ###
def check_file(path):
  """ Kill script if file doesn't exist.
  Args:
    path: Full path of file in question.
  Return:
    True if file exists.
  """
  if not os.path.isfile(path):
    print(f"The file {path} does not exist.")
    sys.exit(1)
  else:
    return True

def get_file_list_from_dir_or_file(path, file_format, full_path=True, should_print=True, is_empty_ok=False):
  """ Get a list of full paths to all files in provided path.
  Args:
    path: Full path to directory or a file with a list of full paths to other files.
    file_format: The format of the files (typically jpg, png, or txt)
  Returns:
    A python list of files of specified file_format (full paths by default)
  """
  file_list = []

  # Check if output files should contain the full path or just the filename.
  if full_path:
    optional_path = path
  else:
    optional_path = ""

  # If provided path is a dir, add all matching files to file_list
  if os.path.isdir(path):
    for file in os.listdir(path):
      if (file.endswith(file_format)):
        file_list.append(optional_path + file)

  # If provided path is a file, add all paths in the file to
  # file_list first verifying that the file actually exists
  elif os.path.isfile(path):
    file = open(path, 'r')

    for file_path in file:
      file_path = file_path.rstrip('\n')

      # Add files which are the correct format and exist
      if (file_path.endswith(file_format) and os.path.isfile(file_path)):
        file_list.append(file_path)
    file.close()
  else:
    print(f"{path} is not a file or directory.")
    sys.exit(1)

  # Check results
  num_files = len(file_list)

  # Kill if there are no files, unless is_empty_ok is set to True
  if num_files == 0 and not is_empty_ok:
    print(f"No files of format {file_format} found at {path}")
    sys.exit(1)
  else:
    print(f"{num_files} files of format {file_format} were found.")
    return file_list

def get_num_lines_from_file(path):
  """ Get the number of lines in a file.
  Args:
    path: Full path of file in question.
  return:
    Number of lines in the file.
  """
  if os.stat(path).st_size == 0:
    return 0
  else:
    with open(path) as file:
      for i, line in enumerate(file):
        pass
    return i + 1

def is_file_like(path):
  """ Check if full path is "file-like," that is, *could* be a 
      valid file path. The file doesn't actually have to exist. 
      Note: files with no extension (e.g. .txt) and that don't 
      actually exist will not be considered to be valid file names 
      as there is no way to distiguist them from a directory 
      (e.g. a LICENCE or MAKE file).
  Args:
    path: Theoretical full or relative path to a file.
  Returns:
    Formatted True for strings with are file-like and False for those
    that aren't.
  """
  return len(os.path.basename(path).split('.')) == 2

def rm_file(path, should_print=True):
  """ Delete the file if it exists.
  Args:
    Full path to file in question.
  return:
    True if deleted, False of not
  """
  if os.path.isfile(path):
    os.remove(path)
    if should_print: print(f"{path} was deleted.")
    return True
  else:
    return False

def write_list_to_file(path, list_, mode='w+'):
  """ Write the list to the file at specified full path.
      Create the file if it doesn't exist.
  Args:
    path: Full path of dir in question.
    list: The Python list to be written item by item.
    mode: The mode of writing.
  Return:
    True on completion.
  """
  file = open(path, mode)

  for line in list_:
    file.write(f"{line}\n")

  file.close()
  return True


### JSON ###
def remove_comments(json_like):
  """
  Removes C-style comments from *json_like* and returns the result.  Example::
      >>> test_json = '''\
      {
          "foo": "bar", // This is a single-line comment
          "baz": "blah" /* Multi-line
          Comment */
      }'''
      >>> remove_comments('{"foo":"bar","baz":"blah",}')
      '{\n    "foo":"bar",\n    "baz":"blah"\n}'
  """
  comments_re = re.compile(
      r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
      re.DOTALL | re.MULTILINE
  )
  def replacer(match):
      s = match.group(0)
      if s[0] == '/': return ""
      return s
  return comments_re.sub(replacer, json_like)

def remove_trailing_commas(json_like):
  """
  Removes trailing commas from *json_like* and returns the result.  Example::
      >>> remove_trailing_commas('{"foo":"bar","baz":["blah",],}')
      '{"foo":"bar","baz":["blah"]}'
  """
  trailing_object_commas_re = re.compile(
      r'(,)\s*}(?=([^"\\]*(\\.|"([^"\\]*\\.)*[^"\\]*"))*[^"]*$)')
  trailing_array_commas_re = re.compile(
      r'(,)\s*\](?=([^"\\]*(\\.|"([^"\\]*\\.)*[^"\\]*"))*[^"]*$)')
  # Fix objects {} first
  objects_fixed = trailing_object_commas_re.sub("}", json_like)
  # Now fix arrays/lists [] and return the result
  return trailing_array_commas_re.sub("]", objects_fixed)


### JSON CONFIG FILES ###
def check_json_config(path):
  """ Get the full path of the json config file. Format the path if provided.
  Args:
    path: Either None or a user-specified path. 
  Returns:
    The formatted, full path to the json config file.
  """

  # If --config wasn't specified, default to same dir as the script
  # and file name the same as the script name + .json
  if path is None:
    config_dir = os.path.dirname(os.path.realpath(sys.argv[0])) + "/"
    config_file = os.path.splitext(os.path.basename(sys.argv[0]))[0] + ".json"
    config_path = config_dir + config_file
  # User provided a path, so format it
  else:
    config_path = format_path(path)

  # Make sure the file exists
  if not os.path.isfile(config_path):
    print(f"The json config file {config_path} does not exist.")
    sys.exit(1)

  return config_path

def get_args_from_json_config(path):
  """ Read the json config file, converting all arguments into a
      python dict.
  Args:
    path: Full path to the json config file.
  Returns:
    A python dict containing all config args as a python dict.
  """

  # Read in json config file
  try:
    with open(path) as f_json:
      json_string = ""

      for line in f_json:
        json_string += line
  except Exception as e:
    print(f"Error reading {path}.")
    print(f"Error: {e}")
    sys.exit(1)
  finally:
    f_json.close()

  # Remove comments if they exist (json doesn't support comments)
  json_no_comments = remove_comments(json_string)

  # Remove trailing commas if they exist 
  proper_json_string = remove_trailing_commas(json_no_comments)

  # Load formatted json into an object
  args = json.loads(proper_json_string)

  return args


### GENERAL PYTHON ###
def camelize(str_or_iter):
  """Convert a string, dict, or list of dicts to camel case.
  param str_or_iter:
    A string or iterable.
  type str_or_iter: Union[list, dict, str]
  rtype: Union[list, dict, str]
  returns:
    camelized string, dictionary, or list of dictionaries.
  """
  underscore_re = re.compile(r'([^\-_\s])[\-_\s]+([^\-_\s])')

  if isinstance(str_or_iter, (list, Mapping)):
      return _process_keys(str_or_iter, camelize)

  s = str(str_or_iter)
  if s.isnumeric():
      return str_or_iter

  if s.isupper():
      return str_or_iter

  return ''.join([
      s[0].lower() if not s[:2].isupper() else s[0],
      underscore_re.sub(lambda m: m.group(1) + m.group(2).upper(), s[1:]),
  ])

def pascalize(str_or_iter):
  """Convert a string, dict, or list of dicts to pascal case.
    param str_or_iter: A string or iterable.
    type str_or_iter: Union[list, dict, str]
    rtype: Union[list, dict, str]
    returns:
    pascalized string, dictionary, or list of dictionaries.
  """
  pascal_re = re.compile(r'([^\-_\s]+)')

  if isinstance(str_or_iter, (list, Mapping)):
      return _process_keys(str_or_iter, pascalize)

  s = str(str_or_iter)
  if s.isnumeric():
      return str_or_iter

  if s.isupper():
      return str_or_iter

  s = camelize(
      pascal_re.sub(lambda m: m.group(1)[0].upper() + m.group(1)[1:], s),
  )
  return s[0].upper() + s[1:]


### MACHINE LEARNING ###
def path_to_txt(path):
  directory = os.path.dirname(path)
  filename = os.path.basename(path).split('.')[0]
  return directory + "/" + filename + ".txt"






