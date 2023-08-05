from __future__ import division
import pandas as pd
import numpy as np
import math
from scipy.interpolate import interp1d
from matplotlib import path
import matplotlib.pyplot as plt
from hydroinform.core import lazy_property

class HydroTs(object):
    def __init__(self, TimeSeries):
        self.time_series= TimeSeries
        self.__np_values = TimeSeries.values
        self.__np_index = TimeSeries.index.values
        self.__years = TimeSeries.index.year
        self.__values_range = range(len(self.__np_values))


    def EventFreq(self, Comparer):
        EventCount = {}
        EventLength = {}
        currentyear = self.__years[0]
        NumberOfEvents = 0;
        CurrentEventLengt = []
        InEvent = False

        for i in self.__values_range:
            #We got a new year. Store data
            if (self.__years[i] != currentyear):
                EventCount[currentyear]= NumberOfEvents
                EventLength[currentyear]= CurrentEventLengt
                currentyear = self.__years[i];
                NumberOfEvents = 0;
                CurrentEventLengt = [];
                CurrentEventLengt.append(0);
    
            if (Comparer(self.__np_values[i])):
            #This is a new event
                if not InEvent:
                    NumberOfEvents+=1
                    InEvent = True
                    CurrentEventLengt.append(0)
            #Increase number of days in event
                CurrentEventLengt[len(CurrentEventLengt) - 1]+=1
            else:
                InEvent = False
    
        if not currentyear in EventCount:
            EventCount[currentyear] = NumberOfEvents
            EventLength[currentyear] = CurrentEventLengt
        #First average the length on years, then average the averages
        #Average length on years:
        ayear=np.mean([v for k,v in EventCount.items()])
        lengthMoreThenZero=[v for k,v in EventLength.items() if len(v)>0]
        if len(lengthMoreThenZero)== 0:
            return [ayear, 0]
        return [ayear, np.mean([np.mean(v) for v in lengthMoreThenZero])]   

    @lazy_property
    def Q95(self):
        self.__set_percentiles()
        return self._lazy_Q95

    @lazy_property
    def Q90(self):
        self.__set_percentiles()
        return self._lazy_Q90


    @lazy_property
    def Q75(self):
        self.__set_percentiles()
        return self._lazy_Q75

    @lazy_property
    def Q50(self):
        self.__set_percentiles()
