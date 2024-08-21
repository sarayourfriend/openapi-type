from enum import Enum

from typing import Literal, NewType
from typing import Any, NamedTuple, Union
from collections.abc import Sequence, Mapping

from pyrsistent import pmap, pvector
from pyrsistent.typing import PVector, PMap

from .custom_types import *


__all__ = ('parse_spec', 'serialize_spec', 'OpenAPI')


class IntegerValue(NamedTuple):
    type: Literal['integer']
    format: str = ''
    example: None | int = None
    default: None | int = None
    minimum: None | int = None
    maximum: None | int = None
    nullable: None | bool = None


class FloatValue(NamedTuple):
    type: Literal['number']
    format: str = ''
    example: None | float = None
    default: None | float = None
    nullable: None | bool = None


class StringValue(NamedTuple):
    type: Literal['string']
    format: str = ''
    description: str = ''
    enum: PVector[str] = pvector()
    default: None | str = None
    pattern: None | str = None
    example: str = ''
    nullable: None | bool = None


class BooleanValue(NamedTuple):
    type: Literal['boolean']
    default: None | bool = None
    nullable: None | bool = None


class Reference(NamedTuple):
    ref: Ref


RecursiveAttrs = Mapping[str, 'SchemaType']  # type: ignore


class ObjectWithAdditionalProperties(NamedTuple):
    """ Represents a free-form object
    https://swagger.io/docs/specification/data-models/dictionaries/#free-form
    """
    type: Literal['object']
    additional_properties: Union[None, bool, 'SchemaType'] = None  # type: ignore
    nullable: None | bool = None


class ArrayValue(NamedTuple):
    type: Literal['array']
    items: 'SchemaType'  # type: ignore
    description: str = ''
    nullable: None | bool = None


class ObjectValue(NamedTuple):
    type: Literal['object']
    properties: RecursiveAttrs
    required: frozenset[str] = frozenset()
    description: str = ''
    xml: Mapping[str, Any] = pmap()
    nullable: None | bool = None


class InlinedObjectValue(NamedTuple):
    properties: RecursiveAttrs
    required: frozenset[str]
    description: str = ''
    nullable: None | bool = None


class ResponseRef(NamedTuple):
    """ Values that are referenced as $response.body#/some/path
    """
    operation_id: str
    parameters: Mapping[str, str]
    nullable: None | bool = None


class ObjectRef(NamedTuple):
    """ Values that are referenced as #/components/schemas/<SomeType>
    """
    ref: str


class ProductSchemaType(NamedTuple):
    all_of: Sequence['SchemaType']  # type: ignore
    nullable: None | bool = None


class UnionSchemaTypeAny(NamedTuple):
    any_of: Sequence['SchemaType']  # type: ignore
    nullable: None | bool = None


class UnionSchemaTypeOne(NamedTuple):
    one_of: Sequence['SchemaType']  # type: ignore
    nullable: None | bool = None


SchemaType = (
    StringValue # type: ignore
    | IntegerValue
    | FloatValue
    | BooleanValue
    | ObjectValue
    | ArrayValue
    | ResponseRef
    | Reference
    | ProductSchemaType
    | UnionSchemaTypeAny
    | UnionSchemaTypeOne
    | ObjectWithAdditionalProperties
    | InlinedObjectValue
    | EmptyValue
)

class ParamLocation(Enum):
    QUERY = 'query'
    HEADER = 'header'
    PATH = 'path'
    COOKIE = 'cookie'


class ParamStyle(Enum):
    """
    * https://swagger.io/specification/#style-values
    * https://swagger.io/specification/#style-examples
    """
    FORM = 'form'
    SIMPLE = 'simple'
    MATRIX = 'matrix'
    LABEL = 'label'
    SPACE_DELIMITED = 'spaceDelimited'
    PIPE_DELIMITED = 'pipeDelimited'
    DEEP_OBJECT = 'deepObject'


class OperationParameter(NamedTuple):
    name: str
    in_: ParamLocation
    schema: SchemaType
    required: bool = False
    description: str = ''
    style: None | ParamStyle = None
    explode: None | bool = None


class Header(NamedTuple):
    """ response header
    """
    schema: SchemaType
    description: str = ''


