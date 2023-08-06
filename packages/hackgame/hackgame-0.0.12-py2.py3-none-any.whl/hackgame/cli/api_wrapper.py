from typing import List, Generic, Type

from click import ClickException
from requests import HTTPError

from hackgame.api import ObjectEndpoint, Resource
from hackgame.cli.identifier_cache import IdentifierCache, CacheItem


class IdentifierCachingObjectEndpoint(ObjectEndpoint, Generic[Resource]):
    """
    Wrapper around ObjectEndpoint that caches incoming Objects that the client sees
    """

    def __init__(
        self,
        endpoint: str,
        object_class: Type[Resource],
        client,
        cache: IdentifierCache,
    ):
        self._cache = cache
        super().__init__(endpoint, object_class, client)

    def get(self, public_uuid) -> Resource:
        resource = super().get(public_uuid)
        if resource is not None:
            self._cache.store(
                CacheItem(
                    public_uuid=resource.public_uuid,
                    handle=resource.handle,
                    object_type=self._class,
                    added_at=0,
                )
            )
        return resource

    def create(self, data) -> Resource:
        resource = super().create(data)
        if resource is not None:
            self._cache.store(
                CacheItem(
                    public_uuid=resource.public_uuid,
                    handle=resource.handle,
                    object_type=self._class,
                    added_at=0,
                )
            )
        return resource

    def list(self) -> List[Resource]:
        resources = super().list()
        for resource in resources:
            self._cache.store(
                CacheItem(
                    public_uuid=resource.public_uuid,
                    handle=resource.handle,
                    object_type=self._class,
                    added_at=0,
                )
            )
        return resources


def pretty_hackgame_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except HTTPError as e:
            status_code = e.response.status_code
            if status_code == 401:
                raise ClickException(
                    "401 unauthorized! have you logged in with `hackgame login`?"
                ) from e
            elif status_code == 403:
                detail = e.response.json().get("detail")
                if detail == "token is required to do this":
                    raise ClickException(
                        "403 forbidden! you need to set a valid token with "
                        "`hackgame use token`"
                    )
                elif detail == "Invalid token.":
                    raise ClickException(
                        "403 forbidden! have you logged in with `hackgame login`?"
                    )
                else:
                    raise
            else:
                raise

    return wrapper


class ClickRaisingObjectEndpoint(ObjectEndpoint, Generic[Resource]):
    """
    Wrapper around ObjectEndpoint that returns a prettier error when we know that
    a HTTP 401, 403, etc., is due to something that the user can fix themselves.
    """

    @pretty_hackgame_error
    def get(self, public_uuid) -> Resource:
        return super().get(public_uuid)

    @pretty_hackgame_error
    def create(self, data) -> Resource:
        return super().create(data)

    @pretty_hackgame_error
    def list(self) -> List[Resource]:
        return super().list()


class CLIObjectEndpoint(
    ClickRaisingObjectEndpoint, IdentifierCachingObjectEndpoint, Generic[Resource]
):
    """Uses the separate CLI Mixins together to create the CLI version of the API"""

    pass
