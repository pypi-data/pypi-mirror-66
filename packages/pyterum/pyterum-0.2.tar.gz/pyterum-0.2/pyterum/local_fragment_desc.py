from __future__ import annotations
from typing import List

class LocalFileDesc:
    def __init__(self, name:str, path:str):
        self.name = name
        self.path = path

    def to_json(self) -> dict:
        return self.__dict__

    @classmethod
    def from_json(cls, d:dict) -> cls:
        if not isinstance(d, dict):
            raise TypeError("Argument 'd' is not of type 'dict'")
        result = cls("", "")
        for key in result.__dict__.keys():
            result.__setattr__(key, d[key])
        return result

class LocalFragmentDesc:
    def __init__(self, files:List[LocalFileDesc]):
        self.files = files
    
    def to_json(self) -> dict:
        result = {}
        for key in self.__dict__.keys():
            result[key] = self.__dict__[key]
        result["files"] = [f.to_json() for f in self.files]
        return result

    @classmethod
    def from_json(cls, d:dict) -> cls:
        if not isinstance(d, dict):
            raise TypeError("Argument 'd' is not of type 'dict'")
        result = cls([])
        for key in result.__dict__.keys():
            result.__setattr__(key, [LocalFileDesc.from_json(f) for f in d[key]])
        return result