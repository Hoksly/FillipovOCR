from parsing.parser import Parser
from Collection import RawImage
import os

if __name__ == '__main__':

    images = os.listdir('testCollection')

    print(images)
    objs = []
    par = Parser()
    for image_name in images:
        print(image_name)
        res = par.parseAndConvert('testCollection/' + image_name)
        objs.extend(res)

    for i in range(len(objs)):
        objs[i].save('images/img' + str(i) + '.png')
