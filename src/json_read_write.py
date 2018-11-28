import json

str_steps = "steps"
str_nailsx = "nailsx"
str_nailsy = "nailsy"
str_steps_done = "steps_done"
str_two_sided_nail = "two_sided_nail"
str_color_scheme = "color_scheme"
str_picture_file = "picture_file"

def write_standard_file(file_name):
    """Create a new .json-file with some input of user parameters and some standard ones."""
    pass

def get_steps(file_name):
    """Only load the steps of the .json-file."""
    with open(file_name) as f:
        return json.loads(f.read())[str_steps]

def update_steps(file_name, steps):
    """The steps are updated in the .json file with new ones."""
    with open(file_name, "r+w") as f:
        dic = json.loads(f.read())
        dic[str_steps] = steps
        f.seek(0)
        f.write(json.dumps(dic))
        f.truncate()
    return
    
def read_json(file_name):
    """Read and return the .json-file's parameters."""
    with open(file_name) as f:
        dic = json.loads(f.read())
        return (dic[str_nailsx], dic[str_nailsy], dic[str_steps_done], dic[str_two_sided_nail], dic[str_color_scheme], dic[str_steps], dic[str_picture_file])

def write(file_name, nailsx, nailsy, steps_done, two_sided_nail, color_scheme, steps, picture_file):
    """Update all parameters into the .json-file."""
    with open(file_name, "w+") as f:
        f.seek(0)
        dic = dict()
        dic[str_nailsx] = nailsx
        dic[str_nailsy] = nailsy
        dic[str_steps_done] = steps_done
        dic[str_two_sided_nail] = two_sided_nail
        dic[str_color_scheme] = color_scheme
        dic[str_steps] = steps
        dic[str_picture_file] = picture_file
        f.write(json.dumps(dic))
        f.truncate()
