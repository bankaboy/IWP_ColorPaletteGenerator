
## Initialisation

import pandas as pd
import numpy as np
import cv2 as cv
import random
import math
import sys
import os
import copy

#img_file = sys.argv[1]




#===================
## Assignment Stage
#====================

def assignment(df, centroids):
    for i in centroids.keys():
        # sqrt((x1 - x2)^2 - (y1 - y2)^2)
        df['distance_from_{}'.format(i)] = (
            np.sqrt(
                (df['red'] - centroids[i][0]) ** 2
                + (df['green'] - centroids[i][1]) ** 2
                + (df['blue'] - centroids[i][2]) ** 2
            )
        )
    centroid_distance_cols = ['distance_from_{}'.format(i) for i in centroids.keys()]
    df['closest'] = df.loc[:, centroid_distance_cols].idxmin(axis=1)
    df['closest'] = df['closest'].map(lambda x: int(x.lstrip('distance_from_')))
    return df

#===============
## Update Stage
#===============

def update(df,centroids):
    for i in centroids.keys():
        centroids[i][0] = np.mean(df[df['closest'] == i]['red'])
        centroids[i][1] = np.mean(df[df['closest'] == i]['green'])
        centroids[i][2] = np.mean(df[df['closest'] == i]['blue'])

    return centroids

#================
#MAIN FUCNTION
#================

def color_palette(img_file):
    exists = os.path.isfile(img_file)
    if not exists:
        print("\n===================================================The file you have given does not exits==========================================\n")
        exit()

    img = cv.imread(img_file,1)

    rows = img.shape[0]
    cols = img.shape[1]


    print("\nIMAGE IS %dx%d \n" %(rows,cols))
    red, green, blue = [],[],[]

    for r in range(rows):       # open cv uses bgr
        for c in range(cols):
            red.append(img[r][c][2])  
            green.append(img[r][c][1])
            blue.append(img[r][c][0])

    #%matplotlib inline

    df=pd.DataFrame({'red': red,'green': green,'blue': blue})


    np.random.seed(200)

    k = 10
    centroids = {i+1: [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)] for i in range(k) }
    #k = 10
    # centroids[i] = [x, y, z]

    df = assignment(df, centroids)

    old_centroids = copy.deepcopy(centroids)

    centroids = update(df,centroids)

    for i in old_centroids.keys():
        old_red = old_centroids[i][0]
        old_green = old_centroids[i][1]
        old_blue = old_centroids[i][2]
        dred = (centroids[i][0] - old_centroids[i][0]) * 0.75
        dgreen = (centroids[i][1] - old_centroids[i][1]) * 0.75
        dblue = (centroids[i][1] - old_centroids[i][2]) * 0.75

    ## Repeat Assigment Stage

    df = assignment(df, centroids)

    # Continue until all assigned categories don't change any more
    while True:
        closest_centroids = df['closest'].copy(deep=True)
        centroids = update(df,centroids)
        df = assignment(df, centroids)
        if closest_centroids.equals(df['closest']):
            break

    final_colors = []
    colnum = 1

    #Getting Hec Codes of color

    for centroid in centroids.keys():
        if math.isnan(centroids[centroid][0]):
            continue
    
        r = int(round(centroids[centroid][0]))
        g = int(round(centroids[centroid][1]))
        b = int(round(centroids[centroid][2]))
    
        rhex = hex(int(round(centroids[centroid][0])))[2:]
        ghex = hex(int(round(centroids[centroid][1])))[2:]
        bhex = hex(int(round(centroids[centroid][2])))[2:]
    
        color = "#"+str(rhex)+str(ghex)+str(bhex)+"\n"
        final_colors.append(color)  
        colnum+=1

    print("\n==================================The Colors in the image are=====================================\n")
    
    for color in final_colors:
        print(color+"\n")

    return final_colors






