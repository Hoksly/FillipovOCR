from parser import Parser
from Collection import RawImage
import os

if __name__ == '__main__':

    try:
        os.mkdir('images')
    except:
        pass
    
    p = Parser()

    raw_images = p.parseAndConvert('formula2.png')
    foldername = "images/"

    for i in range(len(raw_images)):
        raw_images[i].save(foldername + 'img' + str(i) + '.png')

