import os
from PIL import Image
import numpy as np
import argparse
import random
import math
import turtle
import matplotlib.pyplot as plt
from skimage.draw import random_shapes
from skimage import data, color


def generate_dotted_image_and_mask(image_size,number_of_shapes,overlap,file_name):

    image,labels = random_shapes((image_size, image_size),
                                max_shapes=number_of_shapes,
                                shape='circle', multichannel=True,
                                num_channels=3, min_size=15, max_size=30,
                                allow_overlap=overlap)

    centers = [item[:][1] for item in labels]
    centers_x = [(item[0][0]+item[0][1])/2 for item in centers]
    centers_y = [(item[1][0]+item[1][1])/2 for item in centers]


    mask_name = 'mask_'+str(file_name)+'.png'
    image_name = 'image_'+str(file_name)+'.png'

    fig = plt.figure(figsize=(15,15))
    ax = fig.add_subplot(111)
    ax.imshow(image)
    ax.axis([0,1500,0,1500])
    ax.axis('off')
    fig.savefig('/home/native/projects/DeepDot/generate_dots/data/'+image_name)

    fig_scatter = plt.figure(figsize=(15,15))
    ax_scatter = fig_scatter.add_subplot(111)
    ax_scatter.scatter(centers_y,centers_x,color='k',s=2)
    ax_scatter.axis([0,1500,0,1500])
    ax_scatter.axis('off')
    fig_scatter.savefig('/home/native/projects/DeepDot/generate_dots/masks/'+mask_name)

    fig.canvas.draw()
    fig_size_inches = [int(x) for x in fig.get_size_inches()]
    fig_dpi = int(fig.get_dpi())
    width,height = np.asarray(fig_size_inches)*fig_dpi
    mplimage = np.fromstring(fig.canvas.tostring_rgb(),dtype='uint8')
    mplimage = mplimage.reshape(height,width,3)


    fig_scatter.canvas.draw()
    fig_scatter_size_inches = [int(x) for x in fig_scatter.get_size_inches()]
    fig_scatter_dpi = int(fig_scatter.get_dpi())
    width_scatter,height_scatter = np.asarray(fig_scatter_size_inches)*fig_scatter_dpi
    mplimage_scatter = np.fromstring(fig_scatter.canvas.tostring_rgb(),dtype='uint8')
    mplimage_scatter = mplimage_scatter.reshape(height_scatter,width_scatter,3)
    gray_image_scatter = color.rgb2gray(mplimage_scatter).reshape(height_scatter,width_scatter,1)

    print("dots image shpae:{}".format(mplimage.shape))
    print("mask image shpae:{}".format(gray_image_scatter.shape))

    image_with_mask = np.dstack((mplimage,gray_image_scatter))
    print("image with mask shape:{}".format(image_with_mask.shape))



    ## show combined image
    # fig_combined = plt.figure(figsize=(15,15))
    # ax_combined = fig_combined.add_subplot(111)
    # ax_combined.imshow(image)
    # ax_combined.scatter(centers_y,centers_x,color='k',s=2)
    # ax_combined.axis([0,1500,0,1500])
    # ax_combined.axis('off')
    # fig_combined.show()
    # plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Main function')
    parser.add_argument('--num-imgs',type=int,help='number of images to generate')
    parser.add_argument('--img-size',type=int,help='Dimensions of images')
    opts = parser.parse_args()

    number_of_images = opts.num_imgs
    img_size = opts.img_size
    for i in range(number_of_images):
        generate_dotted_image_and_mask(image_size=img_size,
                                        number_of_shapes=1000,
                                        overlap=False, file_name=i)
