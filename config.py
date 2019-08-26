import pickle


class config:

    def __init__(self, filename):
        self.configs = {}
        try:
            with open(filename, "rb") as fr:
                self.configs = pickle.load(fr)
        except:
            pass

    def set_config(self, field, value):
        self.configs[field] = value
        return self

    def del_config(self, field):
        del self.configs[field]
        return self

    def get_config(self, field):
        try:
            return self.configs[field]
        except:
            return None

    def get_configs(self):
        return self.configs

    def set_configs(self, configs):
        self.configs = configs
        return self

    def save_config(self, filename):
        with open(filename, "wb") as fw:
            fw.write(pickle.dumps(self.configs))
