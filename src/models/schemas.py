from pydantic import BaseModel

class PropertyFeatures(BaseModel):
    Transaction: str
    Furnishing: str
    Bathroom: int
    Price_per_Sqft: float
    Total_Area: float
    Covered_parking: int
    Open_parking: int
    Possession_Status: str
    BHK: int
