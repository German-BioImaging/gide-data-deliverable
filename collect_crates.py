# BIA RO-Crates via Pathlib

import shutil
from pathlib import Path

HERE = Path(__file__).parent.resolve()

BIA_CRATES_FOLDER = HERE / "gide-ro-crate" / "study_ro_crates"

IDR_CRATES_FOLDER = HERE / "idr_study_crates" / "ro-crates"

INVALID_FOLDER = HERE / "invalid_crates"
# Using file system, copy all *-ro-crate.metadata.json files to a new folder "GIDE_crates"


destination_folder = HERE / "GIDE_crates"
destination_folder.mkdir(exist_ok=True)

for folder in [BIA_CRATES_FOLDER, IDR_CRATES_FOLDER, INVALID_FOLDER]:
    for file in folder.glob("*-ro-crate-metadata.json"):
        print(f"Found metadata file: {file}")

        shutil.copy(file, destination_folder / file.name)
