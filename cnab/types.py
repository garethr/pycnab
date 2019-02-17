import canonicaljson  # type: ignore

from dataclasses import dataclass, field
from typing import Optional, Any, List, Union, Dict, TypeVar, Callable, Type, cast


T = TypeVar("T")


def from_bool(x: Any) -> bool:
    if not isinstance(x, bool):
        raise Exception(f"{x} not a boolean")
    return x


def from_none(x: Any) -> Any:
    if not x is None:
        raise Exception(f"{x} not None")
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_str(x: Any) -> str:
    if not isinstance(x, str):
        raise Exception(f"{x} not a string")
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    if not isinstance(x, list):
        raise Exception(f"{x} not a list")
    return [f(y) for y in x]


def from_int(x: Any) -> int:
    if not (isinstance(x, int) and not isinstance(x, bool)):
        raise Exception(f"{x} not an integer")
    return x


def to_class(c: Type[T], x: Any) -> dict:
    if not isinstance(x, c):
        raise Exception(f"{x} not a {c}")
    return cast(Any, x).to_dict()


def from_dict(f: Callable[[Any], T], x: Any) -> Dict[str, T]:
    if not isinstance(x, dict):
        raise Exception(f"{x} not a dictionary")
    return {k: f(v) for (k, v) in x.items()}


def clean(result: Dict) -> dict:
    return {k: v for k, v in result.items() if v}


@dataclass
class Action:
    modifies: Optional[bool] = None
    stateless: Optional[bool] = None
    description: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> "Action":
        assert isinstance(obj, dict)
        modifies = from_union([from_bool, from_none], obj.get("modifies"))
        stateless = from_union([from_bool, from_none], obj.get("stateless"))
        description = from_union([from_str, from_none], obj.get("description"))
        return Action(modifies, stateless, description)

    def to_dict(self) -> dict:
        result: dict = {}
        result["modifies"] = from_union([from_bool, from_none], self.modifies)
        result["stateless"] = from_union([from_bool, from_none], self.stateless)
        result["description"] = from_union([from_str, from_none], self.description)
        return clean(result)


@dataclass
class Credential:
    description: Optional[str] = None
    env: Optional[str] = None
    path: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> "Credential":
        assert isinstance(obj, dict)
        description = from_union([from_str, from_none], obj.get("description"))
        env = from_union([from_str, from_none], obj.get("env"))
        path = from_union([from_str, from_none], obj.get("path"))
        return Credential(description, env, path)

    def to_dict(self) -> dict:
        result: dict = {}
        result["description"] = from_union([from_str, from_none], self.description)
        result["env"] = from_union([from_str, from_none], self.env)
        result["path"] = from_union([from_str, from_none], self.path)
        return clean(result)


@dataclass
class ImagePlatform:
    architecture: Optional[str] = None
    os: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> "ImagePlatform":
        assert isinstance(obj, dict)
        architecture = from_union([from_str, from_none], obj.get("architecture"))
        os = from_union([from_str, from_none], obj.get("os"))
        return ImagePlatform(architecture, os)

    def to_dict(self) -> dict:
        result: dict = {}
        result["architecture"] = from_union([from_str, from_none], self.architecture)
        result["os"] = from_union([from_str, from_none], self.os)
        return clean(result)


@dataclass
class Ref:
    field: Optional[str] = None
    media_type: Optional[str] = None
    path: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> "Ref":
        assert isinstance(obj, dict)
        field = from_union([from_str, from_none], obj.get("field"))
        media_type = from_union([from_str, from_none], obj.get("mediaType"))
        path = from_union([from_str, from_none], obj.get("path"))
        return Ref(field, media_type, path)

    def to_dict(self) -> dict:
        result: dict = {}
        result["field"] = from_union([from_str, from_none], self.field)
        result["mediaType"] = from_union([from_str, from_none], self.media_type)
        result["path"] = from_union([from_str, from_none], self.path)
        return clean(result)


