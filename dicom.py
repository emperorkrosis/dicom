import math
import struct
from collections import defaultdict



""" Base class for Dicom Files """
class File(object):
  """ Table of Tag Names for the DICOM Format. """
  TAG_NAMES = {
    (0x0002, 0x0000): "File Metadata Group Length",
    (0x0002, 0x0001): "File metadata Information Version",
    (0x0002, 0x0002): "Media Storage SOP Class UID",
    (0x0002, 0x0003): "Media Storage SOP Instance UID",
    (0x0002, 0x0010): "Transfer Syntax UID",
    (0x0002, 0x0012): "Implementation Class UID",
    (0x0002, 0x0013): "Implementation Version Name",
    (0x0002, 0x0016): "Source Application Entity Title",
    (0x0004, 0x1130): "File Set ID",
    (0x0004, 0x1200): "Offset of First Record of Root",
    (0x0004, 0x1202): "Offset of Last Record of Root",
    (0x0004, 0x1212): "File-set Consistency Flag",
    (0x0004, 0x1220): "Directory Record Sequence",
    (0x0004, 0x1400): "Offset of next Dir Record in Dir Entry",
    (0x0004, 0x1410): "Record In-Use Flag",
    (0x0004, 0x1420): "Offset of Referenced Lower Level Dir Entity",
    (0x0004, 0x1430): "Directory Record Type",
    (0x0004, 0x1500): "Referenced File ID",
    (0x0004, 0x1510): "Referenced SOP Class UID in File",
    (0x0004, 0x1511): "Referenced SOP Instance UID in File",
    (0x0004, 0x1512): "Referenced Transfer Syntax UID in File",
    (0x0008, 0x0005): "Specific Character Set",
    (0x0008, 0x0008): "Image Type",
    (0x0008, 0x0012): "Instance Creation Date",
    (0x0008, 0x0013): "Instance Creation Time",
    (0x0008, 0x0016): "SOP Class UID",
    (0x0008, 0x0018): "SOP Instance UID",
    (0x0008, 0x0020): "Study Date",
    (0x0008, 0x0021): "Series Date",
    (0x0008, 0x0022): "Acquisition Date",
    (0x0008, 0x0023): "Content Date",
    (0x0008, 0x0030): "Study Time",
    (0x0008, 0x0031): "Series Time",
    (0x0008, 0x0032): "Acquisition Time",
    (0x0008, 0x0033): "Content Time",
    (0x0008, 0x0050): "Accession Number",
    (0x0008, 0x0060): "Modality",
    (0x0008, 0x0068): "Presentation Intent Type",
    (0x0008, 0x0070): "Manufacturer",
    (0x0008, 0x0080): "Institution Name",
    (0x0008, 0x0090): "Referring Physicians Name",
    (0x0008, 0x0100): "Code Value",
    (0x0008, 0x0102): "Code Scheme Designator",
    (0x0008, 0x0103): "Code Scheme Version",
    (0x0008, 0x0104): "Code Meaning",
    (0x0008, 0x1010): "Extended Code Value",
    (0x0008, 0x1030): "Study Description",
    (0x0008, 0x1032): "Procedure Code Sequence",
    (0x0008, 0x103e): "Series Description",
    (0x0008, 0x1040): "Institutional Dept Name",
    (0x0008, 0x1050): "Performing Physician Id Seq",
    (0x0008, 0x1060): "Name of Physician Reading Study",
    (0x0008, 0x1070): "Operators Name",
    (0x0008, 0x1090): "Manufacturers Model Name",
    (0x0008, 0x1110): "Referenced Study Sequence",
    (0x0008, 0x1111): "Referenced Performed Procedure Step Seq",
    (0x0008, 0x1120): "Referenced Patient Sequence",
    (0x0008, 0x1140): "Referenced Image Sequence",
    (0x0008, 0x1150): "Referenced SOP Class UID",
    (0x0008, 0x1155): "Referenced SOP Instance UID",
    (0x0008, 0x2111): "Derivation Description",
    (0x0008, 0x2112): "Source Image Sequence",
    (0x0008, 0x2218): "Anatomic Region Sequence",
    (0x0008, 0x3010): "Irradiation Event UID",
    (0x0009, 0x0010): "Vendor Specific (0009,0010)",
    (0x0009, 0x0011): "Vendor Specific (0009,0011)",
    (0x0009, 0x1001): "Vendor Specific (0009,1001)",
    (0x0009, 0x1002): "Vendor Specific (0009,1002)",
    (0x0009, 0x1004): "Vendor Specific (0009,1004)",
    (0x0009, 0x1005): "Vendor Specific (0009,1005)",
    (0x0009, 0x1006): "Vendor Specific (0009,1006)",
    (0x0009, 0x1008): "Vendor Specific (0009,1008)",
    (0x0009, 0x1009): "Vendor Specific (0009,1009)",
    (0x0009, 0x100c): "Vendor Specific (0009,100c)",
    (0x0009, 0x1010): "Vendor Specific (0009,1010)",
    (0x0009, 0x1027): "Vendor Specific (0009,1027)",
    (0x0009, 0x1080): "Vendor Specific (0009,1080)",
    (0x0009, 0x1090): "Vendor Specific (0009,1090)",
    (0x0009, 0x10e3): "Vendor Specific (0009,10e3)",
    (0x0009, 0x10f0): "Vendor Specific (0009,10f0)",
    (0x0009, 0x10f1): "Vendor Specific (0009,10f1)",
    (0x0009, 0x10f2): "Vendor Specific (0009,10f2)",
    (0x0009, 0x10f3): "Vendor Specific (0009,10f3)",
    (0x0009, 0x10f4): "Vendor Specific (0009,10f4)",
    (0x0010, 0x0010): "Patients Name",
    (0x0010, 0x0020): "Patients Id",
    (0x0010, 0x0021): "Issuer of Patient ID",
    (0x0010, 0x0030): "Patients Birth Date",
    (0x0010, 0x0040): "Patients Sex",
    (0x0010, 0x1000): "Other Patient IDs",
    (0x0010, 0x1010): "Patients Age",
    (0x0010, 0x1020): "Patients Size",
    (0x0010, 0x1030): "Patients Weight",
    (0x0010, 0x1040): "Patients Address",
    (0x0010, 0x21b0): "Additional Patient History",
    (0x0018, 0x0010): "Contrast Agent",
    (0x0018, 0x0015): "Body Part Examined",
    (0x0018, 0x0022): "Scan Options",
    (0x0018, 0x0050): "Slice Thickness",
    (0x0018, 0x0060): "KVP",
    (0x0018, 0x0088): "Spacing Between Slices",
    (0x0018, 0x0090): "Data Collection Diameter",
    (0x0018, 0x1000): "Device Serial Number",
    (0x0018, 0x1004): "Plate ID",
    (0x0018, 0x1016): "Secondary Capture Device Manufacturer",
    (0x0018, 0x1018): "Secondary Capture Device Model Name",
    (0x0018, 0x1019): "Hardcopy Device Manufacturer",
    (0x0018, 0x1020): "Software Versions",
    (0x0018, 0x1030): "Protocol Name",
    (0x0018, 0x1050): "Spatial Resolution",
    (0x0018, 0x1100): "Reconstruction Diameter",
    (0x0018, 0x1110): "Distance Source to Detector",
    (0x0018, 0x1111): "Distance Source to Patient",
    (0x0018, 0x1120): "Gantry Tilt",
    (0x0018, 0x1121): "Gantry Slew",
    (0x0018, 0x1130): "Table Height",
    (0x0018, 0x1140): "Rotation Direction",
    (0x0018, 0x1147): "Field of View Shape",
    (0x0018, 0x1150): "Exposure Time",
    (0x0018, 0x1151): "X-Ray Tube Current",
    (0x0018, 0x1152): "Exposure",
    (0x0018, 0x1155): "Radiation Setting",
    (0x0018, 0x115a): "Radiation Mode",
    (0x0018, 0x115e): "Image and Fluoroscopy Area Dose Product",
    (0x0018, 0x1160): "Filter Type",
    (0x0018, 0x1161): "Type of Filters",
    (0x0018, 0x1164): "Imager Pixel Spacing",
    (0x0018, 0x1166): "Grid",
    (0x0018, 0x1170): "Generator Power",
    (0x0018, 0x1180): "Collimator Name",
    (0x0018, 0x1190): "Focal Spots",
    (0x0018, 0x1200): "Date of Calibration",
    (0x0018, 0x1201): "Time of Calibration",
    (0x0018, 0x1210): "Convolution Kernel",
    (0x0018, 0x1400): "Acquisition Device Processing Description",
    (0x0018, 0x1401): "Acquisition Device Processing Code",
    (0x0018, 0x1411): "Exposure Index",
    (0x0018, 0x1412): "Target Exposure Index",
    (0x0018, 0x1413): "Deviation Index",
    (0x0018, 0x1508): "Positioner Type",
    (0x0018, 0x1510): "Positioner Primary Angle",
    (0x0018, 0x1511): "Positioner Secondary Angle",
    (0x0018, 0x1700): "Collimator Shape",
    (0x0018, 0x1720): "Vertices of Polygonal Collimator",
    (0x0018, 0x5100): "Patient Position",
    (0x0018, 0x5101): "View Position",
    (0x0018, 0x6000): "Sensitivity",
    (0x0018, 0x7004): "Detector Type",
    (0x0018, 0x7005): "Detector Configuration",
    (0x0018, 0x7006): "Detector Description",
    (0x0018, 0x700a): "Detector ID",
    (0x0018, 0x7030): "Field of View Origin",
    (0x0018, 0x7032): "Field of View Rotation",
    (0x0018, 0x7034): "Field of View Horiz Flip",
    (0x0018, 0x7060): "Exposure Control Mode",
    (0x0018, 0x7062): "Exposure Control Mode Description",
    (0x0018, 0x8151): "X-Ray Tube Current in uA",
    (0x0018, 0x9305): "Tag Thickness",
    (0x0018, 0x9306): "Single Collimation Width",
    (0x0018, 0x9307): "Total Collimation Width",
    (0x0018, 0x9309): "Table Speed",
    (0x0018, 0x9310): "Table Feed per Rotation",
    (0x0018, 0x9311): "Spiral Pitch Factor",
    (0x0018, 0xa001): "Contributing Equipment Sequence",
    (0x0019, 0x0010): "Vendor Specific (0019,0010)",
    (0x0019, 0x0016): "Vendor Specific (0019,0016)",
    (0x0019, 0x1002): "Vendor Specific (0019,1002)",
    (0x0019, 0x1003): "Vendor Specific (0019,1003)",
    (0x0019, 0x1004): "Vendor Specific (0019,1004)",
    (0x0019, 0x100f): "Vendor Specific (0019,100f)",
    (0x0019, 0x1011): "Vendor Specific (0019,1011)",
    (0x0019, 0x1015): "Vendor Specific (0019,1015)",
    (0x0019, 0x1018): "Vendor Specific (0019,1018)",
    (0x0019, 0x101a): "Vendor Specific (0019,101a)",
    (0x0019, 0x1023): "Vendor Specific (0019,1023)",
    (0x0019, 0x1024): "Vendor Specific (0019,1024)",
    (0x0019, 0x1025): "Vendor Specific (0019,1025)",
    (0x0019, 0x1026): "Vendor Specific (0019,1026)",
    (0x0019, 0x1027): "Vendor Specific (0019,1027)",
    (0x0019, 0x102c): "Vendor Specific (0019,102c)",
    (0x0019, 0x102e): "Vendor Specific (0019,102e)",
    (0x0019, 0x102f): "Vendor Specific (0019,102f)",
    (0x0019, 0x1032): "Vendor Specific (0019,1032)",
    (0x0019, 0x1039): "Vendor Specific (0019,1039)",
    (0x0019, 0x1040): "Vendor Specific (0019,1040)",
    (0x0019, 0x1042): "Vendor Specific (0019,1042)",
    (0x0019, 0x1043): "Vendor Specific (0019,1043)",
    (0x0019, 0x1047): "Vendor Specific (0019,1047)",
    (0x0019, 0x1050): "Vendor Specific (0019,1050)",
    (0x0019, 0x1052): "Vendor Specific (0019,1052)",
    (0x0019, 0x1060): "Vendor Specific (0019,1060)",
    (0x0019, 0x106a): "Vendor Specific (0019,106a)",
    (0x0019, 0x1081): "Vendor Specific (0019,1081)",
    (0x0019, 0x1091): "Vendor Specific (0019,1091)",
    (0x0019, 0x1610): "Vendor Specific (0019,1610)",
    (0x0019, 0x1613): "Vendor Specific (0019,1613)",
    (0x0019, 0x1615): "Vendor Specific (0019,1615)",
    (0x0019, 0x1616): "Vendor Specific (0019,1616)",
    (0x0019, 0x1617): "Vendor Specific (0019,1617)",
    (0x0019, 0x1618): "Vendor Specific (0019,1618)",
    (0x0019, 0x1619): "Vendor Specific (0019,1619)",
    (0x0019, 0x161a): "Vendor Specific (0019,161a)",
    (0x0019, 0x161b): "Vendor Specific (0019,161b)",
    (0x0019, 0x161c): "Vendor Specific (0019,161c)",
    (0x0019, 0x161d): "Vendor Specific (0019,161d)",
    (0x0019, 0x161e): "Vendor Specific (0019,161e)",
    (0x0019, 0x161f): "Vendor Specific (0019,161f)",
    (0x0019, 0x1621): "Vendor Specific (0019,1621)",
    (0x0020, 0x000d): "Study Instance UID",
    (0x0020, 0x000e): "Series Instance UID",
    (0x0020, 0x0010): "Study ID",
    (0x0020, 0x0011): "Series Number",
    (0x0020, 0x0012): "Acquisition Number",
    (0x0020, 0x0013): "Instance Number",
    (0x0020, 0x0020): "Patient Orientation",
    (0x0020, 0x0032): "Image Position - Patient",
    (0x0020, 0x0037): "Image Orientation - Patient",
    (0x0020, 0x0052): "Frame of Reference UID",
    (0x0020, 0x0060): "Laterality",
    (0x0020, 0x0062): "Image Laterality",
    (0x0020, 0x1040): "Position Reference Indicator",
    (0x0020, 0x1041): "Slice Location",
    (0x0020, 0x4000): "Image Comments",
    (0x0020, 0x9128): "Temporal Position Index",
    (0x0021, 0x0010): "Vendor Specific (0021,0010)",
    (0x0021, 0x1003): "Vendor Specific (0021,1003)",
    (0x0021, 0x1010): "Vendor Specific (0021,1010)",
    (0x0021, 0x1030): "Vendor Specific (0021,1030)",
    (0x0021, 0x1035): "Vendor Specific (0021,1035)",
    (0x0021, 0x1036): "Vendor Specific (0021,1036)",
    (0x0021, 0x1040): "Vendor Specific (0021,1040)",
    (0x0021, 0x1050): "Vendor Specific (0021,1050)",
    (0x0021, 0x1080): "Vendor Specific (0021,1080)",
    (0x0021, 0x1091): "Vendor Specific (0021,1091)",
    (0x0021, 0x1092): "Vendor Specific (0021,1092)",
    (0x0021, 0x1093): "Vendor Specific (0021,1093)",
    (0x0023, 0x0010): "Vendor Specific (0023,0010)",
    (0x0023, 0x1070): "Vendor Specific (0023,1070)",
    (0x0025, 0x0010): "Vendor Specific (0025,0010)",
    (0x0025, 0x0010): "Vendor Specific (0025,0010)",
    (0x0025, 0x1010): "Vendor Specific (0027,1010)",
    (0x0025, 0x1011): "Vendor Specific (0027,1011)",
    (0x0025, 0x1012): "Vendor Specific (0027,1012)",
    (0x0027, 0x0010): "Vendor Specific (0027,0010)",
    (0x0027, 0x1010): "Vendor Specific (0027,1010)",
    (0x0027, 0x101c): "Vendor Specific (0027,101c)",
    (0x0027, 0x101e): "Vendor Specific (0027,101e)",
    (0x0027, 0x101f): "Vendor Specific (0027,101f)",
    (0x0027, 0x1020): "Vendor Specific (0027,1020)",
    (0x0027, 0x1035): "Vendor Specific (0027,1035)",
    (0x0027, 0x1042): "Vendor Specific (0027,1042)",
    (0x0027, 0x1043): "Vendor Specific (0027,1043)",
    (0x0027, 0x1044): "Vendor Specific (0027,1044)",
    (0x0027, 0x1045): "Vendor Specific (0027,1045)",
    (0x0027, 0x1046): "Vendor Specific (0027,1046)",
    (0x0027, 0x1047): "Vendor Specific (0027,1047)",
    (0x0027, 0x1050): "Vendor Specific (0027,1050)",
    (0x0027, 0x1051): "Vendor Specific (0027,1051)",
    (0x0028, 0x0002): "Samples Per Pixel",
    (0x0028, 0x0004): "Photometric Interpretation",
    (0x0028, 0x0010): "Rows",
    (0x0028, 0x0011): "Columns",
    (0x0028, 0x0030): "Pixel Spacing",
    (0x0028, 0x0100): "Bits Allocated",
    (0x0028, 0x0101): "Bits Stored",
    (0x0028, 0x0102): "High Bit",
    (0x0028, 0x0103): "Pixel Representation",
    (0x0028, 0x0106): "Blind Spot Localized",
    (0x0028, 0x0107): "Blind Spot X-Coord",
    (0x0028, 0x0108): "Blind Spot Y-Coord",
    (0x0028, 0x0120): "Pixel Padding Value",
    (0x0028, 0x0301): "Burned In Annotation",
    (0x0028, 0x1040): "Pixel Intensity Relationship",
    (0x0028, 0x1041): "Pixel Intensity Relationship Sign",
    (0x0028, 0x1050): "Window Center",
    (0x0028, 0x1051): "Window Width",
    (0x0028, 0x1052): "Rescale Intercept",
    (0x0028, 0x1053): "Rescale Slope",
    (0x0028, 0x1054): "Rescale Type",
    (0x0028, 0x1055): "Window Center and Width Explanation",
    (0x0028, 0x1090): "Recommended Viewing Mode",
    (0x0028, 0x2110): "Lossy Image Compression",
    (0x0028, 0x6100): "Mask Subtraction Sequence",
    (0x0028, 0x6101): "Mask Operation",
    (0x0029, 0x0010): "Vendor Specific (0029,0010)",
    (0x0029, 0x1020): "Vendor Specific (0029,1020)",
    (0x0029, 0x1030): "Vendor Specific (0029,1030)",
    (0x0029, 0x1034): "Vendor Specific (0029,1034)",
    (0x0029, 0x1044): "Vendor Specific (0029,1044)",
    (0x0029, 0x1050): "Vendor Specific (0029,1050)",
    (0x0032, 0x1032): "Requesting Physician",
    (0x0032, 0x1033): "Requesting Service",
    (0x0040, 0x0244): "Performed Procedure Step Start Date",
    (0x0040, 0x0245): "Performed Procedure Step Start Time",
    (0x0040, 0x0253): "Performed Procedure Step ID",
    (0x0040, 0x0254): "Performed Procedure Step Description",
    (0x0040, 0x0255): "Performed Procedure Type Description",
    (0x0040, 0x0260): "Performed Protocol Code Sequence",
    (0x0040, 0x0275): "Request Attributes Sequence",
    (0x0040, 0x0555): "Acquisition Context Sequence",
    (0x0040, 0x1001): "Requested Procedure ID",
    (0x0040, 0x2017): "Filler Order Number",
    (0x0040, 0xa170): "Purpose of Reference Code Sequence",
    (0x0043, 0x0010): "Vendor Specific (0043,0010)",
    (0x0043, 0x1010): "Vendor Specific (0043,1010)",
    (0x0043, 0x1012): "Vendor Specific (0043,1012)",
    (0x0043, 0x1016): "Vendor Specific (0043,1016)",
    (0x0043, 0x101e): "Vendor Specific (0043,101e)",
    (0x0043, 0x101f): "Vendor Specific (0043,101f)",
    (0x0043, 0x1021): "Vendor Specific (0043,1021)",
    (0x0043, 0x1025): "Vendor Specific (0043,1025)",
    (0x0043, 0x1026): "Vendor Specific (0043,1026)",
    (0x0043, 0x1027): "Vendor Specific (0043,1027)",
    (0x0043, 0x1028): "Vendor Specific (0043,1028)",
    (0x0043, 0x102b): "Vendor Specific (0043,102b)",
    (0x0043, 0x1031): "Vendor Specific (0043,1031)",
    (0x0043, 0x1040): "Vendor Specific (0043,1040)",
    (0x0043, 0x1041): "Vendor Specific (0043,1041)",
    (0x0043, 0x1042): "Vendor Specific (0043,1042)",
    (0x0043, 0x1043): "Vendor Specific (0043,1043)",
    (0x0043, 0x1044): "Vendor Specific (0043,1044)",
    (0x0043, 0x1045): "Vendor Specific (0043,1045)",
    (0x0043, 0x1046): "Vendor Specific (0043,1046)",
    (0x0043, 0x104d): "Vendor Specific (0043,104d)",
    (0x0043, 0x104e): "Vendor Specific (0043,104e)",
    (0x0043, 0x1064): "Vendor Specific (0043,1064)",
    (0x0043, 0x1065): "Vendor Specific (0043,1065)",
    (0x0043, 0x1067): "Vendor Specific (0043,1067)",
    (0x0045, 0x0010): "Vendor Specific (0045,0010)",
    (0x0045, 0x1001): "Vendor Specific (0045,1001)",
    (0x0045, 0x1002): "Vendor Specific (0045,1002)",
    (0x0045, 0x1003): "Vendor Specific (0045,1003)",
    (0x0045, 0x1004): "Vendor Specific (0045,1004)",
    (0x0045, 0x1006): "Vendor Specific (0045,1006)",
    (0x0045, 0x1007): "Vendor Specific (0045,1007)",
    (0x0045, 0x1008): "Vendor Specific (0045,1008)",
    (0x0045, 0x1009): "Vendor Specific (0045,1009)",
    (0x0045, 0x100a): "Vendor Specific (0045,100a)",
    (0x0045, 0x100b): "Vendor Specific (0045,100b)",
    (0x0045, 0x100c): "Vendor Specific (0045,100c)",
    (0x0045, 0x100d): "Vendor Specific (0045,100d)",
    (0x0045, 0x100e): "Vendor Specific (0045,100e)",
    (0x0045, 0x100f): "Vendor Specific (0045,100f)",
    (0x0045, 0x1010): "Vendor Specific (0045,1010)",
    (0x0045, 0x1011): "Vendor Specific (0045,1011)",
    (0x0045, 0x1012): "Vendor Specific (0045,1012)",
    (0x0045, 0x1013): "Vendor Specific (0045,1013)",
    (0x0045, 0x1014): "Vendor Specific (0045,1014)",
    (0x0045, 0x1015): "Vendor Specific (0045,1015)",
    (0x0045, 0x1016): "Vendor Specific (0045,1016)",
    (0x0045, 0x1017): "Vendor Specific (0045,1017)",
    (0x0045, 0x1018): "Vendor Specific (0045,1018)",
    (0x0045, 0x1021): "Vendor Specific (0045,1021)",
    (0x0045, 0x1022): "Vendor Specific (0045,1022)",
    (0x0045, 0x1032): "Vendor Specific (0045,1032)",
    (0x0045, 0x103b): "Vendor Specific (0045,103b)",
    (0x0053, 0x0010): "Vendor Specific (0053,0010)",
    (0x0053, 0x1020): "Vendor Specific (0053,1020)",
    (0x0053, 0x1040): "Vendor Specific (0053,1040)",
    (0x0053, 0x1041): "Vendor Specific (0053,1041)",
    (0x0053, 0x1042): "Vendor Specific (0053,1042)",
    (0x0053, 0x1043): "Vendor Specific (0053,1043)",
    (0x0053, 0x1060): "Vendor Specific (0053,1060)",
    (0x0053, 0x1061): "Vendor Specific (0053,1061)",
    (0x0053, 0x1062): "Vendor Specific (0053,1062)",
    (0x0053, 0x1063): "Vendor Specific (0053,1063)",
    (0x0053, 0x1064): "Vendor Specific (0053,1064)",
    (0x0053, 0x1065): "Vendor Specific (0053,1065)",
    (0x0053, 0x1066): "Vendor Specific (0053,1066)",
    (0x0053, 0x1067): "Vendor Specific (0053,1067)",
    (0x0053, 0x1068): "Vendor Specific (0053,1068)",
    (0x0053, 0x106a): "Vendor Specific (0053,106a)",
    (0x0053, 0x106b): "Vendor Specific (0053,106b)",
    (0x0053, 0x109d): "Vendor Specific (0053,109d)",
    (0x0088, 0x0200): "Icon Image Sequence",
    (0x0903, 0x0010): "Vendor Specific (0903,0010)",
    (0x0903, 0x1010): "Vendor Specific (0903,1010)",
    (0x0903, 0x1011): "Vendor Specific (0903,1011)",
    (0x0903, 0x1012): "Vendor Specific (0903,1012)",
    (0x0905, 0x0010): "Vendor Specific (0905,0010)",
    (0x0905, 0x1030): "Vendor Specific (0905,1030)",
    (0x2010, 0x0010): "Image Display Format",
    (0x2050, 0x0020): "Presentation LUT Shape",
    (0x2010, 0x0030): "Annotation Display Format ID",
    (0x2010, 0x0040): "Film Orientation",
    (0x2010, 0x0100): "Border Density",
    (0x2010, 0x0140): "Trim",
    (0x3109, 0x0010): "Vendor Specific (3109,0010)",
    (0x3109, 0x0011): "Vendor Specific (3109,0011)",
    (0x3109, 0x1002): "Vendor Specific (3109,1002)",
    (0x3109, 0x1008): "Vendor Specific (3109,1008)",
    (0x3109, 0x100a): "Vendor Specific (3109,100a)",
    (0x3109, 0x100b): "Vendor Specific (3109,100b)",
    (0x3109, 0x1112): "Vendor Specific (3109,1112)",
    (0x50f1, 0x0010): "Vendor Specific (50f1,0010)",
    (0x50f1, 0x100a): "Vendor Specific (50f1,100a)",
    (0x50f1, 0x100b): "Vendor Specific (50f1,100b)",
    (0x50f1, 0x1010): "Vendor Specific (50f1,1010)",
    (0x50f1, 0x1020): "Vendor Specific (50f1,1020)",
    (0x7fd1, 0x0010): "Vendor Specific (7fd1,0010)",
    (0x7fd1, 0x1010): "Vendor Specific (7fd1,1010)",
    (0x7fe0, 0x0010): "Pixel Data",
    (0xfffe, 0xe000): "Item Tag",
    (0xffff, 0xffff): "LAST"
  }


  """ Whether each of the given tags have an implicit vr or not. """
  TAG_IMPLICIT_VR = defaultdict(lambda: False, {
    (0xfffe,0xe000): True
  })


  """ The length size for tags with implicit VRs. """
  IMPLICIT_VR_LENGTH = {
    (0xfffe, 0xe000): 4
  }


  """ The length size for different VRs. """
  VR_LENGTH = defaultdict(lambda: 2, {
    "OB": 4,  # Other Byte String
    "OW": 4,  # Other Word String
    "SQ": 4,  # Sequence
    "UN": 4   # Unknown bytes
  })


  """ The padding size for different VRs. """
  VR_PADDING = defaultdict(lambda: 0, {
    "OB": 2,
    "OW": 2,
    "SQ": 2,
    "UN": 2
  })


  """ Constructor. """
  def __init__(self, filename):
    self.f = open(filename, "rb")
    pass


  """ Helper to read the DICOM file header. """
  def _readHeader(self):
    h = self.f.read(128)
    for c in h:
      if c != "\x00":
        raise Exception("Invalid header: Not started with 128 zeroes.")
    h = self.f.read(4)
    if h != "DICM":
      raise Exception("Invalid header: Not DICM:", h)


  """ Helper for reading a tag. """
  def _readTag(self):
    t = self.f.read(4)
    if t == '':
      raise EOFError()
    t = struct.unpack("HH", t)
    if t not in File.TAG_NAMES:
      # Debugging
      raise Exception("Invalid tag:", t, self.f.tell())
    return (t, 4)


  """ Helper to read the value type. """
  def _readVR(self):
    v = self.f.read(2)
    if v == '':
      raise EOFError()
    return (v, 2)


  """ Helper to read the length from a data element. """
  def _readLength(self, padding, size):
    self.f.read(padding)
    l = self.f.read(size)
    if l == '':
      raise EOFError()
    if size == 2:
      return (struct.unpack("H", l)[0], 2)
    elif size == 4:
      return (struct.unpack("I", l)[0], 4)
    else:
      raise Exception("Invalid length size.")


  """ Helper to read a value from a data element. """
  def _readValue(self, tag, val, size, depth):
    if val == "SQ":
      self._handleSequenceStart(tag, val, size, depth)
      return ("", self._readFixedLengthSequence(size, depth))
    elif tag == (0xfffe, 0xe000):
      self._handleSequenceItem(tag, val, size, depth)
      return ("", self._readFixedLengthSequence(size, depth))
    else:
      d = self.f.read(size)
      # Allow derived classes to handle this value.
      self._handleValue(tag, val, size, depth, d)
      return (d, size)


  """ Helper to read sequences. """
  def _readFixedLengthSequence(self, size, depth):
    left = size
    while left > 0:
      t,d = self._readTag()
      left -= d
      #print File.TAG_NAMES[t]

      if File.TAG_IMPLICIT_VR[t]:
        v = "UL"
        #print "IMPLICIT"

        padding = 0
        length = File.IMPLICIT_VR_LENGTH[t]
      else:
        v,d = self._readVR()
        left -= d
        #print v

        padding = File.VR_PADDING[v]
        length = File.VR_LENGTH[v]

      l,d = self._readLength(padding, length)
      left -= d
      #print l

      left -= self._readValue(t, v, l, depth + 1)[1]
    self._handleSequenceOrItemEnd(size, depth)
    return size


  """ Helper to handle a sequence starting. """
  def _handleSequenceStart(self, tag, val, size, depth):
    pass


  """ Helper to handle a sequence item. """
  def _handleSequenceItem(self, tag, val, size, depth):
    pass


  """ Helper to handle a sequence or item ending. """
  def _handleSequenceOrItemEnd(self, size, depth):
    pass


  """ Helper to handle data. """
  def _handleValue(self, tag, val, size, depth, data):
    pass


  """ Read a Dicom file. """
  def read(self):
    self._readHeader()
    try:
      while True:
        t = self._readTag()[0]
        #print File.TAG_NAMES[t]

        # TODO: Take into account File.IMPLICIT_VR_LENGTH...
        if File.TAG_IMPLICIT_VR[t]:
          v = "UL"
          #print "IMPLICIT"

          padding = 0
          length = File.IMPLICIT_VR_LENGTH[t]
        else:
          v = self._readVR()[0]
          #print v
          padding = File.VR_PADDING[v]
          length = File.VR_LENGTH[v]

        l = self._readLength(padding, length)[0]
        #print l

        self._readValue(t, v, l, 0)
    except EOFError:
      print "EOF"



