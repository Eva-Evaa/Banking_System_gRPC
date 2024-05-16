from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class BankingReply(_message.Message):
    __slots__ = ["interface", "result", "money", "writeset"]
    INTERFACE_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    MONEY_FIELD_NUMBER: _ClassVar[int]
    WRITESET_FIELD_NUMBER: _ClassVar[int]
    interface: str
    result: str
    money: int
    writeset: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, interface: _Optional[str] = ..., result: _Optional[str] = ..., money: _Optional[int] = ..., writeset: _Optional[_Iterable[int]] = ...) -> None: ...

class BankingRequest(_message.Message):
    __slots__ = ["interface", "money", "writeset"]
    INTERFACE_FIELD_NUMBER: _ClassVar[int]
    MONEY_FIELD_NUMBER: _ClassVar[int]
    WRITESET_FIELD_NUMBER: _ClassVar[int]
    interface: str
    money: int
    writeset: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, interface: _Optional[str] = ..., money: _Optional[int] = ..., writeset: _Optional[_Iterable[int]] = ...) -> None: ...