HTTPCode = NewType('HTTPCode', str)
HeaderName = NewType('HeaderName', str)


class MediaType(NamedTuple):
    """ https://swagger.io/specification/#media-type-object
    """
    schema: None | SchemaType = None
    example: None | str | PMap[str, Any] = None
    examples: Mapping[str, Any] = pmap()
    encoding: Mapping[str, Any] = pmap()


class Response(NamedTuple):
    """ Response of an endpoint
    """
    content: PMap[ContentTypeTag, MediaType] = pmap()
    headers: PMap[HeaderName, Header | Reference] = pmap()
    description: str = ''


HeaderTypeName   = NewType('HeaderTypeName', str)
ParamTypeName    = NewType('ParamTypeName', str)
ResponseTypeName = NewType('ResponseTypeName', str)


class Components(NamedTuple):
    schemas: Mapping[str, SchemaType]
    links: Mapping[str, SchemaType] = pmap()
    parameters: Mapping[ParamTypeName, OperationParameter] = pmap()
    responses: Mapping[ResponseTypeName, Response] = pmap()
    headers: Mapping[HeaderTypeName, Header] = pmap()
    request_bodies: Mapping[str, Any] = pmap()
    security_schemes: Mapping[str, Any] = pmap()


class ServerVar(NamedTuple):
    default: str
    enum: Sequence[str]
    description: str = ''


class Server(NamedTuple):
    url: str
    description: str = ''
    variables: Mapping[str, ServerVar] = pmap()


class InfoLicense(NamedTuple):
    name: str
    url: str = ''


class InfoContact(NamedTuple):
    name: None | str
    email: None | str
    url: None | str


class Info(NamedTuple):
    version: str
    """ API version
    """
    title: str
    license: None | InfoLicense
    contact: None | InfoContact
    terms_of_service: str = ''
    description: str = ''


class SpecFormat(Enum):
    V3_0_0 = '3.0.0'
    V3_0_1 = '3.0.1'
    V3_0_2 = '3.0.2'
    V3_0_3 = '3.0.3'


class ExternalDoc(NamedTuple):
    url: str
    description: str = ''


class RequestBodySchema(NamedTuple):
    schema: SchemaType


class RequestBody(NamedTuple):
    """ https://swagger.io/specification/#request-body-object
    """
    content: Mapping[ContentTypeTag, RequestBodySchema]
    description: str = ''
    required: bool = False


class Operation(NamedTuple):
    """ https://swagger.io/specification/#operation-object
    """
    responses: Mapping[HTTPCode, Reference | Response]  # union order matters
    external_docs: None | ExternalDoc
    summary: str = ''
    operation_id: str = ''
    parameters: frozenset[OperationParameter | Reference] = frozenset()
    request_body: None | RequestBody | Reference = None
    description: str = ''
    tags: frozenset[str] = frozenset()
    callbacks: Mapping[str, Mapping[str, Any]] = pmap()
    security: None | Any = None


class PathItem(NamedTuple):
    """ Describes endpoint methods
    """
    head: None | Operation
    get: None | Operation
    post: None | Operation
    put: None | Operation
    patch: None | Operation
    delete: None | Operation
    trace: None | Operation
    servers: Sequence[Server] = pvector()
    ref: None | Ref = None
    summary: str = ''
    description: str = ''


SecurityName = NewType('SecurityName', str)


class SpecTag(NamedTuple):
    name: str
    external_docs: None | ExternalDoc
    description: str = ''


class OpenAPI(NamedTuple):
    openapi: SpecFormat
    """ Spec format version
    """
    info: Info
    """ Various metadata
    """
    paths: Mapping[str, PathItem]
    components: Components = Components(schemas=pmap(), links=pmap())
    servers: Sequence[Server] = pvector()
    security: Sequence[Mapping[SecurityName, Sequence[str]]] = pvector()
    tags: Sequence[SpecTag] = pvector()
    external_docs: None | ExternalDoc = None


overrides = {
    OperationParameter.in_: 'in',
    Reference.ref: '$ref',
    PathItem.ref: '$ref',
}


parse_spec, serialize_spec = TypeGenerator & overrides ^ OpenAPI
