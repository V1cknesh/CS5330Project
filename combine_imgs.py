import cv2
import numpy as np 
import glob

ns = [10, 30, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
for i in range(2):
	imgs = []
	for n in ns:
		img = cv2.imread('./result/benchmark_'+str(i)+'_'+str(n)+'.png')
		imgs.append(img)
		h, w = img.shape[:2]
	img = np.asarray(imgs).reshape(4, h*3, w, 3).transpose(1,0,2,3).reshape(h*3, w*4, 3)
	print(img.shape)
	cv2.imshow('', img)
	cv2.waitKey(10)
	cv2.imwrite('./result/benchmark_'+str(i)+'.png', img)



ns = [0.001, 0.01, 0.1, 0.2, 0.5]
for i in range(2, 4):
	imgs = []
	for n in ns:
		img = cv2.imread('./result/benchmark_'+str(i)+'_'+str(n)+'.png')
		imgs.append(img)
		h, w = img.shape[:2]
	img = np.asarray(imgs).reshape(5, h, w, 3).transpose(1,0,2,3).reshape(h, w*5, 3)
	print(img.shape)
	cv2.imshow('', img)
	cv2.waitKey(10)
	cv2.imwrite('./result/benchmark_'+str(i)+'.png', img)