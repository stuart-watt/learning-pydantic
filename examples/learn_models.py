from pydantic import BaseModel, ValidationError
import json

class User():

    def __init__(self, id: int, name="John Doe"):
        self.id = id
        self.name = name


class PydanticUser(BaseModel):
    id: int
    name = "John Doe"


if __name__ == "__main__":

    # Ordinary python classes will accept any type for the input variables
    print("Ordinary User class")
    for i in [123, "123", 123.45, True, (1, 2, 3)]:
        user = User(id=i)
        print(f"id: {type(user.id)} = {user.id}, name: {type(user.name)} = {user.name}")

    for name in ["David", 1, True, (1, 2, 3)]:
        user = User(id=123, name=name)
        print(f"id: {type(user.id)} = {user.id}, name: {type(user.name)} = {user.name}")

    # Classes inherited from BaseModel will try to ast the inputs to the expected values
    # In this case, id was type hinter to int and name was inferred as str
    # If the input cannot be correctly cast, an error will be raised
    print("\nPydantic User class")
    for i in [123, "123", 123.45, True, (1, 2, 3)]:
        try:
            user = PydanticUser(id=i)
            print(f"id: {type(user.id)} = {user.id}, name: {type(user.name)} = {user.name}")
        except ValidationError as e:
            for error in json.loads(e.json()):
                print(f"{error['loc'][0]}: {error['msg']}")

    for name in ["David", 1, True, (1, 2, 3)]:
        try:
            user = PydanticUser(id=123, name=name)
            print(f"id: {type(user.id)} = {user.id}, name: {type(user.name)} = {user.name}")

        except ValidationError as e:
            for error in json.loads(e.json()):
                print(f"{error['loc'][0]}: {error['msg']}")

    # You can access the class values using the dict or json methods
    user = PydanticUser(id=123, name="David")
    print("\n", user.dict())
    print(user.json())

    print(user.schema())