#        Q50 =self.time_series.median()
        return self._lazy_Q50

    @lazy_property
    def Q25(self):
        self.__set_percentiles()
        return self._lazy_Q25


    def __set_percentiles(self):
        q=[0.05, 0.1, 0.25,0.5,0.75]
        p= np.quantile(self.__np_values, q, interpolation ='linear')
        self._lazy_Q95 =p[0]
        self._lazy_Q90 =p[1]
        self._lazy_Q75=p[2]
        self._lazy_Q50=p[3]
        self._lazy_Q25=p[4]

    def fre25(self):
        return self.EventFreq(lambda v : v > self.Q25)[0]

    def fre75(self):
        return self.EventFreq(lambda v : v > self.Q75)[0]

    def fre1(self):
        return self.EventFreq(lambda v : v > self.Q50)[0]

    def fre3(self):
        return self.EventFreq(lambda v : v > 3*self.Q50)[0]

    def fre7(self):
        return self.EventFreq(lambda v : v > 7*self.Q50)[0]

    """
    Calculates the average number of timesteps where the value is above a threshold
    """
    def duration(self, Threshold):
        Durations = []
        Durations.append(0)

        for i in self.__values_range:
            if (self.__np_values[i] > Threshold):
                Durations[-1]+=1
            elif self.__np_values[i] <= Threshold and Durations[-1] > 0:
                Durations.append(0)
    
        if Durations[-1] == 0:
            del Durations[-1]
        if (len(Durations) == 0):
            return 0
        return np.mean(Durations)

    def values_above(self, Threshold):
        Durations = []
        Durations.append([])

        for i in self.__values_range:
            if (self.__np_values[i] > Threshold):
                Durations[-1].append(self.__np_values[i])
            elif self.__np_values[i] <= Threshold and len(Durations[-1]) > 0:
                Durations.append([])
    
        if len(Durations[-1]) == 0:
            del Durations[-1]
        return Durations




    """
    Calculates the average number of timesteps where the value is below a threshold
    """
    def DurationBelow(self, Threshold):
        Durations = []
        Durations.append(0)

        for i in self.__values_range:
            if (self.__np_values[i] < Threshold):
                Durations[-1]+=1
            elif self.__np_values[i] >= Threshold and Durations[-1] > 0:
                Durations.append(0)
    
        if Durations[-1] == 0:
            del Durations[-1]
        if (len(Durations) == 0):
            return 0
        return np.mean(Durations)


    def DVFIEQR(self, sin = 2):
        if self.Q50==0:
            return 0
        return 0.217 + 0.103 * sin + 0.02 * self.Q90/self.Q50 * self.EventFreq(lambda v : v > self.Q50)[0];


    def DVPIEQR(self):
        return 0.546 + 0.02 * self.fre25() - 0.019 * self.dur3() - 0.025 * self.fre75()


    def DFFV_EQR(self, sin = 2):
        p25 = self.Q75;
        p75 = self.Q25;
        return 0.811 * self.BaseFlowIndex() + 0.058 * sin + 0.05 * self.EventFreq(lambda v : v >= p75)[0] - 0.319 - 0.0413 * self.EventFreq(lambda v : v <= p25)[0];
    
    
    def medianmin(self):
        return self.time_series.resample("A").min().median()

    def medianmax(self):
        return self.time_series.resample("A").max().median()

    def medmin(self):
        return self.medianmin()/self.Q50

    def medmax(self):
        return self.medianmax()/self.Q50

    def mamin(self):
        return self.time_series.resample("A").min().mean()/self.Q50

    def mamax(self):
        return self.time_series.resample("A").max().mean()/self.Q50

    def mamax7(self):
        return self.__mamax( 7)

    def mamax30(self):
        return self.__mamax( 30)

    def fremedmin(self):
        val =self.medmin()
        return self.EventFreq( lambda v : v < val)[0]

    def mf(self):
        return self.time_series.mean()

    def cv(self):
        return self.time_series.var()

    def q1(self):
        return self.time_series.quantile(0.01, interpolation='linear')/self.Q50

    def q10(self):
        return self.time_series.quantile(0.1, interpolation='linear')/self.Q50

    def q25(self):
        return self.time_series.quantile(0.25, interpolation='linear')/self.Q50

    def q75(self):
        return self.time_series.quantile(0.75, interpolation='linear')/self.Q50

    def q90(self):
        return self.time_series.quantile(0.90, interpolation='linear')/self.Q50

    def durmedmin(self):
        val =medmin(self.time_series)
        return Duration(self.time_series, val)

    def dur75(self):
        val =self.Q75()
        return self.DurationBelow( val)

    def dur1(self):
        val =self.Q50
        return self.duration( val)

    def dur3(self):
        val =self.Q50
        return self.duration( 3*val)

    def dur7(self):
        val =self.Q50
        return self.duration( 7*val)

    def dur25(self):
        val =Q25(self.time_series)
        return Duration(self.time_series, val)

    def pea1(self):
        val = self.Q50
        events = self.values_above( val)
        return np.mean([np.mean(t) for t in events])/val

    def pea3(self):
        val =self.Q50
        return np.mean([t for t in self.time_series if t>3*val])/val

    def pea7(self):
        val =self.Q50
        return np.mean([t for t in self.time_series if t>7*val])/val

    def pea25(self):
        val =Q25(self.time_series)
        return np.mean([t for t in self.time_series if t>val])/val

    def norises(self):
        toreturn =0
        for i in range(0,len(self.time_series)-1):
            if(self.time_series.values[i]<self.time_series.values[i+1]):
                toreturn+=1
        return toreturn/len(self.time_series)

    def nofalls(self):
        toreturn =0
        for i in range(0,len(self.time_series)-1):
            if(self.time_series.values[i]>self.time_series.values[i+1]):
                toreturn+=1
        return toreturn/len(self.time_series)


    def EQR_DFFV(self):
        return 0.38 - 0.01 * self.dur75() + 0.12 * self.pea1() - 0.1*self.dur7()

    def EQR_DFFV2(self):
        return 2.85 +1.531*self.mamin() - 0.031* self.fremedmin() - 9.206*self.norises()


    def __mamax(self, windowsize):
        maximums=[]
        for year in range(self.time_series.index[0].year,self.time_series.index[-1].year+1):
            maximums.append(self.time_series[str(year)].rolling(windowsize, win_type='triang').sum().max())
        maximums =[max for max in maximums if not math.isnan(max)]
        return np.mean(maximums)/self.Q50


    """
    /// Calculates the Base flow Index(BFI) from http://nora.nerc.ac.uk/6050/1/IH_108.pdf
    /// The self.TimeSeries must contain daily values
    """
    def BaseFlowIndex(self):
        if len(self.time_series) == 0:
            return -1;

        nDays = 5

        localcount = 0
        nDaysMin = []
        locallist = [];
        for i in self.__values_range:
            if (localcount == nDays):
                min1 = min(locallist)
                nDaysMin.append([ i - nDays + locallist.index(min1) , min1])
                locallist = []
                localcount = 0
            locallist.append(self.__np_values[i]);
            localcount+=1
    

        Ordinates = []
        nDaysMin09 =[l[1]*0.9 for l in nDaysMin]
        for i in range(0, len(nDaysMin) - 2):
            centralvalue = nDaysMin09[i + 1];
            if centralvalue < nDaysMin[i][1]  and centralvalue < nDaysMin[i + 2][1]:
                Ordinates.append(nDaysMin[i + 1])
    

        interpolated = []

        if len(Ordinates) < 2:
            return 0

        i1 = Ordinates[0][0]
        i2 = Ordinates[-1][0]

        interpolated = np.interp(range(i1, i2),[o[0] for o in Ordinates],[o[1] for o in Ordinates])


        Vb = sum(interpolated)
        vals = self.__np_values[i1:i2 - i1+1]
        Va = sum(vals)


        #Why?
