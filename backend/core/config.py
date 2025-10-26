from dotenv import load_dotenv, find_dotenv
import os

class Config:
    config = None

    def __init__(self):
        load_dotenv(find_dotenv(usecwd=True), override=True)
    
    def get(self, key: str, default = None):
        key = key.upper()
        value = os.getenv(key, default)
        return self.cast_value(value)

    def cast_value(self, value):
        if type(value) == str:
            print(value, value.isdigit())
            if value.lower() in ("true", "false"):
                # If value is true | false then it is boolean
                value = value.lower() == "true"
            elif value.isdigit() or (value.startswith('-') and value[1:].isdigit()):
                # If it is number or negative number then cast to integer
                value = int(value)
            else:
                # If it is none of above types then we check for float type
                # If the value is non-float type then float will raise ValueError 
                # We depend on that to confirm it is float or not
                try:
                    float_value = float(value)
                    value = float_value
                except ValueError:
                    value = value

                # If it is a json string, then parse it to json object
                try:
                    import json
                    json_value = json.loads(value)
                    value = json_value
                except (TypeError, ValueError):
                    value = value
        
        return value

Config = Config()