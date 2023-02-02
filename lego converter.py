from PIL import Image as im
import cv2
from tqdm import tqdm
import numpy as np

colourlib = [
    [255,255,255],
    [99,52,10],
    [155,143,0],
    [11,233,187],
    [191,174,54],
    [0,0,0]
]
path = 'tardis.jpeg'
dimensions = [80,128]

def modulus(data):
    return (sum([data[i] ** 2 for i in range (0,len(data))])) ** 0.5

def shrink():
    temp = im.open(path)
    temp.thumbnail(dimensions)
    temp.save('temp.png')

def match(input):
    temp = np.array([modulus([input[0] - colourlib[i][0],input[1] - colourlib[i][1],input[2] - colourlib[i][2]]) for i in range (0,len(colourlib))])
    return list(zip((np.where(temp == np.amin(temp)))[0]))[0][0]


def findnearest(image):
    b,g,r = cv2.split(image)
    matched = []
    for i in tqdm(range(len(b))):
        row = [match([b[i][j],g[i][j],r[i][j]]) for j in range (0,len(b[i]))]
        matched.append(row)
    return matched

def render(map):
    bchannel = []
    gchannel = []
    rchannel = []
    for i in range (0,len(map)):
        brow = []
        grow = []
        rrow = []
        for value in map[i]:
            brow.append(colourlib[value][0])
            grow.append(colourlib[value][1])
            rrow.append(colourlib[value][2])
        bchannel.append(brow)
        gchannel.append(grow)
        rchannel.append(rrow)
    return np.array([bchannel,gchannel,rchannel]).astype(np.uint8)


shrink()
temp = cv2.imread('temp.png')
temp = cv2.merge(render(findnearest(temp)))
cv2.imshow('converted',temp)
cv2.waitKey(0)