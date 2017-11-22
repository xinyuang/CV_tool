#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 13:22:08 2017

@author: DensoML
"""

#Getting the coefficients of the polynomial
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from skimage import io
from collections import deque
from moviepy.editor import VideoFileClip
import sklearn.preprocessing

src_points = np.float32([[0 , 690],
                         [1150 , 670],
                         [750 , 425],
                         [530 , 425]])
dst_points = np.float32([[300 , 700],
                         [900 , 700],
                         [900 , 0],
                         [300 , 0]])
# Storing our averages
prev_frames = []
prev_curvatures = []
prev_car_off = []

def region_of_interest(img,vertices):
    #defining a blank mask to start with
    mask = np.zeros_like(img)   

    #defining a 3 channel or 1 channel color to fill the mask with depending on the input image
    if len(img.shape) > 2:
        channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255
        
    #filling pixels inside the polygon defined by "vertices" with the fill color    
    cv2.fillPoly(mask, vertices, ignore_mask_color)
    
    #returning the image only where mask pixels are nonzero
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image

def applyTransformation(img):
    # Given src and dst points, calculate the perspective transform matrix
    M = cv2.getPerspectiveTransform(src_points, dst_points)

    # Warp the image using OpenCV warpPerspective()
    transformed = cv2.warpPerspective(img, M, (img.shape[1], img.shape[0]))
    
    # Return transformed image
    return transformed

def abs_sobel_thresh(img, orient='x', thresh_min=0, thresh_max=255):
    # Apply x or y gradient with the OpenCV Sobel() function
    # and take the absolute value
    if orient == 'x':
        abs_sobel = np.absolute(cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3))
    if orient == 'y':
        abs_sobel = np.absolute(cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3))
    # Rescale back to 8 bit integer
    scaled_sobel = np.uint8(255*abs_sobel/np.max(abs_sobel))
    # Create a copy and apply the threshold
    binary_output = np.zeros_like(scaled_sobel)
    # Here I'm using inclusive (>=, <=) thresholds, but exclusive is ok too
    binary_output[(scaled_sobel >= thresh_min) & (scaled_sobel <= thresh_max)] = 1

    # Return the result
    return binary_output

def mag_thresh(img, thresh_min=0, thresh_max=255):
    # Take both Sobel x and y gradients
    sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=9)
    sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=9)
    # Calculate the gradient magnitude
    gradmag = np.sqrt(sobelx**2 + sobely**2)
    # Rescale to 8 bit
    scale_factor = np.max(gradmag)/255 
    gradmag = (gradmag/scale_factor).astype(np.uint8) 
    # Create a binary image of ones where threshold is met, zeros otherwise
    binary_output = np.zeros_like(gradmag)
    binary_output[(gradmag >= thresh_min) & (gradmag <= thresh_max)] = 1

    # Return the binary image
    return binary_output

def applySobelMask(img):
    # Convert to HLS and extract L and S channel
    hls = cv2.cvtColor(img, cv2.COLOR_RGB2HLS)
    l_channel = hls[:,:,1]
    s_channel = hls[:,:,2]
    
    # Apply sobel in x direction on L and S channel
    l_channel_sobel_x = abs_sobel_thresh(l_channel,'x', 20, 200)
    s_channel_sobel_x = abs_sobel_thresh(s_channel,'x', 60, 200)
    sobel_combined_x = cv2.bitwise_or(s_channel_sobel_x, l_channel_sobel_x)
    
    # Apply magnitude sobel
    l_channel_mag = mag_thresh(l_channel, 80, 200)
    s_channel_mag = mag_thresh(s_channel, 80, 200)
    mag_combined = cv2.bitwise_or(l_channel_mag, s_channel_mag)
    
    # Combine all the sobel filters
    mask_combined = cv2.bitwise_or(mag_combined, sobel_combined_x)
    
    # Mask out the desired image and filter image again
#    mask_combined = region_of_interest(mask_combined, np.array([[(330, 0),(950, 0), (950, 680), (330, 680)]]))
    #mask_combined = region_of_interest(mask_combined, np.array([[(330, 0),(950, 0), (950, 680), (330, 680)]]))
    
    # Return the sobel mask
    return mask_combined

def applyColorMask(img):
    # Convert to HLS and extract S and V channel
    img_hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    # Define color thresholds in HSV
    white_low = np.array([[[0, 0, 210]]])
    white_high = np.array([[[255, 30, 255]]])

    yellow_low = np.array([[[18, 80, 80]]])
    yellow_high = np.array([[[30, 255, 255]]])

    # Apply the thresholds to get only white and yellow
    white_mask = cv2.inRange(img_hsv, white_low, white_high)
    yellow_mask = cv2.inRange(img_hsv, yellow_low, yellow_high)

    # Bitwise or the yellow and white mask
    color_mask = cv2.bitwise_or(yellow_mask, white_mask)
    return color_mask

def combineMasks(sobel_mask, color_mask):
    mask_combined = np.zeros_like(sobel_mask)
    mask_combined[(color_mask>=.5)|(sobel_mask>=.5)] = 1
    return mask_combined

def window_mask(width, height, img_ref, center,level):
    output = np.zeros_like(img_ref)
    output[int(img_ref.shape[0]-(level+1)*height):int(img_ref.shape[0]-level*height),max(0,int(center-width/2)):min(int(center+width/2),img_ref.shape[1])] = 1
    return output

def slidingWindow(img):
    # Window settings
    window_width = 50
    window_height = 100
    # How much to slide left and right for searching
    margin = 30
    
    # Store the (left,right) window centroid positions per level
    window_centroids = [] 
    # Create our window template that we will use for convolutions
    window = np.ones(window_width) 
    
    # Find the starting point for the lines
    l_sum = np.sum(img[int(3*img.shape[0]/5):,:int(img.shape[1]/2)], axis=0)
    l_center = np.argmax(np.convolve(window,l_sum))-window_width/2
    r_sum = np.sum(img[int(3*img.shape[0]/5):,int(img.shape[1]/2):], axis=0)
    r_center = np.argmax(np.convolve(window,r_sum))-window_width/2+int(img.shape[1]/2)
    
    # Add what we found for the first layer
    window_centroids.append((l_center,r_center))
    
    # Go through each layer looking for max pixel locations
    for level in range(1, (int)(img.shape[0] / window_height)):
        # convolve the window into the vertical slice of the image
        image_layer = np.sum(img[int(img.shape[0]-(level+1)*window_height):int(img.shape[0]-level*window_height),:], axis=0)
        conv_signal = np.convolve(window, image_layer)
        # Use window_width/2 as offset because convolution signal reference is at right side of window, not center of window
        offset = window_width / 2
        # Find the best left centroid by using past left center as a reference
        l_min_index = int(max(l_center+offset-margin,0))
        l_max_index = int(min(l_center+offset+margin,img.shape[1]))
        l_center = np.argmax(conv_signal[l_min_index:l_max_index])+l_min_index-offset
        # Find the best right centroid by using past right center as a reference
        r_min_index = int(max(r_center+offset-margin,0))
        r_max_index = int(min(r_center+offset+margin,img.shape[1]))
        r_center = np.argmax(conv_signal[r_min_index:r_max_index])+r_min_index-offset
        # Add what we found for that layer
        window_centroids.append((l_center,r_center))
    
    # If we have found any window centers, print error and return
    if len(window_centroids) == 0:
        print("No windows found in this frame!")
        return
    
    # Points used to draw all the left and right windows
    l_points = np.zeros_like(img)
    r_points = np.zeros_like(img)

    # Go through each level and draw the windows
    for level in range(0,len(window_centroids)):
        # Window_mask is a function to draw window areas
        l_mask = window_mask(window_width,window_height,img,window_centroids[level][0],level)
        r_mask = window_mask(window_width,window_height,img,window_centroids[level][1],level)
        # Add graphic points from window mask here to total pixels found 
        l_points[(l_points == 255) | ((l_mask == 1) ) ] = 255
        r_points[(r_points == 255) | ((r_mask == 1) ) ] = 255

    # Draw the results
    template = np.array(r_points+l_points,np.uint8) # add both left and right window pixels together
    zero_channel = np.zeros_like(template) # create a zero color channle 
    template = np.array(cv2.merge((template, template, template)),np.uint8) # make window pixels green
    warpage = np.array(cv2.merge((img, img, img)),np.uint8) # making the original road pixels 3 color channels
    output = cv2.addWeighted(warpage, 1, template, 0.5, 0.0) # overlay the orignal road image with window results
    
    # Extract left and right line pixel positions
    leftx = np.nonzero(l_points)[1]
    lefty = np.nonzero(l_points)[0]
    rightx = np.nonzero(r_points)[1]
    righty = np.nonzero(r_points)[0]
            
    # Fit a second order polynomial to each
    left_fit = np.polyfit(lefty, leftx, 2)
    right_fit = np.polyfit(righty, rightx, 2)
    
    # Return left and right lines as well as the image
    return left_fit, right_fit, output

def applyBackTrans(img, left_fit, right_fit):
    ploty = np.linspace(0, 719, num=720)
    # Calculate left and right x positions
    left_fitx = left_fit[0]*ploty**2 + left_fit[1]*ploty + left_fit[2]
    right_fitx = right_fit[0]*ploty**2 + right_fit[1]*ploty + right_fit[2]
    
    # Defining a blank mask to start with
    polygon = np.zeros_like(img) 

    # Create an array of points for the polygon
    plot_y = np.linspace(0, img.shape[0]-1, img.shape[0])
    pts_left = np.array([np.transpose(np.vstack([left_fitx, plot_y]))])
    #print(pts_left.shape)
    pts_right = np.array([np.flipud(np.transpose(np.vstack([right_fitx, plot_y])))])
    pts = np.hstack((pts_left, pts_right))

    # Draw the polygon in blue
    cv2.fillPoly(polygon, np.int_([pts]), (0, 0, 255))
    #cv2.line(polygon, np.int(left_fitx[0],plot_y[0]),np.int(left_fitx[1],plot_y[1]), color=(255,0,0), thickness=2)
    #cv2.line(polygon, pts_right, color=(0,0,255), thickness=2)
    #cv2.polylines(polygon, np.int_([pts]), isClosed=False, color=(0,0,255), thickness = 20)
    # Calculate top and bottom distance between the lanes
#    top_dist = right_fitx[0] - left_fitx[0]
#    bottom_dist = right_fitx[-1] - left_fitx[-1]
#    
#    # Add the polygon to the list of last frames if it makes sense
#    if len(prev_frames) > 0: 
#        if top_dist < 300 or bottom_dist < 300 or top_dist > 500 or bottom_dist > 500:
#            polygon = prev_frames[-1]
#        else:
#            prev_frames.append(polygon)
#    else:
#        prev_frames.append(polygon)
#        
#    # Check that the new detected lane is similar to the one detected in the previous frame
#    polygon_gray = cv2.cvtColor(polygon, cv2.COLOR_RGB2GRAY) 
#    prev_gray = cv2.cvtColor(prev_frames[-1], cv2.COLOR_RGB2GRAY)  
#    non_similarity = cv2.matchShapes(polygon_gray,prev_gray, 1, 0.0)
#    if non_similarity > 0.002: 
#        polygon = prev_frames[-1]

    # Calculate the inverse transformation matrix
    #M_inv = cv2.getPerspectiveTransform(dst_points, src_points)

    # Warp the blank back to original image space using inverse perspective matrix (Minv)
    #image_backtrans = cv2.warpPerspective(polygon, M_inv, (img.shape[1], img.shape[0])) 
    #image_backtrans = cv2.warpPerspective(polygon, M_inv, (img.shape[1], img.shape[0])) 
    
    # Return the 8-bit mask
    return np.uint8(polygon)

def findLanes(img):   
    # Copy and crop the image
    img_cropped = np.copy(img)
    img_cropped = region_of_interest(img, [src_points.astype(np.int32)])
    
    # Apply image transformation
    img_warped = applyTransformation(img_cropped)
    
    # Apply the sobel mask to the image
    img_sobel = applySobelMask(img_warped)
    
    # Apply the color mask to the image
    img_color = applyColorMask(img_warped)
    
    # Combine color and sobel mask
    img_mask = combineMasks(img_sobel, img_color)
    
    # Find the lines from polyfit
    left_fit, right_fit, _ = slidingWindow(img_mask)
    
    # Create the lane mask and apply backtransformation
    lane_mask = applyBackTrans(img, left_fit, right_fit)
    
    # Combine the sample image with the lane layer
    img_result = cv2.addWeighted(img, 1, lane_mask, 1, 0)
    
    # Add the information for the image
    #img_info = displayInfo(img_result)
    
    return img_result

def resize_img(img):
    height, width = img.shape[:2]
    img = cv2.resize(img,(1280,720), interpolation = cv2.INTER_CUBIC)
    return img

for i in range(0,74):
    img = io.imread('test/cropped_'+str(i)+'_broad.jpg')
    #img = io.imread('/home/spc/lane_detection/image1.jpg')
    img_resize = resize_img(img)
    #img_cropped = region_of_interest(img_resize, [src_points.astype(np.int32)])
    #img_warped = applyTransformation(img_cropped)
    img_sobel = applySobelMask(img_resize)
    img_color = applyColorMask(img_resize)
    img_mask = combineMasks(img_sobel, img_color)
    left_fit, right_fit, _ = slidingWindow(img_mask)
    #left_norm = sklearn.preprocessing.normalize((left_fit), norm='l2', axis=1, return_norm=False)
    #right_norm = sklearn.preprocessing.normalize((right_fit), norm='l2', axis=1, return_norm=False)
#    left_norm = np.array(left_norm)
#    right_norm = np.array(right_norm)
    a = np.sqrt(np.square(left_fit[0]) + np.square(left_fit[1]) + np.square(left_fit[2]))
    b = np.sqrt(np.square(right_fit[0]) + np.square(right_fit[1]) + np.square(right_fit[2]))
    left_norm = np.array(left_fit)/a
    right_norm = np.array(right_fit)/b
    lane_mask = applyBackTrans(img_resize, left_fit, right_fit)
    img_result = cv2.addWeighted(img_resize, 1, lane_mask, 1, 0)
    plt.imshow(img_result)
    #plt.show(img_result)   
    plt.show()
