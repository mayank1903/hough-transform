import matplotlib.pyplot as plt
import numpy as np
from skimage.color import rgb2gray
from skimage.transform import rotate
from skimage.transform import (hough_line, hough_line_peaks)
from scipy.stats import mode
from skimage import io
from skimage.filters import threshold_otsu, sobel

#plotting the image for the probabilistic hough transform
def plot_image_with_lines_p_hough(image, lines):
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    # Plot the original image
    axes[0].imshow(image, cmap='gray')
    axes[0].set_title('Original Image')
    axes[0].axis('off')

    # Plot the image with detected lines
    axes[1].imshow(image, cmap='gray')
    for line in lines:
        p0, p1 = line
        axes[1].plot((p0[0], p1[0]), (p0[1], p1[1]), 'g')
    axes[1].set_title('Image with Detected Lines')
    axes[1].axis('off')

    plt.show()

#plotting the image for the standard hough transform
def plot_image_with_lines_hough(image, lines):
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    # Plot the original image
    axes[0].imshow(image, cmap='gray')
    axes[0].set_title('Original Image')
    axes[0].axis('off')

    # Plot the image with detected lines
    axes[1].imshow(image, cmap='gray')
    for _, angle, dist in zip(*lines):
        y0 = (dist - 0 * np.cos(angle)) / np.sin(angle)
        y1 = (dist - image.shape[1] * np.cos(angle)) / np.sin(angle)
        axes[1].plot((0, image.shape[1]), (y0, y1), 'r')
    axes[1].set_xlim((0, image.shape[1]))
    axes[1].set_ylim((image.shape[0], 0))
    axes[1].set_title('Image with Detected Lines')
    axes[1].axis('off')

    plt.show()

#document rotation code
def binarizeImage(RGB_image):

  if len(RGB_image.shape) == 3 and RGB_image.shape[2] == 3:
        image = rgb2gray(RGB_image)
  else:
      image = RGB_image  # Assume grayscale image if not 3-channel RGB

  plt.imshow(RGB_image, cmap='gray')
  plt.axis('off')
  plt.title('Original grayscale Edges')
  # plt.savefig('binary_image.png')

  # image = rgb2gray(RGB_image)
  threshold = threshold_otsu(image)
  bina_image = image < threshold
  
  return bina_image

def findEdges(bina_image):
  
  image_edges = sobel(bina_image)

  return image_edges

def findTiltAngle(image_edges):
  
  h, theta, d = hough_line(image_edges)
  accum, angles, dists = hough_line_peaks(h, theta, d)

  angles_mode = mode(angles)
  angle = np.rad2deg(angles_mode.mode)
  
  if (angle < 0):
    
    r_angle = angle + 90
    
  else:
    
    r_angle = angle - 90

  # Plot Image and Lines    
  fig, ax = plt.subplots()
  

  ax.imshow(image_edges, cmap='gray')

  origin = np.array((0, image_edges.shape[1]))

  for _, angle, dist in zip(*hough_line_peaks(h, theta, d)):

    y0, y1 = (dist - origin * np.cos(angle)) / np.sin(angle)
    ax.plot(origin, (y0, y1), '-r')

  ax.set_xlim(origin)
  ax.set_ylim((image_edges.shape[0], 0))
  ax.set_axis_off()
  ax.set_title('Detected lines')

  plt.savefig('hough_lines.png')

  plt.show()
  return r_angle

  
def rotateImage(RGB_image, angle):

  fixed_image = rotate(RGB_image, angle)

  plt.imshow(fixed_image, cmap='gray')
  plt.axis('off')
  plt.title('Fixed Image')
  plt.savefig('fixed_image.png')
  plt.show()

  return fixed_image

def generalPipeline(path):

  img = path

  image = io.imread(img)
  bina_image = binarizeImage(image)
  image_edges = findEdges(bina_image)
  angle = findTiltAngle(image_edges)
  rotateImage(io.imread(img), angle)