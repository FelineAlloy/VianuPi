import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

# Read coordinates from the file
with open('coordinates.txt', 'r') as file:
    lines = file.readlines()

# Extract latitude and longitude values
latitude = []
longitude = []
for line in lines:
    lat, lon = map(float, line.strip().split(','))
    latitude.append(lat)
    longitude.append(lon)

# Create a Basemap instance with desired map projection
m = Basemap(projection='cyl', lat_0=0, lon_0=0, llcrnrlat=-90, urcrnrlat=90)

# Draw continents, coastlines, and country borders in gray
m.fillcontinents(color='lightgray', lake_color='white')
m.drawcoastlines(linewidth=0.6)
m.drawcountries(linewidth=0.6)

# Draw meridians and parallels
m.drawmeridians(range(-180, 181, 30), labels=[False, False, False, True])
m.drawparallels(range(-90, 91, 30), labels=[True, False, False, False])

# Plot the coordinates on the map
x, y = m(longitude, latitude)
m.scatter(x, y, s=5, color='red')

# Customize the plot
plt.title("Trajectory of the ISS during the run of our code")
plt.xlabel("Longitude", labelpad=15)
plt.ylabel("Latitude", labelpad=20)
plt.gca().xaxis.set_label_coords(0.5, -0.1)
plt.gca().yaxis.set_label_coords(-0.1, 0.5)

# Show the plot
plt.show()
