import yaml

class config:
    def __init__(self, filename):
        with open(filename) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            self.global_data = data["global_data"]
            self.data = data["data"]
            self.inputs = data["inputs"]
