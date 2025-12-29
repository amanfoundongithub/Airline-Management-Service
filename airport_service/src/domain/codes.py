from dataclasses import dataclass

@dataclass(frozen = True)
class IATACode:
    value : str

    def __post_init__(self):
        if len(self.value) != 3 or not self.value.isalpha():
            raise ValueError(f"The IATA Code {self.value} is not valid.")
        object.__setattr__(self, "value", self.value.upper())

@dataclass(frozen = True)
class ICAOCode:
    value : str

    def __post_init__(self):
        if len(self.value) != 4 or not self.value.isalpha():
            raise ValueError(f"The ICAO Code {self.value} is not valid.")
        object.__setattr__(self, "value", self.value.upper())