from os import environ
from pathlib import Path
import shutil
from . import create_world_spec


spec = create_world_spec()

if environ.get("RELEASE"):
    spec.create_apworld_file()
else:
    output_dir = Path("dist/distance")
    shutil.rmtree(output_dir)
    spec.create_apworld_file(
        apworld_output_dir=output_dir,
        apworld_contents_temp_dir=output_dir,
        preserve_apworld_contents_temp_dir=True,
    )
