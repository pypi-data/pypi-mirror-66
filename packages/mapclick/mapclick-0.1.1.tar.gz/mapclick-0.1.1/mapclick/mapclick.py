import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)
from matplotlib.widgets import Cursor
import numpy as np
import re
from io import StringIO
try:
    import cartopy
    import cartopy.crs as ccrs
    from cartopy.io.img_tiles import Stamen
    from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
except ModuleNotFoundError as e:
    raise('Please install cartopy to draw maps\n   conda install -c scitools cartopy')
try:
    import pyproj
    from pyproj.crs import CRS
except ModuleNotFoundError as e:
    raise('Please install pyproj to draw maps\n   pip install pyproj')


class Station(object):
    def __init__(self, sta_lst):
        dtype = {'names': ('station', 'evla', 'evlo'), 'formats': ('U20', 'f4', 'f4')}
        self.station, self.stla, self.stlo = np.loadtxt(sta_lst, dtype=dtype, unpack=True, ndmin=1)
        #self.station = [sta.decode() for sta in self.station]
        self.sta_num = self.stla.shape[0]


def read_lines(fname):
    with open(fname) as f:
        content = f.read()
    content_lines = re.split(r'>.+?\n', content)
    return [np.loadtxt(StringIO(line)) for line in content_lines[1:]]

class MapPoint():
    def __init__(self, figsize=(8, 8)):
        # self.lines = []
        self.xcoords = []
        self.ycoords = []
        self.line = None
        self.marker_visble = True
        self.points = [None, None]
        self.texts = [None, None]
        mercator = ccrs.Mercator()
        self.fig = plt.figure(figsize=figsize)
        self.ax = self.fig.add_subplot(1, 1, 1, projection=mercator)
        self.fig.canvas.mpl_connect('button_press_event', self.onclick)

    def generate_map(self, lonmin, lonmax, latmin, latmax, elev=False, background='terrain-background', resolution=6, xa=2, ya=2, nation=True):
        plt.cla()
        self.lonmin = lonmin
        self.lonmax = lonmax
        self.latmin = latmin
        self.latmax = latmax
        self.ax.set_extent([self.lonmin, self.lonmax, self.latmin, self.latmax], crs=ccrs.PlateCarree())
        if elev:
            tiler = Stamen(background)
            self.ax.add_image(tiler, resolution)
        self.ax.add_feature(cartopy.feature.COASTLINE)
        if nation:
            self.ax.add_feature(cartopy.feature.BORDERS, linestyle=':')
        self.set_ticks(xa=xa, ya=ya)

    def set_ticks(self, xa=2, ya=2):
        lon_axis = np.arange(self.lonmin, self.lonmax, xa)
        lat_axis = np.arange(self.latmin, self.latmax, ya)
        self.ax.set_xticks(lon_axis, crs=ccrs.PlateCarree())
        self.ax.set_yticks(lat_axis, crs=ccrs.PlateCarree())
        lon_formatter = LongitudeFormatter()
        lat_formatter = LatitudeFormatter()
        self.ax.xaxis.set_major_formatter(lon_formatter)
        self.ax.yaxis.set_major_formatter(lat_formatter)
        self.ax.grid(True)

    def plot_station(self, fname, marker='v', color='red'):
        stas = Station(fname)
        self.ax.plot(stas.stlo, stas.stla, marker=marker, color=color, linestyle="None",
                     alpha=0.7, transform=ccrs.PlateCarree())

    def plot_line(self, fname, **kw):
        lines = read_lines(fname)
        for line in lines:
            self.line = self.ax.plot(line[:, 0], line[:, 1], transform=ccrs.PlateCarree(), **kw)

    def onclick(self, event):
        pcs = pyproj.Proj(CRS.from_json_dict(self.ax.projection.proj4_params))
        lon, lat = pcs(event.xdata, event.ydata, inverse=True)
        if not self.marker_visble:
            self.points[0][0].set_marker("None") 
            self.points[1][0].set_marker("None") 
            self.texts[0].set_visible(False)
            self.texts[1].set_visible(False)
            self.line[0].set_linestyle("None")
        self.xcoords.append(lon)
        self.ycoords.append(lat)
        if len(self.xcoords) == 1:
            self.points[0] = self.ax.plot(event.xdata, event.ydata, marker='x', linestyle="None", color='k')
            self.texts[0] = self.ax.annotate('Lat: {:.2f}\nLon: {:.2f}'.format(lat, lon),
                             xy=(event.xdata, event.ydata), xycoords='data',
                             xytext=(0, 10), textcoords='offset points',
                             #  arrowprops=dict(facecolor='black', shrink=0.05),
                             horizontalalignment='center', verticalalignment='bottom',
                             bbox=dict(boxstyle="round",
                                       ec=(1., 0.5, 0.5),
                                       fc=(1., 0.8, 0.8),))
            self.marker_visble = True
        if len(self.xcoords) == 2:
            self.line = self.ax.plot(self.xcoords, self.ycoords, color='k', transform=ccrs.PlateCarree())
            self.points[1] = self.ax.plot(event.xdata, event.ydata, marker='x', linestyle="None", color='k')
            self.texts[1] = self.ax.annotate('Lat: {:.2f}\nLon: {:.2f}'.format(lat, lon),
                             xy=(event.xdata, event.ydata), xycoords='data',
                             xytext=(0, 10), textcoords='offset points',
                             #  arrowprops=dict(facecolor='black', shrink=0.05),
                             horizontalalignment='center', verticalalignment='bottom',
                             bbox=dict(boxstyle="round",
                                       ec=(1., 0.5, 0.5),
                                       fc=(1., 0.8, 0.8),))
            self.xcoords[:] = []
            self.ycoords[:] = []
            self.marker_visble = False
        plt.draw()        
    

if __name__ == "__main__":
    mp = MapPoint()
    mp.generate_map(100, 106, 21.5, 24.5, elev=True, resolution=8, nation=False, xa=0.5, ya=0.5)
    mp.plot_line('/Users/xumj/Documents/GMT/province.cn', linewidth=0.5, color='k')
    mp.plot_line('/Users/xumj/Documents/GMT/active_fault_dqd.ftd', linewidth=1, color=(0/255, 105/255, 167/255))
    mp.plot_station('/Users/xumj/Researches/SouthYNRF/sta.lst')
    plt.show()
