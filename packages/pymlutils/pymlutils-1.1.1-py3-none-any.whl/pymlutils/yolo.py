import os
from .pymlutils import *

### YOLO ###
def get_classes_from_label(path):
  """ Get all classes from a yolo label file.
  Args:
    path: Full path to the image (not label).
  Returns:
    A Python list containing all ids (int) of classes.
  """
  # Change file extension to .txt
  path = path_to_txt(path)

  # Read classes to list
  classes = []

  with open(path) as file:
    for line in file:
      class_ = line.split()[0]
      classes.append(class_)
  return classes

def get_bboxes_from_label(path):
  """ Get all bboxes from a yolo label file.
  Args:
    path: Full path to the image (not label).
  Returns:
    A Python list of bboxes for the provided path in format:
    [center_x, center_y, width, height], all as floats.
  """
  # Change file extension to .txt
  path = path_to_txt(path)

  # Read bboxes to list
  bboxes = []

  with open(path) as file:
    for line in file:
      bbox = line.strip().split()[1:]

      # Convert strings to floats
      for i, coord in enumerate(bbox):
        bbox[i] = float(coord)

      bboxes.append(bbox)
  return bboxes

def read_label(path):
  """ Read yolo label file into list line by line.
  Args:
    path: Full path to the image (not label).
  Returns:
    A Python list of class and bboxes for the provided path 
    in format: [class, center_x, center_y, width, height].
  """
  # Change file extension to .txt
  path = path_to_txt(path)

  # Read labels to list
  detections = []

  with open(path) as file:
    for line in file:
      # Add the class as an int
      list_ = [int(line.split()[0])]

      # Convert bbox to floats
      for coord in line.strip().split()[1:]:
        list_.append(float(coord))

      detections.append(list_)
  return detections  

def write_label(path, labels, mode='w+', precision=6):
  """ Write the list to the file at specified full path.
      Create the file if it doesn't exist.
  Args:
    path: Full path to label file.
    bbox_list: List of yolo bboxes to be written in format:
               [class, center_x, center_y, width, height]
    mode: The mode of writing.
    precision: How many decimal places to keep for bbox.
  Return:
    True on completion.
  """
  file = open(path, mode)

  # Write all lines to file
  for label in labels:
    # Line to be written to file
    line = ""

    for item in label:
      line += str(round(item, precision)) + " "

    line = line.strip()
    file.write(f"{line}\n")

  file.close()
  return True

def check_bbox(bbox_yolo):
  """ Check if bounding boxes extend beyond the image bounds.
  Args:
    bbox_yolo: A list containing a bbox in Yolo format 
               [center_x, center_y, width, height]. Recall that 
               in Yolo coords, the origin is the upper left,
               not the upper right, so the y-axis is inverted.
  Return:
    A boolean value of True if valid and false if invalid.
  """
  x_min = bbox_yolo[0] - bbox_yolo[2]/2
  x_max = bbox_yolo[0] + bbox_yolo[2]/2
  y_max = bbox_yolo[1] + bbox_yolo[3]/2
  y_min = bbox_yolo[1] - bbox_yolo[3]/2

  if((x_min < 0.0) or (x_max > 1.0) or (y_min < 0.0) or (y_max > 1.0)):
    print(f"The following bbox is out of bounds:")
    print(f"bbox_yolo = {bbox_yolo}")
    return False
  else:
    return True