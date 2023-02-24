from dataclasses import dataclass

@dataclass
class IMSVariable:
    variable_code: str
    unit: str
    description: str
    
    def __repr__ (self) -> str:
        return f"Code: {self.variable_code} - Unit: ({self.unit}) - Description: {self.description}"
