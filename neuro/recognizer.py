from Collection import RawImage, Node, NodeType


class TypeRecognizer:
    def __init__(self, deepModel):
        self.model = deepModel

    def recognize(self, rawImage: RawImage):
        imageValue = self.model.recognize(rawImage.image)

        return Node(NodeType.UNDEFINED, imageValue, rawImage.imageBox)
