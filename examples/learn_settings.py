import os

from pydantic import (
    BaseSettings
)

os.environ["USER_NAME"] = "David"
os.environ["PYD_USER_NAME"] = "Steve"

class Settings_1(BaseSettings):
    user_name: str = "no name"

    class Config:
        case_sensitive = True

class Settings_2(BaseSettings):
    user_name: str = "no name"

    class Config:
        case_sensitive = False

class Settings_3(BaseSettings):
    user_name: str = "no name"

    class Config:
        case_sensitive = False
        env_prefix = "pyd_"

class Settings_4(BaseSettings):
    user_name: str = "no name"
    age: int

    class Config:
        case_sensitive = False
        env_file = ".env"
        # NOTE: environment variables take priority over dotenv file


if __name__=="__main__":

    print(Settings_1().json())
    print(Settings_2().json())
    print(Settings_3().json())
    print(Settings_4().json())

# Output:
# {"user_name": "no name"}
# {"user_name": "David"}
# {"user_name": "Steve"}
# {"user_name": "David", "age": 45}
