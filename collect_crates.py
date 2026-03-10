# BIA RO-Crates via Pathlib

import logging
import shutil
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

HERE = Path(__file__).parent.resolve()

BIA_CRATES_FOLDER = HERE / "gide-ro-crate" / "study_ro_crates"

IDR_CRATES_FOLDER = HERE / "idr_study_crates" / "ro-crates"

SSBD_DB_FOLDER = HERE / "gide-ro-crate-openssbd" / "project-ro-crate" / "database"

SSBD_REPO_FOLDER = HERE / "gide-ro-crate-openssbd" / "project-ro-crate" / "repository"

INVALID_FOLDER = HERE / "invalid_crates"

destination_folder = HERE / "GIDE_crates"
destination_folder.mkdir(exist_ok=True)
logger.info(f"Destination folder: {destination_folder}")

folders = {
    "BIA_CRATES_FOLDER": BIA_CRATES_FOLDER,
    "IDR_CRATES_FOLDER": IDR_CRATES_FOLDER,
    "SSBD_DB_FOLDER": SSBD_DB_FOLDER,
    "SSBD_REPO_FOLDER": SSBD_REPO_FOLDER,
    "INVALID_FOLDER": INVALID_FOLDER,
}

for folder_name, folder in folders.items():
    files = list(folder.glob("*-ro-crate-metadata.json"))

    if files:
        logger.info(f"Found {len(files)} RO-Crate metadata file(s) in: {folder_name}")
        for file in files:
            try:
                shutil.copy(file, destination_folder / file.name)
                logger.debug(f"Copied: {file.name}")
            except Exception as e:
                logger.error(f"Failed to copy {file.name}: {e}")
    else:
        logger.debug(f"No RO-Crate metadata files found in: {folder_name}")
