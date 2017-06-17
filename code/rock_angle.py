import numpy as np
import cv2
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

example2 = "../calibration_images/example_rock2.jpg"

example1 = "../calibration_images/example_rock1.jpg"

example3 = "../calibration_images/test3.jpg"

example4 = "../calibration_images/test4.jpg"

image1 = mpimg.imread(example1)
image2 = mpimg.imread(example2)
image3 = mpimg.imread(example3)
image4 = mpimg.imread(example4)

image = image3
	
def find_rock(img, rgb_thresh=(100,100,76)):
	color_select = np.zeros_like(img[:,:,0])
	rock_thresh = (img[:,:,0] > rgb_thresh[0]) \
                & (img[:,:,1] > rgb_thresh[1]) \
                & (img[:,:,2] <= rgb_thresh[2])
	color_select[rock_thresh] = 1
	return color_select

def rover_coords(binary_img):
    # Identify nonzero pixels
    ypos, xpos = binary_img.nonzero()
    # Calculate pixel positions with reference to the rover position being at the 
    # center bottom of the image.  
    x_pixel = np.absolute(ypos - binary_img.shape[0]).astype(np.float)
    y_pixel = -(xpos - binary_img.shape[0]).astype(np.float)
    return x_pixel, y_pixel

# codes copied from jupyter notebook for perspect_transform
def perspect_transform(img, src, dst):
           
    M = cv2.getPerspectiveTransform(src, dst)
    warped = cv2.warpPerspective(img, M, (img.shape[1], img.shape[0]))# keep same size as input image
    
    return warped
	
def to_polar(xpix, ypix):
	dist = np.sqrt(xpix ** 2 - ypix ** 2)
	angles = np.arctan2(ypix, xpix)
	return dist, angles

# codes for testing the result using the perspect transformed image as input

dst_size = 5

bottom_offset = 6
source = np.float32([[14, 140], [301 ,140],[200, 96], [118, 96]])
destination = np.float32([[image.shape[1]/2 - dst_size, image.shape[0] - bottom_offset],
                  [image.shape[1]/2 + dst_size, image.shape[0] - bottom_offset],
                  [image.shape[1]/2 + dst_size, image.shape[0] - 2*dst_size - bottom_offset], 
                  [image.shape[1]/2 - dst_size, image.shape[0] - 2*dst_size - bottom_offset],
                  ])

# codes for testing the result using image as input
warped = perspect_transform(image, source, destination)
rock = find_rock(warped)
xpix, ypix = rover_coords(rock)
dist, angle = to_polar(xpix, ypix)
avgAngle = np.mean(angle)

fig = plt.figure(figsize=(12,9))
plt.subplot(221)
plt.imshow(image)
plt.subplot(222)
plt.imshow(warped)
plt.subplot(223)
plt.imshow(rock, cmap='gray')
plt.subplot(224)
plt.plot(xpix, ypix, '.')
plt.ylim(-160, 160)
plt.xlim(0, 160)
arrow_length = 100
x_arrow = arrow_length * np.cos(avgAngle)
y_arrow = arrow_length * np.sin(avgAngle)
plt.arrow(0, 0, x_arrow, y_arrow, color='red', zorder=2, head_width=10, width=2)
plt.show()