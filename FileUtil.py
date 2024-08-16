#
# F i l e U t i l . p y
#

# This file is for general utility functions involving file manipulation.

import re

class NewEndWritter:
  def __init__(self, fileName):
    self.fileName = fileName
    self.endPattern = re.compile(r"^#+\s*generated code beyond this point\s*#+$")
    self.file = None  # Initialize file object

  def __enter__(self):
    try:
      # open file for read and write
      self.file = open(self.fileName, "r+")

      # Find the magic line (if present)
      keepLen = 0
      numKeepLine = 0
      majicLineFound = False

      for line in self.file:
        keepLen += len(line)
        numKeepLine += 1

        if self.endPattern.match(line):
          majicLineFound = True
          break

      ####  in Windows every line with a \n will have an extra character (\n\r) in the file  ####

      # if the last kept line doesn't end with a \n (it is the last line of the file), add a \n
      if 0 < numKeepLine:
        if line[len(line) - 1] != '\n':
          self.file.seek(keepLen + numKeepLine - 1)
          self.file.write('\n')

        filePos = keepLen + numKeepLine

        # truncate beyond the file position
        self.file.seek(filePos)
        self.file.truncate()

      # if magic line was not found, add one
      if (numKeepLine == 0) or not majicLineFound:
        self.file.write("##  generated code beyond this point  ##\n")

    except FileNotFoundError:
      # Create an empty file if it doesn't exist
      self.file = open(self.fileName, "w")

    # Return the file object for use in the 'with' block
    return self.file

  def __exit__(self, exc_type, exc_value, traceback):
    # Ensure the file is closed properly, regardless of errors
    if self.file:
      self.file.close()
