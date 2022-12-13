from pydantic import (
    BaseModel, 
    ValidationError, 
    validator,
    constr,
)
import json

class User(BaseModel):
    id: int
    first_name: constr(min_length=2, max_length=20)
    last_name: constr(min_length=2, max_length=20)
    age: int
    address: str

    @validator("last_name")
    def frist_and_last_name_not_equal(cls, v, values):
        if "first_name" in values and v == values["first_name"]:
            raise ValueError("first_name cannot be the same as last_name")
        return v

    @validator("address")
    def address_cannot_be_po_box(cls, v, values):
        if any(s in v.lower() for s in ["po box", "pobox", "p.o. box"]):
            raise ValueError("Address cannot be a PO Box")
        return v

if __name__=="__main__":
    user = {
        "id": 123, 
        "first_name": "David", 
        "last_name": "Doe",
        "age": 100,
        "address": "10 Fake St, Fakesville, 1234",
    }
    user = User(**user)

    try:
        bad_user = {
            "id": 123, 
            "first_name": "David", 
            "last_name": "David",
            "age": 100,
            "address": "PO Box 123, Fakesville, 1111",
        }
        bad_user = User(**bad_user)
    except ValidationError as e:
        for error in json.loads(e.json()):
            print(f"{error['loc'][0]}: {error['msg']}")

# Output:
# last_name: first_name cannot be the same as last_name
# address: Address cannot be a PO Box
