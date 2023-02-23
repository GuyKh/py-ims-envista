class IMSVariable:
    def __init__(self, variable_code: str, unit: str, description: str):
        self.variable_code = variable_code
        self.unit = unit
        self.description = description

    def __repr__ (self) -> str:
        return f"Code: {self.variable_code} - Unit: ({self.unit}) - Description: {self.description}"