""" Dicom Dump File """
class DumpFile(File):
  def __init__(self, filename):
    super(self.__class__, self).__init__(filename)
    # The current tab spacing for debug output.
    self.current_tab = ""


  def _handleSequenceStart(self, tag, val, size, depth):
    super(self.__class__, self)._handleSequenceStart(tag, val, size, depth)
    print self.current_tab + File.TAG_NAMES[tag]
    self.current_tab += "  "


  def _handleSequenceItem(self, tag, val, size, depth):
    super(self.__class__, self)._handleSequenceItem(tag, val, size, depth)
    print self.current_tab + "-----------------------"
    self.current_tab += "  "


  def _handleSequenceOrItemEnd(self, size, depth):
    super(self.__class__, self)._handleSequenceOrItemEnd(size, depth)
    self.current_tab = self.current_tab[:-2]


  def _handleValue(self, tag, val, size, depth, data):
    super(self.__class__, self)._handleValue(tag, val, size, depth, data)
    print self.current_tab + File.TAG_NAMES[tag]
    if len(data) == 0:
      print self.current_tab + "  " + "Empty"
    elif val == "US":
      print self.current_tab + "  " + str(struct.unpack("H", data)[0])
    elif val == "UL":
      print self.current_tab + "  " + str(struct.unpack("I", data)[0])
    elif val == "SS":
      print self.current_tab + "  " + str(struct.unpack("h", data)[0])
    elif val == "OB":
      print self.current_tab + "  " + "(data size:", size, ")"
    elif val == "OW":
      print self.current_tab + "  " + "(data size:", size, ")"
    elif val == "UN":
      print self.current_tab + "  " + "(data size:", size, ")"
    elif val == "FD":
      print self.current_tab + "  " + "(data size:", size, ")"
    elif val == "DA":
      print self.current_tab + "  " + str(data[0:4] + "/" + data[4:6] +
                                          "/" + data[6:])
    elif val == "TM":
      print self.current_tab + "  " + str(data[0:2] + ":" + data[2:4] +
                                          ":" + data[4:])
    elif val in ["UI", "SH", "AE", "CS", "PN", "LO", "IS", "DS", "ST", "AS",
                 "LT"]:
      print self.current_tab + "  " + str(data)
    else:
      raise Exception("Unhandled Value: ", val)



