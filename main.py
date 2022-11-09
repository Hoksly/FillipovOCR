from parser import Parser
from Collection import RawImage
import os

if __name__ == '__main__':

    images = os.listdir('samples2')

    print(images)
    objs = []
    par = Parser()
    for image_name in images:
        print(image_name)
        res = par.parseAndConvert('samples2/' + image_name)
        objs.extend(res)

    for i in range(len(objs)):
        objs[i].save('images/img' + str(i) + '.png')
