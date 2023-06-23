import numpy as np
import cv2
import matplotlib.pyplot as plt

h = 3040
w = 4056 

ch = int(3040/2) - 60
cw = int(4056/2) + 60

# calculate mean of black images to use at zero level

black = np.zeros((100, 100, 3), dtype = np.uint8)
for i in range(5):
    img = cv2.imread(f'data/000_{i:03d}.png')
    img = img[ch-50 : ch+50, cw-50 : cw+50]

    black += img // 5

# cv2.imshow('black', black)

# create a mask arround non-black pixels
mask = np.zeros((100, 100), dtype = np.uint8)
mask = cv2.circle(mask, (50, 53), 23, 255, -1)
# cv2.imshow('mask', mask)

# for each image take the mean of the masek pixels and calculate an average signal level for each LED intensity
result = np.empty((0, 3))
res_err = np.empty((0, 3))
for j in range(1, 8):

    avg = np.empty((0, 3), dtype=np.uint16)
    for i in range(5):

        img = cv2.imread(f'data/{j:03d}_{i:03d}.png')
        img = img[ch-50 : ch+50, cw-50 : cw+50]
        img = cv2.subtract(img, black)

        avg_col = cv2.mean(img, mask=mask)[:3]
        avg_col = np.mean(img[53, 50-23:50+23, :], axis=0)
        avg = np.vstack([avg, avg_col])


        #img = cv2.bitwise_and(img, img, mask = mask)
        # cv2.imshow('img', img)
        
    mean = np.mean(avg, axis=0)
    err = np.abs(avg-mean)
    err_mean = np.mean(err, axis=0)

    result = np.vstack([result, mean])
    res_err = np.vstack([res_err, err_mean])


x = np.arange(1, 8)
y = result

m = 0.0001845854545454548
c = 0.0007937245791245789

plt.xlabel("Light Intensity (mW/m^2)")
plt.ylabel("Signal")
# plt.errorbar((m*x+c)*1000, y[:, 0], res_err[:, 0], color='b', capsize = 3)
# plt.errorbar((m*x+c)*1000, y[:, 1], res_err[:, 1], color='g', capsize = 3)
plt.errorbar((m*x+c)*1000, y[:, 2], res_err[:, 2], color='r', capsize = 3)

plt.savefig("Intensity vs Signal.png")

plt.show()

