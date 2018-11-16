import json

def write_standard_file(file_name):
    pass

def update_steps(file_name, steps):
    with open(file_name, "r+w") as f:
        dic = json.loads(f.read())
        dic["steps"] = steps
        f.seek(0)
        f.write(json.dumps(dic))
        f.truncate()
    return
    
def read_json(file_name):
    with open(file_name) as f:
        dic = json.loads(f.read())
        return (dic["nailsx"], dic["nailsy"], dic["steps_done"], dic["two_sided_nail"], dic["color_scheme"], dic["steps"], dic["picture_file"])

def get_steps(file_name):
    with open(file_name) as f:
        return json.loads(f.read())["steps"]
