from skimage.color import rgb2gray
import numpy as np
import cv2
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from scipy import ndimage

def regionbased(image):
	gray = rgb2gray(image)
	gray_r = gray.reshape(gray.shape[0]*gray.shape[1])
	for i in range(gray_r.shape[0]):
		if gray_r[i] > gray_r.mean():
			gray_r[i] = 1
		else:
			gray_r[i] = 0
	gray = gray_r.reshape(gray.shape[0],gray.shape[1])
	plt.imshow(gray, cmap='gray')

def regionbased1(image):
	gray = rgb2gray(image)
	gray_r = gray.reshape(gray.shape[0]*gray.shape[1])
	for i in range(gray_r.shape[0]):
		if gray_r[i] > gray_r.mean():
			gray_r[i] = 3
		elif gray_r[i] > 0.5:
			gray_r[i] = 2
		elif gray_r[i] > 0.25:
			gray_r[i] = 1
		else:
			gray_r[i] = 0
	gray = gray_r.reshape(gray.shape[0],gray.shape[1])
	plt.imshow(gray, cmap='gray')

def kmeansbased(image):
	resize=image/255
	resize=resize.reshape(pic_n.shape[0]*pic_n.shape[1], pic_n.shape[2])
	kmeans = KMeans(n_clusters=7, random_state=0).fit(pic_n)
	final = kmeans.cluster_centers_[kmeans.labels_]
	cluster_pic = final.reshape(image.shape[0], image.shape[1], image.shape[2])
	plt.imshow(cluster_pic)
	