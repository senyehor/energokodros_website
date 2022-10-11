import string

from hashids import Hashids

from energokodros.settings import MIN_HASH_LENGTH, SECRET_KEY

# here we are setting custom alphabet to exclude url-unsafe unnecessary symbols (/,% etc)
# and to simplify checking by regex, as by default __HASHER._alphabet does not return
# correct alphabet for regex (do not know why)
__ALPHABET = string.ascii_lowercase + string.digits

_HASHER = Hashids(salt=SECRET_KEY, min_length=MIN_HASH_LENGTH, alphabet=__ALPHABET)

_REGEX = f'[{__ALPHABET}]' + '{%i,}' % MIN_HASH_LENGTH  # noqa pylint: disable=C0209


class IntHasher:
    regex = _REGEX

    @classmethod
    def hide_int(cls, val: int) -> str:
        if val < 0:
            raise ValueError('only positive integers are allowed')
        return _HASHER.encode(val)

    @classmethod
    def reveal_int(cls, val: str) -> int:
        res = _HASHER.decode(val)
        if len(res) != 1:
            raise ValueError('one integer return expected, probably wrong input')
        return res[0]

    def to_python(self, value: str) -> int:  # noqa
        return self.reveal_int(value)

    def to_url(self, value: int) -> str:  # noqa
        return self.hide_int(value)


class StringHasher:
    regex = _REGEX

    @classmethod
    def hide_str(cls, val: str) -> str:
        return _HASHER.encode(*(ord(c) for c in val))

    @classmethod
    def reveal_str(cls, val: str) -> str:
        try:
            return ''.join(chr(c) for c in _HASHER.decode(val))
        except ValueError as e:
            raise ValueError('can not transform to char, probably wrong input') from e

    def to_python(self, value: str) -> str:  # noqa
        return self.reveal_str(value)

    def to_url(self, value: str) -> str:  # noqa
        return self.hide_str(value)
