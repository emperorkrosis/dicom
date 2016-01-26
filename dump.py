import dicom
import os
import sys

# Example usage for dumping all the images from a DICOM directory structure
d = dicom.DirectoryFile(".\\medical\\DICOMDIR")
d.read()

# Reading the directory will store all the image filenames in d.files.
# Iterate over all those files to extract the images themselves.
image_filenames = [".\\medical\\" + f.strip() for f in d.files]
count = 1
for filename in image_filenames:
  print filename
  out_filename = ".\\images\\output" + str(count) + ".bmp"
  print out_filename
  sys.stdout.flush()
  img = dicom.ImageFile(filename, out_filename)
  img.read()
  count = count + 1

# Example of single file debugging for DICOM image files.
#d = dicom.ImageFile(".\\medical\\DICOM\\8428\\8429\\84212", "test2.bmp")
#d = dicom.ImageFile(".\\medical\\DICOM\\846743\\846745\\846766", "test3.bmp")
#d = dicom.ImageFile(".\\medical\\DICOM\\847768\\847771\\847773", "test3.bmp")
#d = dicom.ImageFile(".\\medical\\DICOM\\84527\\84530\\84540", "test4.bmp")
#d.read()

# Example of single file debugging for DICOM debug dumping files.
#d = dicom.DumpFile(".\\medical\\DICOM\\84527\\84534\\845654")
#d.read()
