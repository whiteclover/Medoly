import importlib
import pkgutil

import logging

LOGGER = logging.getLogger("kanon.composer")


def scan_submodules(package, recursive=True):
    """ Import and scan all submodules of a module, recursively, including sub packages, 

    :param package: package (name or actual module)
    :type package: str | module
    :rtype: dict[str, types.ModuleType]
    """
    if isinstance(package, str):
        package = importlib.import_module(package)
    results = {}
    is_path = False
    if hasattr(package, "__path__"):
        is_path = True
        for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
            full_name = package.__name__ + '.' + name
            results[full_name] = importlib.import_module(full_name)
            if recursive and is_pkg:
                LOGGER.debug("Scaning package: %s", full_name)
                results.update(scan_submodules(full_name)[0])
    return results, is_path, package
