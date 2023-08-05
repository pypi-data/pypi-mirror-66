# hydroinform
This package contains a steady-state stream model and some tools to access .dfs-files from DHI

# Usage
Convert .dfs, res1d and res11-files to netCDF:
```sh
#Import NetCDF and DFS from hydroinform
from hydroinform import NetCDF, DFS

#Saves "omr4_jag_3DSZ.dfs3 as "omr4_jag_3DSZ.nc"
NetCDF.save_as_NetCDF('omr4_jag_3DSZ.dfs3')

#Saves "omr4_jag_3DSZ.dfs3 as "newname.nc"
NetCDF.save_as_NetCDF('omr4_jag_3DSZ.dfs3','newname.nc')

#Saves only the first item and the second and fourth time step from "omr4_jag_3DSZ.dfs3""
d= DFS.DFSBase.open_file('omr4_jag_3DSZ.dfs3')
NetCDF.save_dfs_as_NetCDF(d, [0], [1,3], 'omr4_jag_3DSZ_one_time.nc')

#Saves the discharge data from "Storaa_HD_quasiStationary_20090701.res1d" as 'Storaa_HD_quasiStationary_20090701.nc'
NetCDF.save_as_NetCDF('Storaa_HD_quasiStationary_20090701.res1d')

```

Write a pump extraction file to be used with MikeZero:
```sh
#Import DFS from HydroInform
from hydroinform import DFS

#The number of Items (In this case number of pumping wells)
numberofitems = 5;

#Now create the file.
_tso = DFS.DFS0.new_file(r'c:\temp\extraction.dfs0'), numberofitems);

#Loop the items and set the units etc.
for itemCount in range (0, numberofitems):
    _tso.items[itemCount].value_type = DFS.DataValueType.MeanStepBackward
    _tso.items[itemCount].eum_item = DFS.EumItem.eumIPumpingRate
    _tso.items[itemCount].eum_unit = DFS.EumUnit.eumUm3PerYear
    _tso.items[itemCount].name = "Item number: " + str(itemCount)
      
#Loop the years where you have pumping data
tscount = 0;
for year in range(2010, 2016):
    #For every year append a new timestep
    _tso.append_time_step(datetime.datetime(year, 12, 31, 12))
    #Loop the items and set a value for this timestep
    for itemCount in range (0, numberofitems):
        #Sets the data. Note that timesteps count from 0 and Items count from 1
        _tso.set_data(tscount, itemCount+1, year * itemCount)
    tscount+=1
#Call dispose which will save and close the file.
_tso.dispose()
```