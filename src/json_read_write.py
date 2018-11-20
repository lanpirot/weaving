import json

str_steps = "steps"
str_nailsx = "nailsx"
str_nailsy = "nailsy"
str_steps_done = "steps_done"
str_two_sided_nail = "two_sided_nail"
str_color_scheme = "color_scheme"
str_picture_file = "picture_file"

def write_standard_file(file_name):
    pass

def update_steps(file_name, steps):
    with open(file_name, "r+w") as f:
        dic = json.loads(f.read())
        dic[str_steps] = steps
        f.seek(0)
        f.write(json.dumps(dic))
        f.truncate()
    return
    
def read_json(file_name):
    with open(file_name) as f:
        dic = json.loads(f.read())
        return (dic[str_nailsx], dic[str_nailsy], dic[str_steps_done], dic[str_two_sided_nail], dic[str_color_scheme], dic[str_steps], dic[str_picture_file])

def get_steps(file_name):
    with open(file_name) as f:
        return json.loads(f.read())[str_steps]
