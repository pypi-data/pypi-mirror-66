from distutils.version import StrictVersion
from cachetools import TTLCache, cached
from getversion import get_module_version

import requests

import hackgame


@cached(cache=TTLCache(maxsize=1024, ttl=3600))
def versions(package_name):
    url = "https://pypi.python.org/pypi/%s/json" % (package_name,)
    response = requests.get(url)
    data = response.json()
    versions = list(data["releases"].keys())
    versions.sort(key=StrictVersion)
    return versions


def hackgame_update_notice():
    hackgame_versions = versions("hackgame")
    current_version = get_module_version(hackgame)[0]
    latest_version = hackgame_versions[-1]
    if current_version != latest_version:
        return f"this version of hackgame client is out-of-date" \
               f" ({current_version} -> {latest_version})"
