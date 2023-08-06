import json

class JSONSerializer(object):
    def data_frame_to_json(self, data_frame):
        return data_frame.to_json()


    def numpy_to_json(self, array):
        return json.dumps({"data": array.tolist()})