##        vv = 0;
##        for i in range(1,len(vals)):
##            vv += (vals[i] + vals[i -1]) / 2;
    
        vvb = 0;
        for i in range (0,len(Ordinates)-1):
            vvb += (Ordinates[i][1] + Ordinates[i + 1][1]) / 2 * (Ordinates[i + 1][0] - Ordinates[i][0]);

        return Vb / Va;

class GroundWaterLayer(object):
    def __init__(self, gvk, dkmlag,dkmomr):
        self.feature = gvk
        self.insidecoords =[]
        self.holes=[]
        self.dkmlag=dkmlag
        self.dkmomr = dkmomr

        lastarea=-1
        for i in range(0, len(gvk.parts)):
            if i == len(gvk.parts)-1:
                end = len(gvk.points)-1
            else:
                end=gvk.parts[i+1]
            points=gvk.points[gvk.parts[i]:end]
            x=[p[0] for p in points]
            y=[p[1] for p in points]
            p=path.Path(points)
            area = 0.5*(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))
            if area<0: #Negative area means counter clock wise points which represents holes.
                self.holes.append(p)
            elif area>lastarea: #We have found a larger polgon. Use that
                self.path=p
                lastarea=area

        self.sum=0
        
    def plot(self):
        self.outeredge()
        plt.plot([p.x for p in self.insidecoords],[p.y for p in self.insidecoords],'x')
        plt.plot(self.path.vertices[:,0],self.path.vertices[:,1])
        for hole in self.holes:
            plt.plot(hole.vertices[:,0],hole.vertices[:,1])
            
        #Directions
        plt.plot([p.x for p in self.south],[p.y-250 for p in self.south],'^')
        plt.plot([p.x+250 for p in self.east],[p.y for p in self.east],'<')
        plt.plot([p.x-250 for p in self.west],[p.y for p in self.west],'>')
        plt.plot([p.x for p in self.north],[p.y+250 for p in self.north],'v')
        
        plt.gca().axis('equal')
    

    def remove_holes(self):
        toremove=[]
        for hole in self.holes:
            for p in self.insidecoords:
                if hole.contains_point((p.x,p.y)):
                    toremove.append(p)
        
        for p in toremove:
            self.insidecoords.remove(p)
        
    def outeredge(self):
        self.north=[]
        self.south=[]
        self.east =[]
        self.west=[]
        dict_coord={}
        dict_coord_row={}
        for c in self.insidecoords:
            if not c.col in dict_coord:
                dict_coord[c.col]=[]
            dict_coord[c.col].append(c.row)
            if not c.row in dict_coord_row:
                dict_coord_row[c.row]=[]
            dict_coord_row[c.row].append(c.col)
        for c in self.insidecoords:
            if not c.row+1 in dict_coord[c.col]:
                self.north.append(c)
            if not c.row-1 in dict_coord[c.col]:
                self.south.append(c)
            if not c.col+1 in dict_coord_row[c.row]:
                self.east.append(c)
            if not c.col-1 in dict_coord_row[c.row]:
                self.west.append(c)




                
class GroundWaterBody(object):
    def __init__(self, name):
        self.name = name
        self.GroundWaterLayers = []
    
    def sort_layers(self):
        #remove layers without dfs-points
        self.GroundWaterLayers = [b for b in self.GroundWaterLayers if len(b.insidecoords)>0]
        
        if len(self.GroundWaterLayers)>0:
            self.GroundWaterLayers.sort(key=lambda gwl:gwl.insidecoords[0].layer, reverse=True)            
            self.points_from_above=self.__project()
            self.GroundWaterLayers.sort(key=lambda gwl:gwl.insidecoords[0].layer)            
            self.points_from_below=self.__project()
        else:
            self.points_from_above=[]
            self.points_from_below=[]

 
    def __project(self):            
        points_from_above=[]
        points_from_above.extend(self.GroundWaterLayers[0].insidecoords)
    
        if len(self.GroundWaterLayers)>1:
            dict_coord={}
            for c in points_from_above:
                if not c.col in dict_coord:
                    dict_coord[c.col]=[]
                dict_coord[c.col].append(c.row)
                  
            for i in range(1,len(self.GroundWaterLayers)):
                for c in self.GroundWaterLayers[i].insidecoords:
                    if not c.col in dict_coord:
                        dict_coord[c.col]=[]
                    if not c.row in dict_coord[c.col]:
                        points_from_above.append(c)
                        dict_coord[c.col].append(c.row)
        return points_from_above
            

        
    def plot(self):
        from mpl_toolkits.mplot3d import Axes3D
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        for gwb in self.GroundWaterLayers:
            xs=[]
            ys=[]
            zs=[]
            for p in gwb.insidecoords:
                xs.append(p.x)
                ys.append(p.y)
                zs.append(p.layer)
                ax.scatter(xs, ys, zs)

        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')
        
        plt.show()

