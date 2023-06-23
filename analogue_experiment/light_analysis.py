import numpy as np
import matplotlib.pyplot as plt

# experimental data: each row represents a different light level;
# each light level was measured twice at 6 decreasing distances
lux = np.array([
    [[104, 45, 22, 13, 8, 5], [104, 43, 23, 12, 6, 5]],
    [[115, 50, 25, 15, 9, 6], [105, 45, 20, 9, 5, 6]],
    [[127, 55, 29, 17, 10, 8], [127, 55, 30, 11, 5, 8]],
    [[143, 65, 32, 19, 12, 8], [143, 57, 27, 17, 12, 8]],
    [[152, 71, 35, 21, 12, 9], [152, 71, 35, 21, 12, 9]],
    [[160, 75, 40, 23, 15, 10], [160, 77, 36, 22, 14, 9]],
    [[165, 80, 41, 26, 17, 11], [165, 80, 32, 25, 17, 11]],
    [[185, 80, 44, 27, 18, 12], [185, 80, 44, 27, 18, 12]],
    [[207, 87, 45, 29, 20, 13], [175, 85, 47, 30, 20, 13]]
                ], dtype=np.float64)
dist = np.array([5, 10, 15, 20, 25, 30], dtype=np.float64)

lux *= dist**2
lux /= 50**2 # account for the tube lenght
lux *= 0.23/3.3 # account for the (measured) voltage drop when adding series resistors (2 * 1M Ohm) to reduce LED intensity
                # (we assume that the LED behaves liniarly at low voltages)
lux /= 125 # convert lux to W/m2 since lux is ajusted for human perception
           # luminous efficiency of a 5mm white LED is aprox. 125 lux/(W/m2)

lux = lux[:, :, 1:]
dist = dist[1:]

# calculate mean intensity and error
mean = np.mean(lux, axis=2)
err = np.abs(mean[:, :, np.newaxis] - lux)
err_mean = np.mean(err, axis=2)

x = np.arange(1, 20)[1:]

# plot mean intensity and error
plt.errorbar(x[:9]-1, mean[:, 0]*1000, err_mean[:, 0]*1000, color='darkgrey', elinewidth=1, capsize=2)
plt.errorbar(x[:9]-1, mean[:, 1]*1000, err_mean[:, 1]*1000, color='darkgrey', elinewidth=1, capsize=2)

# use least squares method to find the best fit lign
x //= 2
mean = mean.flatten()
m, c = np.linalg.lstsq(np.vstack([x, np.ones(len(mean))]).T, mean, rcond=None)[0]

# print the parameters to use in analysis.py and plot everything
print((m, c))

plt.xlabel("LED level")
plt.ylabel("Light Intensity (mW/m^2)")
plt.plot(np.arange(1, 10), (m*np.arange(1, 10)+c)*1000, color='red', zorder=10)

plt.savefig("LED vs Intensity.png")

plt.show()