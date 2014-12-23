class Crossing:
    def __init__(self):
        self.value_list = dict()
        self.incils = list()

    def add_keyvalue(self, key, value):
        self.value_list[key] = value

    def get_value(self, key):
        if key in self.value_list:
            return self.value_list[key]
        else:
            return None

    def get_inci(self):
        return self.incils

    def set_values(self, values):
        self.value_list = values

    def get_values(self):
        return self.value_list

    # Constructs a python dictionary from
    # dbf field data struct
    def get_dict(self, dbfT):
        ret_d = dict()

        for field_name in dbfT.field_names:
            ret_d[field_name] = self.value_list[field_name]
        return ret_d
        

class Incident:
    def __init__(self):
        self.value_list = dict()
        
    def add_keyvalue(self, key, value):
        self.value_list[key] = value

    def get_value(self, key):
        if key in self.value_list:
            return self.value_list[key]
        else:
            return None
            
    def get_dict(self):
        return self.value_list
