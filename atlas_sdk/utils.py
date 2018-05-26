import os, base64

def svgs_to_data_uri(files):
  """Converts given files to base64 data uri and make a dictionary where
  keys are filenames.

  :param files: Files to read
  :type files: list
  :rtype: dict

  """

  files = [files] if type(files) is not list else files

  result = {}

  for path in files:
    with open(path, mode='rb') as f:
      name, _ = os.path.splitext(os.path.basename(path))

      result[name] = 'data:image/svg+xml;base64,' + base64.b64encode(f.read()).decode()

  return result