from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class MapSizeRequest(_message.Message):
    __slots__ = ("width", "height")
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    width: int
    height: int
    def __init__(self, width: _Optional[int] = ..., height: _Optional[int] = ...) -> None: ...

class MapSizeReply(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class SecondForTimerRequest(_message.Message):
    __slots__ = ("timeSecond",)
    TIMESECOND_FIELD_NUMBER: _ClassVar[int]
    timeSecond: int
    def __init__(self, timeSecond: _Optional[int] = ...) -> None: ...

class SecondForTimerReply(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class NbplayerRequest(_message.Message):
    __slots__ = ("nbPlayers",)
    NBPLAYERS_FIELD_NUMBER: _ClassVar[int]
    nbPlayers: int
    def __init__(self, nbPlayers: _Optional[int] = ...) -> None: ...

class NbplayerReply(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class StartGameRequest(_message.Message):
    __slots__ = ("isStarting",)
    ISSTARTING_FIELD_NUMBER: _ClassVar[int]
    isStarting: int
    def __init__(self, isStarting: _Optional[int] = ...) -> None: ...

class StartGameReply(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class InscriptionRequest(_message.Message):
    __slots__ = ("name", "role")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    name: str
    role: str
    def __init__(self, name: _Optional[str] = ..., role: _Optional[str] = ...) -> None: ...

class InscriptionReply(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class MoveRequest(_message.Message):
    __slots__ = ("name", "direction")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DIRECTION_FIELD_NUMBER: _ClassVar[int]
    name: str
    direction: str
    def __init__(self, name: _Optional[str] = ..., direction: _Optional[str] = ...) -> None: ...

class MoveReply(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...
