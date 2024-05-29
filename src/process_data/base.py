# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import Any


class BaseProcessDataInterface(ABC):
    """
    Baseclass for data processing interfaces
    """

    @classmethod
    @abstractmethod
    def in_memory(cls, file_name: str) -> Any: ...

    @classmethod
    @abstractmethod
    def streaming(cls, file_name: str) -> Any: ...
