from sys import argv
from time import sleep
from typing import Type, List, Dict, Tuple, Optional

from sources.source_http_client import HttpClientSource
from sources.source_http_server import HttpServerSource
from sources.source_image import ImageFileSource
from sources.factory import FactoryMixin

from controller.connector import Connector

source_types: Dict[str, Type[FactoryMixin]] = {
    "client": HttpClientSource,
    "server": HttpServerSource,
    "image": ImageFileSource,
}


def print_help():
    print("Usage: [source type] [...param=value]")
    print("Source types:")
    for key in source_types.keys():
        print(f"\t\t{key}")


def print_params(source_type: Type[FactoryMixin]):
    params = source_type.parameters()
    for key in params.keys():
        print(f"\t{key} ({params[key].type}): ")
        print(f"\t\t{params[key].description}")
        if params[key].required:
            print("\t\tRequired")
        else:
            print("\t\tOptional")


def correct_type(source: Type[FactoryMixin], key, value):
    info = source.parameters().get(key, None)
    if not info:
        return value

    return info.type(value)


def parse_args(argv: List[str]) -> Optional[Tuple[Dict, Type[FactoryMixin]]]:
    # Basic argument validation
    if len(argv) < 2 or argv[1] not in source_types:
        print_help()
        return

    source_type = source_types[argv[1]]
    params = argv[2:]
    param_dict = {}
    for param in params:
        if "=" not in param:
            print_params(source_type)
            return

        sep = param.index("=")
        key = param[:sep]
        param_dict[key] = correct_type(source_type, key, param[sep + 1 :])
    return (param_dict, source_type)

# TODO provide seprate mechanism for quiting the program
def running_interface(connector: Connector):
    try:
        while True:
            print("Running...")
            sleep(3)
    except KeyboardInterrupt as e:
        connector.stop()
        raise

# TODO write simple command line UI for testing code
if __name__ == "__main__":
    parsed = parse_args(argv.copy())
    if parsed:
        params, source_factory = parsed
        try:
            source = source_factory.create(**params)
            connector = Connector.factory(source, 24)
            connector.start()
            running_interface(connector)
        except TypeError as e:
            print_params(source_factory)
            raise e
