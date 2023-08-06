from dash_infra import Callback
from dash_infra.mixins.storage_mixins import StorageMixin


class StorageCallback(Callback, StorageMixin):
    pass


@StorageCallback.as_callback
def square(x):
    return x ** 2


@StorageCallback.as_callback
def cube(x):
    return x ** 3


@StorageCallback.as_callback
def square_root(x):
    return x ** (1 / 2)


@StorageCallback.as_callback
def sum_callback(*args):
    return sum(args)
