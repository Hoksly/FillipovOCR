from parser import Parser
from Collection import RawImage

if __name__ == '__main__':
    objs = Parser.parseImage("notshackaled.png")

    raw_images = []
    for el in objs:
        raw_images.append(RawImage(el))

    foldername = "images/"

    for i in range(len(raw_images)):
        raw_images[i].save(foldername + 'img' + str(i) + '.png')

