from tap import Tap

from ..lib.manuals import MANUALS

from . import generate_world


class ArgumentParser(Tap):
    manual: str

    def configure(self) -> None:
        self.add_argument("manual", choices=MANUALS.keys())

parser = ArgumentParser(prog="mkworld", description="Generates a manual .apworld file")
args = parser.parse_args()
generate_world(MANUALS[args.manual])
