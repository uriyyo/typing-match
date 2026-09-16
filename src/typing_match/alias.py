import collections as _collections
import collections.abc as _abc
import contextlib as _contextlib
import datetime as _datetime
import decimal as _decimal
import enum as _enum
import fractions as _fractions
import io as _io
import ipaddress as _ipaddress
import numbers as _numbers
import os as _os
import pathlib as _pathlib
import re as _re
import types as _types
import uuid as _uuid
import zoneinfo as _zoneinfo

bool = bool
bytearray = bytearray
bytes = bytes
complex = complex
dict = dict
float = float
frozenset = frozenset
int = int
list = list
memoryview = memoryview
object = object
range = range
set = set
slice = slice
str = str
tuple = tuple
type = type

BaseException = BaseException
Exception = Exception

none = None
ellipsis = ...


class collections:
    ChainMap = _collections.ChainMap
    Counter = _collections.Counter
    OrderedDict = _collections.OrderedDict
    defaultdict = _collections.defaultdict
    deque = _collections.deque

    class abc:
        AsyncGenerator = _abc.AsyncGenerator
        AsyncIterable = _abc.AsyncIterable
        AsyncIterator = _abc.AsyncIterator
        Awaitable = _abc.Awaitable
        Callable = _abc.Callable
        Collection = _abc.Collection
        Container = _abc.Container
        Coroutine = _abc.Coroutine
        Generator = _abc.Generator
        Hashable = _abc.Hashable
        ItemsView = _abc.ItemsView
        Iterable = _abc.Iterable
        Iterator = _abc.Iterator
        KeysView = _abc.KeysView
        Mapping = _abc.Mapping
        MappingView = _abc.MappingView
        MutableMapping = _abc.MutableMapping
        MutableSequence = _abc.MutableSequence
        MutableSet = _abc.MutableSet
        Reversible = _abc.Reversible
        Sequence = _abc.Sequence
        Set = _abc.Set
        Sized = _abc.Sized
        ValuesView = _abc.ValuesView


class types:
    EllipsisType = _types.EllipsisType
    FunctionType = _types.FunctionType
    GenericAlias = _types.GenericAlias
    MethodType = _types.MethodType
    ModuleType = _types.ModuleType
    NoneType = _types.NoneType
    TracebackType = _types.TracebackType
    UnionType = _types.UnionType


class contextlib:
    AbstractAsyncContextManager = _contextlib.AbstractAsyncContextManager
    AbstractContextManager = _contextlib.AbstractContextManager


class datetime:
    date = _datetime.date
    datetime = _datetime.datetime
    time = _datetime.time
    timedelta = _datetime.timedelta
    timezone = _datetime.timezone


class decimal:
    Decimal = _decimal.Decimal


class enum:
    Enum = _enum.Enum
    Flag = _enum.Flag
    IntEnum = _enum.IntEnum
    IntFlag = _enum.IntFlag


class fractions:
    Fraction = _fractions.Fraction


class io:
    BufferedIOBase = _io.BufferedIOBase
    BytesIO = _io.BytesIO
    IOBase = _io.IOBase
    RawIOBase = _io.RawIOBase
    StringIO = _io.StringIO
    TextIOBase = _io.TextIOBase


class ipaddress:
    IPv4Address = _ipaddress.IPv4Address
    IPv4Interface = _ipaddress.IPv4Interface
    IPv4Network = _ipaddress.IPv4Network
    IPv6Address = _ipaddress.IPv6Address
    IPv6Interface = _ipaddress.IPv6Interface
    IPv6Network = _ipaddress.IPv6Network


class numbers:
    Complex = _numbers.Complex
    Integral = _numbers.Integral
    Number = _numbers.Number
    Rational = _numbers.Rational
    Real = _numbers.Real


class os:
    PathLike = _os.PathLike


class pathlib:
    Path = _pathlib.Path
    PurePath = _pathlib.PurePath


class re:
    Match = _re.Match
    Pattern = _re.Pattern


class uuid:
    UUID = _uuid.UUID


class zoneinfo:
    ZoneInfo = _zoneinfo.ZoneInfo