@dataclass
class Image:
    image: str
    description: Optional[str] = None
    digest: Optional[str] = None
    image_type: Optional[str] = None
    media_type: Optional[str] = None
    platform: Optional[ImagePlatform] = None
    refs: List[Ref] = field(default_factory=list)
    size: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> "Image":
        assert isinstance(obj, dict)
        description = from_union([from_str, from_none], obj.get("description"))
        digest = from_union([from_str, from_none], obj.get("digest"))
        image = from_str(obj.get("image"))
        image_type = from_union([from_str, from_none], obj.get("imageType"))
        media_type = from_union([from_str, from_none], obj.get("mediaType"))
        platform = from_union([ImagePlatform.from_dict, from_none], obj.get("platform"))
        refs = from_union(
            [lambda x: from_list(Ref.from_dict, x), from_none], obj.get("refs")
        )
        size = from_union([from_int, from_none], obj.get("size"))
        return Image(
            description, digest, image, image_type, media_type, platform, refs, size
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["description"] = from_union([from_str, from_none], self.description)
        result["digest"] = from_union([from_str, from_none], self.digest)
        result["image"] = from_str(self.image)
        result["imageType"] = from_union([from_str, from_none], self.image_type)
        result["mediaType"] = from_union([from_str, from_none], self.media_type)
        result["platform"] = from_union(
            [lambda x: to_class(ImagePlatform, x), from_none], self.platform
        )
        result["refs"] = from_list(lambda x: to_class(Ref, x), self.refs)
        result["size"] = from_union([from_int, from_none], self.size)
        return clean(result)


@dataclass
class InvocationImage:
    image: str
    digest: Optional[str] = None
    image_type: Optional[str] = "oci"
    media_type: Optional[str] = None
    platform: Optional[ImagePlatform] = None
    size: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> "InvocationImage":
        assert isinstance(obj, dict)
        digest = from_union([from_str, from_none], obj.get("digest"))
        image = from_str(obj.get("image"))
        image_type = from_union([from_str, from_none], obj.get("imageType"))
        media_type = from_union([from_str, from_none], obj.get("mediaType"))
        platform = from_union([ImagePlatform.from_dict, from_none], obj.get("platform"))
        size = from_union([from_str, from_none], obj.get("size"))
        return InvocationImage(image, digest, image_type, media_type, platform, size)

    def to_dict(self) -> dict:
        result: dict = {}
        result["digest"] = from_union([from_str, from_none], self.digest)
        result["image"] = from_str(self.image)
        result["imageType"] = from_union([from_str, from_none], self.image_type)
        result["mediaType"] = from_union([from_str, from_none], self.media_type)
        result["platform"] = from_union(
            [lambda x: to_class(ImagePlatform, x), from_none], self.platform
        )
        result["size"] = from_union([from_str, from_none], self.size)
        return clean(result)


@dataclass
class Maintainer:
    name: str
    email: Optional[str] = None
    url: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> "Maintainer":
        assert isinstance(obj, dict)
        name = from_union([from_str, from_none], obj.get("name"))
        email = from_union([from_str, from_none], obj.get("email"))
        url = from_union([from_str, from_none], obj.get("url"))
        return Maintainer(name, email, url)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_union([from_str, from_none], self.name)
        result["email"] = from_union([from_str, from_none], self.email)
        result["url"] = from_union([from_str, from_none], self.url)
        return clean(result)


@dataclass
class Destination:
    description: Optional[str] = None
    env: Optional[str] = None
    path: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> "Destination":
        assert isinstance(obj, dict)
        description = from_union([from_str, from_none], obj.get("description"))
        env = from_union([from_str, from_none], obj.get("env"))
        path = from_union([from_str, from_none], obj.get("path"))
        return Destination(description, env, path)

    def to_dict(self) -> dict:
        result: dict = {}
        result["description"] = from_union([from_str, from_none], self.description)
        result["env"] = from_union([from_str, from_none], self.env)
        result["path"] = from_union([from_str, from_none], self.path)
        return clean(result)


@dataclass
class Metadata:
    description: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> "Metadata":
        assert isinstance(obj, dict)
        description = from_union([from_str, from_none], obj.get("description"))
        return Metadata(description)

    def to_dict(self) -> dict:
        result: dict = {}
        result["description"] = from_union([from_str, from_none], self.description)
        return clean(result)


@dataclass
class Parameter:
    type: str
    destination: Destination
    default_value: Union[bool, int, None, str] = None
    allowed_values: Optional[List[Any]] = field(default_factory=list)
    max_length: Optional[int] = None
    max_value: Optional[int] = None
    metadata: Optional[Metadata] = None
    min_length: Optional[int] = None
    min_value: Optional[int] = None
    required: Optional[bool] = None

    @staticmethod
    def from_dict(obj: Any) -> "Parameter":
        assert isinstance(obj, dict)
        allowed_values = from_union(
            [lambda x: from_list(lambda x: x, x), from_none], obj.get("allowedValues")
        )
        default_value = from_union(
            [from_int, from_bool, from_none, from_str], obj.get("defaultValue")
        )
        destination = from_union([Destination.from_dict], obj.get("destination"))
        max_length = from_union([from_int, from_none], obj.get("maxLength"))
        max_value = from_union([from_int, from_none], obj.get("maxValue"))
        metadata = from_union([Metadata.from_dict, from_none], obj.get("metadata"))
        min_length = from_union([from_int, from_none], obj.get("minLength"))
        min_value = from_union([from_int, from_none], obj.get("minValue"))
        required = from_union([from_bool, from_none], obj.get("required"))
        type = from_str(obj.get("type"))
        return Parameter(
            type,
            destination,
            default_value,
            allowed_values,
            max_length,
            max_value,
            metadata,
            min_length,
            min_value,
            required,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["allowedValues"] = from_list(lambda x: x, self.allowed_values)
        result["destination"] = from_union(
            [lambda x: to_class(Destination, x)], self.destination
        )
        result["maxLength"] = from_union([from_int, from_none], self.max_length)
        result["maxValue"] = from_union([from_int, from_none], self.max_value)
        result["metadata"] = from_union(
            [lambda x: to_class(Metadata, x), from_none], self.metadata
        )
        result["minLength"] = from_union([from_int, from_none], self.min_length)
        result["minValue"] = from_union([from_int, from_none], self.min_value)
        result["required"] = from_union([from_bool, from_none], self.required)
        result["type"] = from_str(self.type)
        return clean(result)


@dataclass
class Bundle:
    name: str
    version: str
    invocation_images: List[InvocationImage]
    schema_version: Optional[str] = "v1"
    actions: Dict[str, Action] = field(default_factory=dict)
    credentials: Dict[str, Credential] = field(default_factory=dict)
    description: Optional[str] = None
    license: Optional[str] = None
    images: Dict[str, Image] = field(default_factory=dict)
    keywords: List[str] = field(default_factory=list)
    maintainers: List[Maintainer] = field(default_factory=list)
    parameters: Dict[str, Parameter] = field(default_factory=dict)

    @staticmethod
    def from_dict(obj: Any) -> "Bundle":
        assert isinstance(obj, dict)
        actions = from_union(
            [lambda x: from_dict(Action.from_dict, x), from_none], obj.get("actions")
        )
        credentials = from_union(
            [lambda x: from_dict(Credential.from_dict, x), from_none],
            obj.get("credentials"),
        )
        description = from_union([from_str, from_none], obj.get("description"))
        license = from_union([from_str, from_none], obj.get("license"))
        images = from_union(
            [lambda x: from_dict(Image.from_dict, x), from_none], obj.get("images")
        )
        invocation_images = from_list(
            InvocationImage.from_dict, obj.get("invocationImages")
        )
        keywords = from_union(
            [lambda x: from_list(from_str, x), from_none], obj.get("keywords")
        )
        maintainers = from_union(
            [lambda x: from_list(Maintainer.from_dict, x), from_none],
            obj.get("maintainers"),
        )
        name = from_str(obj.get("name"))
        parameters = from_union(
            [lambda x: from_dict(Parameter.from_dict, x), from_none],
            obj.get("parameters"),
        )
        schema_version = from_union([from_str, from_none], obj.get("schemaVersion"))
        version = from_str(obj.get("version"))
        return Bundle(
            name,
            version,
            invocation_images,
            schema_version,
            actions,
            credentials,
            description,
            license,
            images,
            keywords,
            maintainers,
            parameters,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["actions"] = from_dict(lambda x: to_class(Action, x), self.actions)
        result["credentials"] = from_dict(
            lambda x: to_class(Credential, x), self.credentials
        )
        result["description"] = from_union([from_str, from_none], self.description)
        result["license"] = from_union([from_str, from_none], self.license)
        result["images"] = from_dict(lambda x: to_class(Image, x), self.images)
        result["invocationImages"] = from_list(
            lambda x: to_class(InvocationImage, x), self.invocation_images
        )
        result["keywords"] = from_list(from_str, self.keywords)
        result["maintainers"] = from_list(
            lambda x: to_class(Maintainer, x), self.maintainers
        )
        result["name"] = from_str(self.name)
        result["parameters"] = from_dict(
            lambda x: to_class(Parameter, x), self.parameters
        )
        result["schemaVersion"] = from_str(self.schema_version)
        result["version"] = from_str(self.version)
        return clean(result)

    def to_json(self, pretty: bool = False) -> str:
        if pretty:
            func = canonicaljson.encode_pretty_printed_json
        else:
            func = canonicaljson.encode_canonical_json
        return func(self.to_dict()).decode()
