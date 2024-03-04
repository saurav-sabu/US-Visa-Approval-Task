import sys


class TargetValueMapping:
    def __init__(self) -> None:
        self.Certified = 0
        self.Denied = 1

    def _asdict(self):
        return self.__dict__
    
    def reverse_mapping(self):
        mapping_response = self._asdict()
        return dict(zip(mapping_response.values(),mapping_response.keys()))