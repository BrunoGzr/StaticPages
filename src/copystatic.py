import os
import shutil


def copy_static_to_public(source: str, destination: str) -> None:
    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.mkdir(destination)
    _copy_recursive(source, destination)


def _copy_recursive(source: str, destination: str) -> None:
    for item in os.listdir(source):
        source_path = os.path.join(source, item)
        destination_path = os.path.join(destination, item)
        if os.path.isfile(source_path):
            print(f"Copying {source_path} -> {destination_path}")
            shutil.copy(source_path, destination_path)
        else:
            print(f"Creating directory {destination_path}")
            os.mkdir(destination_path)
            _copy_recursive(source_path, destination_path)
