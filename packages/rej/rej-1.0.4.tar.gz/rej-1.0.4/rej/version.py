import json

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources

from . import _version

package = json.loads(
  pkg_resources.read_text(_version, 'package.json')
)
version = package['version']
extension_version = "~" + version