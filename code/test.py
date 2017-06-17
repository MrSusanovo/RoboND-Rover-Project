import numpy as np
import cv2
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

example2 = "../calibration_images/example_rock2.jpg"

example1 = "../calibration_images/example_rock1.jpg"

image1 = mpimg.imread(example1)
image2 = mpimg.imread(example2)

image = image1
	
def find_rock(img, rgb_thresh=(100,100,76)):
	color_select = np.zeros_like(img[:,:,0])
	rock_thresh = (img[:,:,0] > rgb_thresh[0]) \
                & (img[:,:,1] > rgb_thresh[1]) \
                & (img[:,:,2] <= rgb_thresh[2])
	color_select[rock_thresh] = 1
	return color_select


# codes copied from jupyter notebook for perspect_transform
def perspect_transform(img, src, dst):
           
    M = cv2.getPerspectiveTransform(src, dst)
    warped = cv2.warpPerspective(img, M, (img.shape[1], img.shape[0]))# keep same size as input image
    
    return warped



# codes used for comparing rgb channels

red = np.copy(image)
green = np.copy(image)
blue = np.copy(image)

red[:,:,[1,2]] = 0
green[:,:,[0,2]] = 0
blue[:,:,[0,1]] = 0
fig = plt.figure(figsize=(15,4))
plt.subplot(131)
plt.imshow(red)
plt.subplot(132)
plt.imshow(green)
plt.subplot(133)
plt.imshow(blue)

# codes for testing the result using image as input
rock = find_rock(image)
plt.subplot(131)
plt.imshow(rock, cmap='gray')
plt.subplot(133)
plt.imshow(image)

# codes for testing the result using the perspect transformed image as input

dst_size = 5

bottom_offset = 6
source = np.float32([[14, 140], [301 ,140],[200, 96], [118, 96]])
destination = np.float32([[image.shape[1]/2 - dst_size, image.shape[0] - bottom_offset],
                  [image.shape[1]/2 + dst_size, image.shape[0] - bottom_offset],
                  [image.shape[1]/2 + dst_size, image.shape[0] - 2*dst_size - bottom_offset], 
                  [image.shape[1]/2 - dst_size, image.shape[0] - 2*dst_size - bottom_offset],
                  ])

warped = perspect_transform(image, source, destination)
rock_in_warped = find_rock(warped)
plt.subplot(131)
plt.imshow(rock_in_warped, cmap='gray')
plt.subplot(132)
plt.imshow(warped)

plt.show()
