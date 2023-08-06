from typing import NamedTuple, Any, Tuple, Type, Callable

from pyrsistent import pmap, pvector
from pyrsistent.typing import PVector, PMap
from itertools import chain
from typeit import TypeConstructor

import routes as rts
from typeit.combinator.constructor import _TypeConstructor

from routedsl.bricks import URLTextFragment, DataType, JSON, HTTP, empty_handler
from routedsl.ops import *

Section = Any

Header = DataType()

OK = StatusCode(200)


GET = HTTP('GET')
POST = HTTP('POST')


class User(NamedTuple):
    user_id: int


class Headers(NamedTuple):
    content_type: str = 'application/json'


def get_user_info() -> User:
    return User(user_id=1)

def update_user_info(user: User) -> bool:
    return True


class Routes(NamedTuple):
    endpoints: PVector[HTTP] = pvector()
    current_prefix: HTTP = HTTP()
    constructors: PMap[Type[Any], Tuple[Callable[[Any], Type[Any]], Callable[[Any], Type[Any]]]] = pmap()

    def __truediv__(self, other: URLTextFragment) -> 'Routes':
        return self._replace(current_prefix=self.current_prefix / other)

    def __call__(self, other: HTTP) -> 'Routes':
        endpoint = self.current_prefix._replace(
            method=other.method,
            segments=pvector(chain(self.current_prefix.segments, other.segments)),
            headers_type=other.headers_type,
            return_type=other.return_type,
            handler=other.handler,
            request_types=self.current_prefix.request_types.update(other.request_types),
            docs=other.docs
        )
        return self._replace(endpoints=pvector(chain(self.endpoints, [endpoint])))

    __or__ = __call__

    def __repr__(self) -> str:
        return (
            'Routes:\n'
            '\t' + '\n\t'.join(str(x) for x in self.endpoints)
        )


def generate_router(
    routes: Routes,
    typer: _TypeConstructor = TypeConstructor
) -> Tuple[rts.URLGenerator, PMap[Type[Any], Tuple[Callable, Callable]]]:
    mapper = rts.Mapper()
    constructors_serializers: PMap[Type[Any], Tuple[Callable, Callable]] = pmap()
    for http_endpoint in routes.endpoints:
        conditions = dict(method=[http_endpoint.method.upper()])

        for typ in http_endpoint.request_types.keys():
            if typ not in constructors_serializers:
                constructors_serializers = constructors_serializers.set(typ, typer.apply_on(typ))

        mapper.connect(
            None,
            http_endpoint.segments_url,
            controller=http_endpoint,
            conditions=conditions,
        )

    router = rts.URLGenerator(mapper,
                              pmap({'HTTP_HOST': 'localhost', 'SCRIPT_NAME': ''}))


    return router, constructors_serializers
