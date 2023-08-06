import yaml

class config:
    def __init__(self, filename):
        with open(filename) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            self.global_data = data["global_data"]
            self.data = data["data"]
            self.inputs = data["inputs"]

    def update(self, filename):
        with open(filename) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            if "global_data" in data:
                self.global_data = data["global_data"]
            if "data" in data:
                self.data = data["data"]
            if "inputs" in data:
                self.inputs = data["inputs"]
