import arcpy
# Importing in the ArcGIS Python Package which contains the following modules: charts, data access, geocoding, Image Analysis, Mapping, Metadata, Network Analyst, Sharing, Spatial Analyst, Workflow Manager
# Creating a filepath. Properties for the environment class are exposed as properties in the arcpy.env class. This class can be used to store and retrieve the current values from the file path.
arcpy.env.workspace = r"C:\Users\dsmcm\Desktop\Final project Programming"
# Converts a feature class or feature layer to a feature class.
# In this case, I was assigning the shapefile to under the grouping of the recently made geodatabase, the geodatabase is created under the name of the Arcgis project.
arcpy.FeatureClassToFeatureClass_conversion(r"C:\Users\dsmcm\Desktop\Final project Programming\Transport\shortened_roads.shp",
                                            r"C:\Users\dsmcm\Desktop\Final project Programming\Final Project Program ArcPY\Final Project Program ArcPY.gdb", "roadsforkoala")
# This line of code represents bringing in the csv file, to be displayed as a feature class based on x-, y- coordinates from a table. The coordinate system assigned is the Geocentric Datum of Australia 1994.
arcpy.management.XYTableToPoint(r"C:\Users\dsmcm\Desktop\Final project Programming\Koalas\Koala Location\Koala Location LLGDA94.csv",
                                r"C:\Users\dsmcm\Desktop\Final project Programming\Final Project Program ArcPY\Final Project Program ArcPY.gdb\KoalaLocationLLGDA94_Layer_XYTableToPoint",
                                "Longitude", "Latitude", None, "Geocentric Datum of Australia 1994")
# The buffer code is made from creating an offset based on the input's vertices. There will need a distance value, (side type, end type, which are style options for the buffer)
# Method being used as Planar, creating an Euclidean dstance buffer. "NONE" being the dissolve type, which is not needed in this project.
arcpy.analysis.Buffer("KoalaLocationLLGDA94_Layer_XYTableToPoint",
                      r"C:\Users\dsmcm\Desktop\Final project Programming\Final Project Program ArcPY\Final Project Program ArcPY.gdb\KoalaLocationLLGDA94_Buffer",
                      "2 Kilometers", "FULL", "ROUND", "NONE", None, "PLANAR")
# Similar line of code, but being 10 metres instead of 2 kilometres. This is buffering around the shapefile instead of the Koala study sites.
arcpy.analysis.Buffer("roadsforkoala", r"C:\Users\dsmcm\Desktop\Final project Programming\Final Project Program ArcPY\Final Project Program ArcPY.gdb\roadsbuffer",
                      "10 Meters", "FULL", "ROUND", "NONE", None, "PLANAR")
# This tool can be used to create a new dataset that contains a subset of features that were added to another dataset.
# The parameters for clip are: input features, features that are used to clip the input features, then the output feature class, the cluster tolerance will be set to None.
arcpy.analysis.Clip("roadsbuffer", "KoalaLocationLLGDA94_Buffer",
                    r"C:\Users\dsmcm\Desktop\Final project Programming\Final Project Program ArcPY\Final Project Program ArcPY.gdb\roadsbuffer_Clip", None)
# The merge process is used to combine both tables & feature classes into a single output. The parameter for "ADD_SOURCE_INFO" is to add the original source for each field inside of the clip.
arcpy.Merge_management(["roadsbuffer_Clip"], r"C:\Users\dsmcm\Desktop\Final project Programming\Final Project Program ArcPY\Final Project Program ArcPY.gdb\roadsbuffer_Clip_Merge1",
                       "", "ADD_SOURCE_INFO")
# Process designed to gather features that overlap, then will be written to the output feature class.
# The line contains: input features, the output feature class, the join attributes which will be "ALL", cluster tolerance once again set to None, the output type being the input.
arcpy.analysis.Intersect("roadsbuffer_Clip_Merge1 #;roadsbuffer_Clip #;KoalaLocationLLGDA94_Buffer #;roadsbuffer #",
                         r"C:\Users\dsmcm\Desktop\Final project Programming\Final Project Program ArcPY\Final Project Program ArcPY.gdb\roadsbuffer_intersect", "ALL", None, "INPUT")
# Combining features based on specific attributes
# Input features, Output features, Choosing fields/fields to aggregate features,
# 'None' for statistics field, the multi_part, allowing multiple features to be placed into the output, Dissolve_lines, dissolving into a single feaute.
arcpy.management.Dissolve("roadsbuffer_intersect", r"C:\Users\dsmcm\Desktop\Final project Programming\Final Project Program ArcPY\Final Project Program ArcPY.gdb\roadsbuffer_intersect_Dissolve",
                          "Koala_Num;Site_ID", None, "MULTI_PART", "DISSOLVE_LINES")
# Creating a new field for our distance.
# Including the input table from the dissolve output, the field name, field type being double, the field precision, scale & length are left to none. Not needed.
# Field alias is left blank, allowing fields to include null values. Allowing the newly created field to be not required, but not allowing any constrains.
arcpy.management.AddField("roadsbuffer_intersect_Dissolve", "Kilometres", "DOUBLE", None, None, None, '', "NULLABLE", "NON_REQUIRED", '')
# Including the value of the road length that was gathered from the feature class of 'roadsforkoala', establishing the length to be metres. (Backed up with coordinates)
arcpy.management.CalculateField("roadsbuffer_intersect_Dissolve", "Kilometres", "!Shape_Length!", "PYTHON3", '', "TEXT", "NO_ENFORCE_DOMAINS")
# Exported the new attribute table into a Excel spreadsheet to be continued on with the second part of the project.
arcpy.conversion.TableToExcel("roadsbuffer_intersect_Dissolve", r"C:\Users\dsmcm\Desktop\Final project Programming\result_table.xls", "NAME", "CODE")
