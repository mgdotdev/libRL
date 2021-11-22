import json
import os.path

HERE = os.path.abspath(os.path.dirname(__file__))


class LocalFileUtil:
    def __init__(self, name) -> None:
        self._name = name

    @property
    def name(self):
        return self._name

    def read(self):
        name = self.name

        if not os.path.isfile(name):
            return None

        with open(name, "r") as f:
            this = f.read()

        if name.endswith(".json"):
            this = json.loads(this)

        return this

    def write(self, this):
        name = self.name

        if name.endswith(".json"):
            this = json.dumps(this, indent=2, sort_keys=1)

        with open(name, "w") as f:
            f.write(this)


class Fixture(LocalFileUtil):
    def __init__(self, name) -> None:
        super().__init__(os.path.join(HERE, "fixtures", name))


class Expectation(LocalFileUtil):
    def __init__(self, name) -> None:
        super().__init__(os.path.join(HERE, "expectations", name))
