from dataclasses import dataclass, replace
from itertools import chain
from typing import Type, Any, Tuple, NamedTuple, Callable, Union, get_type_hints

from infix import rbind
from pyrsistent import pvector, pmap
from pyrsistent.typing import PVector, PMap

URLTextFragment = str
Docstring = str


@dataclass(frozen=True)
class DataType:
    typ: Type[Any] = Type[Any]

    def __getitem__(self, item: Type[Any]) -> 'DataType':
        return replace(self, typ=item)


JSON = DataType()


def empty_handler() -> Tuple[()]:
    """ A stub function that represents a handler that does nothing
    """
    return ()


class HTTP(NamedTuple):
    method: str = 'GET'
    segments: PVector[URLTextFragment] = pvector(['/'])
    headers_type: Type[Any] = Type[Any]
    return_type: Tuple[int, DataType] = (200, JSON[Type[Any]])
    handler: Callable = empty_handler
    request_types: PMap[Type[Any], Type[Any]] = pmap()
    """ Set of types used in this HTTP segment
    """
    docs: Docstring = ""

    def __truediv__(self, other: Union[URLTextFragment, Union[Tuple[str, Type], Tuple[str, Type, Docstring]]]) -> 'HTTP':
        if isinstance(other, URLTextFragment):
            return self._replace(segments=pvector(chain(self.segments, [other])))

        elif isinstance(other, tuple):
            placeholder_name, typ, *docs = other
            if hasattr(typ, placeholder_name):
                typ_actual = get_type_hints(typ)[placeholder_name]
            else:
                typ_actual = typ

            return self._replace(
                segments=pvector(chain(self.segments, [f'{{{placeholder_name}}}'])),
                request_types=self.request_types.set(typ, typ).set(typ_actual, typ_actual)
            )
        elif isinstance(other, rbind):
            return self | other

        raise NotImplementedError(f'Unknown type of URL segment: {type(other)}')

    @property
    def segments_url(self) -> str:
        url = '/'.join(x.strip('/ ') for x in self.segments if x.strip('/ '))
        return f'/{url}'

    def __repr__(self) -> str:
        return f'HTTP ( {self.method} {self.segments_url} )'
