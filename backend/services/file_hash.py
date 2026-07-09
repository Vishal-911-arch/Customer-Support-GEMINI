import hashlib


class FileHasher:

    @staticmethod
    def sha256(file_path):

        sha = hashlib.sha256()

        with open(file_path, "rb") as f:

            while True:

                chunk = f.read(8192)

                if not chunk:
                    break

                sha.update(chunk)

        return sha.hexdigest()