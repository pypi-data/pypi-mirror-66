import inspect
import logging
from typing import Sequence, Callable, Any

from marshmallow import Schema
from marshmallow.exceptions import MarshmallowError
from starlette.responses import Response

from star_resty.exceptions import DumpError

__all__ = ('create_render', 'Render')

logger = logging.getLogger(__name__)


def create_render(method) -> 'Render':
    renders = []
    response_schema = getattr(method, 'response_schema', None)
    if response_schema is None:
        response_schema = getattr(method, 'Response', None)

    if response_schema is not None:
        if inspect.isclass(response_schema):
            response_schema = response_schema()
        renders.append(dump_content(response_schema))

    serializer = getattr(method, 'serializer', None)
    if serializer is not None:
        renders.append(render_bytes(serializer, method.status_code or 200))

    return Render(renders)


class Render:
    __slots__ = ('_renders',)

    def __init__(self, renders: Sequence):
        self._renders = renders

    def __call__(self, content: Any):
        for r in self._renders:
            content = r(content)

        return content


def render_bytes(serializer, status_code):
    def render(content):
        return Response(serializer.render(content),
                        media_type=serializer.media_type,
                        status_code=status_code)

    return render


def dump_content(response_schema: Schema) -> Callable:
    def dump(content):
        try:
            return response_schema.dump(content)
        except MarshmallowError as e:
            logger.error('Dump error: %s', e)
            raise DumpError(e) from e
        except (ValueError, TypeError) as e:
            logger.error('Dump error: %s', e)
            raise DumpError(e) from e

    return dump
