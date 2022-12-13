from pydantic import (
    BaseModel,
    PositiveInt,
    conint,
    constr,
    StrictFloat,
    ValidationError
)

import json

class User(BaseModel):

    id: PositiveInt()
    name: constr(min_length=2, max_length=20)
    age: conint(gt=0, lt=100)
    address: str
    height: StrictFloat()


if __name__=="__main__":
    user = {
        "id": 123, 
        "name": "David", 
        "age": 30, 
        "address": "10 Fake St, Fakesville, 1234",
        "height": 180.3
    }
    user = User(**user)

    try:
        bad_user = {
            "id": -5, 
            "name": "David Hasalonglastname", 
            "age": 101, 
            "address": "10 Fake St, Fakesville, 1234",
            "height": 180
        }
        bad_user = User(**bad_user)
    except ValidationError as e:
        for error in json.loads(e.json()):
            print(f"{error['loc'][0]}: {error['msg']}")

# Outputs:
# id: ensure this value is greater than 0
# name: ensure this value has at most 20 characters
# age: ensure this value is less than 100
# height: value is not a valid float
