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
    print("\n", user.dict(), sep="")
    print(user.json())

# Output:
# Ordinary User class
# id: <class 'int'> = 123, name: <class 'str'> = John Doe
# id: <class 'str'> = 123, name: <class 'str'> = John Doe
# id: <class 'float'> = 123.45, name: <class 'str'> = John Doe
# id: <class 'bool'> = True, name: <class 'str'> = John Doe
# id: <class 'tuple'> = (1, 2, 3), name: <class 'str'> = John Doe
# id: <class 'int'> = 123, name: <class 'str'> = David
# id: <class 'int'> = 123, name: <class 'int'> = 1
# id: <class 'int'> = 123, name: <class 'bool'> = True
# id: <class 'int'> = 123, name: <class 'tuple'> = (1, 2, 3)

# Pydantic User class
# id: <class 'int'> = 123, name: <class 'str'> = John Doe
# id: <class 'int'> = 123, name: <class 'str'> = John Doe
# id: <class 'int'> = 123, name: <class 'str'> = John Doe
# id: <class 'int'> = 1, name: <class 'str'> = John Doe
# id: value is not a valid integer
# id: <class 'int'> = 123, name: <class 'str'> = David
# id: <class 'int'> = 123, name: <class 'str'> = 1
# id: <class 'int'> = 123, name: <class 'str'> = True
# name: str type expected

# {'id': 123, 'name': 'David'}
# {"id": 123, "name": "David"}