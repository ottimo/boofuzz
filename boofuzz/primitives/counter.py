import struct

from ..constants import LITTLE_ENDIAN
from boofuzz.primitives.base_primitive import BasePrimitive


class Counter(BasePrimitive):
  def __init__(self, value, size=-1):
    super(Counter, self).__init__()
    self._value = self._original_value = value
    self.encoding = 'ascii'
    self.size = size

  @property
  def name(self):
      return None

  def mutate(self):
    self._value += 1
    return False

  def _render(self, value):
      """Render string value, properly encoded.
      """
      try:
          # Note: In the future, we should use unicode strings when we mean to encode them later. As it is, we need
          # decode the value before decoding it! Meaning we'll never be able to use characters outside the ASCII
          # range.
          _rendered = str(value).decode('ascii').encode(self.encoding)
      except UnicodeDecodeError:
          # If we can't decode the string, just treat it like a plain byte string
          _rendered = value
      if self.size < 0:
        return _rendered
      rendered = hex(int(_rendered))[2:]
      return ('{:0>' +str(self.size)+ '}').format(rendered)