""" Dicom Image File """
class ImageFile(File):
  def __init__(self, filename, out_filename):
    super(self.__class__, self).__init__(filename)

    # The most recent bitmap metadata read from the file.
    self.last_image_data = {
      "width": 1024,
      "height": 1024,
      "format": "",
      "samples": 1,
      "bpp": 16
    }
    self.out_filename = out_filename


  def _handleValue(self, tag, val, size, depth, data):
    super(self.__class__, self)._handleValue(tag, val, size, depth, data)

    # Handle collecting File IDs
    if depth == 0:
      if tag == (0x0028, 0x0002):  # Samples Per Pixel
        self.last_image_data["samples"] = struct.unpack("H", data)[0]
      elif tag == (0x0028, 0x0004): # Photometric Interpretation
        self.last_image_data["format"] = str(data)
      elif tag == (0x0028, 0x0010): # Rows
        self.last_image_data["height"] = struct.unpack("H", data)[0]
      elif tag == (0x0028, 0x0011): # Columns
        self.last_image_data["width"] = struct.unpack("H", data)[0]
      elif tag == (0x0028, 0x0101): # Bits Stored
        self.last_image_data["bpp"] = struct.unpack("H", data)[0]
      elif tag == (0x7fe0, 0x0010): # Pixel Data
        invert = False
        if self.last_image_data["format"] == "MONOCHROME1 ":
          invert = True
        elif self.last_image_data["format"] == "MONOCHROME2 ":
          invert = False
        else:
          raise Exception("Unsupported image format:",
                          self.last_image_data["format"])
        if self.last_image_data["bpp"] == 16:
          self._slowWriteBitmap(self.last_image_data["width"],
                                self.last_image_data["height"],
                                self.last_image_data["samples"],
                                self.last_image_data["bpp"],
                                invert,
                                data)
        else:
          self._writeBitmap(self.last_image_data["width"],
                            self.last_image_data["height"],
                            self.last_image_data["samples"],
                            self.last_image_data["bpp"],
                            invert,
                            data)


  """ Helper to write out a bitmap. """
  def _writeBitmap(self, width, height, samples, bpp, invert, data):
    shift = bpp - 8
 
    mult4 = lambda n: int(math.ceil(n/4.0))*4
    lh = lambda n: struct.pack("<h", n)
    li = lambda n: struct.pack("<i", n)

    header = (b"BM" +
              li((height * mult4(width * 3)) + 0x36) +
              b"\x00\x00\x00\x00" + # Must be Zeros
              b"\x36\x00\x00\x00" + # Offset of first pixel data
              b"\x28\x00\x00\x00" + # Size of BitmapInfoHeader (40 bytes)
              li(width) +           # Width
              li(height) +          # Height
              b"\x01\x00" +         # Color planes (always 1)
              lh(24) +              # BPP
              b"\x00\x00\x00\x00" + # No compression
              b"\x00\x00\x00\x00" +
              b"\x00\x00\x00\x00" +
              b"\x00\x00\x00\x00" +
              b"\x00\x00\x00\x00" +
              b"\x00\x00\x00\x00")

    extra_bytes = (mult4(width * 3) - (width * 3))
    encoded_data = b""
    for r in range(height-1, -1, -1):
      for c in range(width):
        pixel = struct.unpack_from("<H", data, (r*width+c)*2)[0]
        pixel = (pixel >> shift) & 0xff
        if invert:
          pixel = 0xff - pixel
        encoded_data += struct.pack("3B", pixel, pixel, pixel)
      for e in range(extra_bytes):
        encoded_data += b"\x00"
    fout = open(self.out_filename, "wb")
    fout.write(header)
    fout.write(encoded_data)
    fout.close()


  """ Helper to write out a bitmap. """
  def _slowWriteBitmap(self, width, height, samples, bpp, invert, data):
    maxVal = 0x0000
    minVal = 0xffff
    for r in range(height-1, -1, -1):
      for c in range(width):
        pixel = struct.unpack_from("<H", data, (r*width+c)*2)[0]
        # HACK: Exclude the high order bits which are noisy in the CT images.
        pixel = pixel & 0x0fff
        if pixel > maxVal:
          maxVal = pixel
        if pixel < minVal:
          minVal = pixel
 
    mult4 = lambda n: int(math.ceil(n/4.0))*4
    lh = lambda n: struct.pack("<h", n)
    li = lambda n: struct.pack("<i", n)

    header = (b"BM" +
              li((height * mult4(width * 3)) + 0x36) +
              b"\x00\x00\x00\x00" + # Must be Zeros
              b"\x36\x00\x00\x00" + # Offset of first pixel data
              b"\x28\x00\x00\x00" + # Size of BitmapInfoHeader (40 bytes)
              li(width) +           # Width
              li(height) +          # Height
              b"\x01\x00" +         # Color planes (always 1)
              lh(24) +              # BPP
              b"\x00\x00\x00\x00" + # No compression
              b"\x00\x00\x00\x00" +
              b"\x00\x00\x00\x00" +
              b"\x00\x00\x00\x00" +
              b"\x00\x00\x00\x00" +
              b"\x00\x00\x00\x00")

    extra_bytes = (mult4(width * 3) - (width * 3))
    encoded_data = b""
    for r in range(height-1, -1, -1):
      for c in range(width):
        pixel = struct.unpack_from("<H", data, (r*width+c)*2)[0]
        # HACK: Exclude the high order bits which are noisy in the CT images.
        pixel = pixel & 0x0fff
        pixel = int(float(pixel-minVal) / float(maxVal-minVal) * float(255)) & 0xff
        # HACK: Any noise should get turned black.
        if pixel >= 235:
          pixel = 0
        if invert:
          pixel = 0xff - pixel
        encoded_data += struct.pack("3B", pixel, pixel, pixel)
      for e in range(extra_bytes):
        encoded_data += b"\x00"
    fout = open(self.out_filename, "wb")
    fout.write(header);
    fout.write(encoded_data)
    fout.close()



