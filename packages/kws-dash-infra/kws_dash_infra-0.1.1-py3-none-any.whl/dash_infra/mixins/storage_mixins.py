from dash.dependencies import Input


class StorageMixin(object):
    def add_storage_output(self, storage, key=None):
        storage.create_storage_callback(self, key)

    def use_storage_inputs(self, storage, *keys):
        self.dash_inputs += [
            Input(storage.storage_key(key), "children") for key in keys
        ]
        storage.add_deserializer(self)
