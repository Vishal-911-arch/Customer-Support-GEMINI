import json
from pathlib import Path

REGISTRY = Path("indexed_files.json")


class FileRegistry:

    @staticmethod
    def load():

        if not REGISTRY.exists():
            return []

        with open(REGISTRY, "r") as f:
            return json.load(f)

    @staticmethod
    def save(data):

        with open(REGISTRY, "w") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def contains(file_hash):

        return file_hash in FileRegistry.load()

    @staticmethod
    def add(file_hash):

        data = FileRegistry.load()

        if file_hash not in data:
            data.append(file_hash)
            FileRegistry.save(data)