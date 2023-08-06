from google.protobuf.empty_pb2 import Empty
from spaceone.core.pygrpc.message_type import *
from spaceone.api.core.v1 import query_pb2

__all__ = ['EmptyInfo', 'StatisticsInfo']


def EmptyInfo():
    return Empty()


def StatisticsInfo(values):
    return query_pb2.StatisticsInfo(values=change_list_value_type(values))
