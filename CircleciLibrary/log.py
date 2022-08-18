from robot.libraries.BuiltIn import BuiltIn

def trace(obj, level="TRACE"):
    BuiltIn().log(str(obj), level=level)
    return obj