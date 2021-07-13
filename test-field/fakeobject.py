__all__ = ["FakeObject"]
class FakeObject(str):
    def __init__(self,string):
        self.string = string