from netCDF4 import Dataset
import time as itime

root_group = Dataset("test.nc", "w", format="NETCDF4")
print(root_group.data_model)  # NETCDF4
print(root_group.groups)
print(root_group.cmptypes)
print(root_group.dimensions)
print(root_group.disk_format)  # HDF5
root_group.close()

# test.nc
# 8948 4446 0d0a 1a0a 0208 0800 0000 0000
# 0000 0000 ffff ffff ffff ffff ef00 0000
# 0000 0000 3000 0000 0000 0000 9433 450f
# 4f48 4452 020c b402 2200 0000 0000 0300
# 0000 0000 0000 00ff ffff ffff ffff ffff
# ffff ffff ffff ffff ffff ffff ffff ff0a
# 0200 0100 0000 0015 1c00 0400 0000 0301
# 00ff ffff ffff ffff ffff ffff ffff ffff
# ffff ffff ffff ffff ff0c 4500 0000 0003
# 000e 0008 0004 0000 5f4e 4350 726f 7065
# 7274 6965 7300 1300 0000 2200 0000 0200
# 0000 7665 7273 696f 6e3d 322c 6e65 7463
# 6466 3d34 2e39 2e30 2c68 6466 353d 312e
# 3132 2e32 0011 0000 0000 0000 0000 0000
# 0000 0000 0000 0000 0000 0038 945b 4d

root_group = Dataset("test.nc", "a")
forecast_grp = root_group.createGroup("forecasts")
analyze_grp = root_group.createGroup("analyses")
# print(root_group.groups)  # Only NETCDF4 formatted files support Groups

# the result of print(root_group.groups)
# {'forecasts': <class 'netCDF4._netCDF4.Group'>
# group /forecasts:
#     dimensions(sizes):
#     variables(dimensions):
#     groups: , 'analyses': <class 'netCDF4._netCDF4.Group'>
# group /analyses:
#     dimensions(sizes):
#     variables(dimensions):
#     groups: }

forecast_grp1 = root_group.createGroup("/forecasts/model1")
forecast_grp2 = root_group.createGroup("/forecasts/model2")


# print(root_group.groups)


# the result
# {'forecasts': <class 'netCDF4._netCDF4.Group'>
# group /forecasts:
#     dimensions(sizes):
#     variables(dimensions):
#     groups: model1, model2, 'analyses': <class 'netCDF4._netCDF4.Group'>
# group /analyses:
#     dimensions(sizes):
#     variables(dimensions):
#     groups: }

# print(root_group)


def walk_tree(t):
    yield t.groups.values()
    for value in t.groups.values():
        yield from walk_tree(value)


for children in walk_tree(root_group):
    for child in children:
        print(child)

level = root_group.createDimension("level", None)  # create an unlimited dimension (a dimension that can be appended to)
time = root_group.createDimension("time", None)
latitude = root_group.createDimension("lat", 73)  # 73 is the size of the dimension
longitude = root_group.createDimension("lon", 144)

print(root_group.dimensions)
print(time.isunlimited())

for dimension_object in root_group.dimensions.values():
    print(dimension_object)

times = root_group.createVariable("time", "f8", ("time",))  # the tuple argument here is for dimensions
levels = root_group.createVariable("level", "i4", ("level",))
latitudes = root_group.createVariable("lat", "f4", ("lat",))
longitudes = root_group.createVariable("lon", "f4", ("lon",))

temp = root_group.createVariable("temp", "f4", ("time", "level", "lat", "lon"))
# the above assignment means, create a variable named temp,
# the variable datatype is f4 which represents 32-bit floating point
# the variable's dimensions are ("time", "level", "lat", "lon"), which were already defined previously
# The dimensions themselves are usually also defined as variables, called coordinate variables
print(temp)

# The following two examples are netCDF global attributes,
# which belong to and provide information for the entire dataset
root_group.description = "some test script"
root_group.history = "Created" + itime.ctime(itime.time())
# The following two examples are netCDF variable attributes, which set value to variable instances
latitudes.units = "degrees north"
longitudes.units = "degrees east"

# To retrieve the names of all the netCDF instances
for name in root_group.ncattrs():
    print("Global attr {} = {}".format(name, getattr(root_group, name)))

print(root_group.__dict__)

