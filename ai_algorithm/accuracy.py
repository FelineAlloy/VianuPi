import numpy as np

# load the verification data 
ver = np.loadtxt('verification.csv', delimiter=',', dtype=np.uint16)
ver = np.transpose(ver)

# load the AI predictions
pred = np.loadtxt('output.txt', delimiter=' ', dtype=np.uint16)
pred = np.transpose(pred)

# only keep the predictions for images we have manualy verified
mask = np.isin(pred[0, :], ver[0, :])
pred = pred[:, mask]

ver = np.transpose(ver)
pred = np.transpose(pred)

# remove image indecies
ver = ver[:, 1:]
pred = pred[:, 1:]

# see how many of the manualy assigned tags are present in the predictions for each image
nr = np.sum((ver[:, :, None] == pred[:, None, :]).any(-1))

# Give a weight of 1/2 for each tag identified correctly and find the accuracy percentage.
# We give a weight of 1/2 since each manualy reviewed image was assigned 2 tags
accuracy = 1/2 * nr / ver.shape[0]