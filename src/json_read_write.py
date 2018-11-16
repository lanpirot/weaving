import json

def write_standard_file():
    #json.dumps()
    return
    
def read_json(file_name):
    with open(file_name) as f:
        dic = json.loads(f.read())
        return (dic["nailsx"], dic["nailsy"], dic["two_sided_nail"], dic["color_scheme"], dic["steps"], dic["picture_file"])
