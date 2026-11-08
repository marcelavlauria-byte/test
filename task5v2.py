# Exercise #05-03: Plotting gridded data
import requests
import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

url = "https://raw.githubusercontent.com/manuelalehner/scientific_programming/main/data/era5_precip_july2025.nc"

ds = nc.Dataset("era5_data", memory=requests.get(url).content)

# here the arrays are created
precip = np.array(ds["tp"][0, :, :])
lon = np.array(ds["longitude"][:])
lat = np.array(ds["latitude"][:])

ds.close()

# this way it converts longitude from 0-360 to -180-180
# this means we only change the names of the numbers higher than 180
lon_new = lon.copy()
lon_new[lon_new > 180] -= 360

# argsort --> sorts the new array from the more neg value to the more positive value
# so the negative values are in the West side.
# idx --> is the index that will help for changing the columns of the array "precip"
idx = np.argsort(lon_new)

lon_new = lon_new[idx]
precip_new = precip[:, idx]

# Convert precipitation from meters to millimeters
precip_mm = precip_new * 1000


################ Figure ###########

fig = plt.figure(figsize=(12, 6))
ax = plt.axes(projection=ccrs.PlateCarree())
vmax = np.percentile(precip_mm, 99)

# base precipitation map on blues
im = ax.pcolormesh(
    lon_new, lat, precip_mm,
    shading="auto",
    cmap="Blues",
    vmin=0,
    vmax=vmax,
    transform=ccrs.PlateCarree()
)

# Lightblue contour: precipitation below 1 mm/day
ax.contour(
    lon_new, lat, precip_mm,
    levels=[1],
    colors="paleturquoise",
    linewidths=1,
    transform=ccrs.PlateCarree()
)

# Magenta contour: precipitation above 10 mm/day
ax.contour(
    lon_new, lat, precip_mm,
    levels=[10],
    colors="magenta",
    linewidths= 1,
    transform=ccrs.PlateCarree()
)

# Add continent outlines
ax.coastlines(resolution="110m", color="black", linewidth=0.8)

# Colorbar
fig.colorbar(im, ax=ax, label="Precipitation (mm/day)")

ax.set_title("ERA5 precipitation - July 2025")
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
ax.legend(
    handles=[
        plt.Line2D([0], [0], color="paleturquoise", label="< 1 mm/day"),
        plt.Line2D([0], [0], color="purple", label="> 10 mm/day")
    ],
    loc="lower left"
)
# Add latitude and longitude lines
gl = ax.gridlines(
    draw_labels=True,
    linewidth=0.5,
    color="gray",
    alpha=0.5,
    linestyle="--"
)

# Show labels only on the left and bottom
gl.top_labels = False
gl.right_labels = False
plt.show()