""" Dicom Directory File """
class DirectoryFile(File):
  def __init__(self, filename):
    super(self.__class__, self).__init__(filename)

    # The most recent bitmap metadata read from the file.
    self.last_name = None
    self.last_type = None
    self.last_width = 0
    self.last_height = 0
    self.files = []


  def _handleSequenceOrItemEnd(self, size, depth):
    super(self.__class__, self)._handleSequenceOrItemEnd(size, depth)
    if self.last_name is not None and self.last_type is not None:
      #if (self.last_width != 512 or self.last_height != 512) and (self.last_width != 1024 or self.last_height != 1024):
      #if (self.last_width == 512 and self.last_height == 512):
        #print self.last_width, self.last_height, self.last_name, self.last_type
      self.files.append(self.last_name)
    self.last_name = None
    self.last_type = None
    self.last_width = 0
    self.last_height = 0


  def _handleValue(self, tag, val, size, depth, data):
    super(self.__class__, self)._handleValue(tag, val, size, depth, data)

    # Handle collecting File IDs
    if tag == (0x0004, 0x1500):  # Referenced File ID
      self.last_name = str(data)
    elif tag == (0x0008, 0x0008): # Image Type
      self.last_type = str(data)
    elif tag == (0x0028, 0x0010): # Rows
      self.last_height = struct.unpack("H", data)[0]
    elif tag == (0x0028, 0x0011): # Columns
      self.last_width = struct.unpack("H", data)[0]
