from typing import List

from .base_serializer import BaseSerializer
from .generic_serializer import GenericSerializer
from .serializer import Serializer
from .uuid_serializer import UUIDSerializer


SERIALIZERS: List[Serializer] = [GenericSerializer(), UUIDSerializer()]

__all__ = ["BaseSerializer", "SERIALIZERS"]
