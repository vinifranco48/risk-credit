from pathlib import Path

import typer
from loguru import logger
from tqdm import tqdm

from src.config import PROCESSED_DATA_DIR
import sys
from pathlib import Path

# Adicione o diretório raiz do projeto ao sys.path
print(sys.path.append(str(Path(__file__).resolve().parents[1])))
app = typer.Typer()

print(sys)
@app.command()
def main(
    # ---- REPLACE DEFAULT PATHS AS APPROPRIATE ----
    input_path: Path = PROCESSED_DATA_DIR / "dataset.csv",
    output_path: Path = PROCESSED_DATA_DIR / "features.csv",
    # -----------------------------------------
):
    # ---- REPLACE THIS WITH YOUR OWN CODE ----
    logger.info("Generating features from dataset...")
    for i in tqdm(range(10), total=10):
        if i == 5:
            logger.info("Something happened for iteration 5.")
    logger.success("Features generation complete.")
    # -----------------------------------------


if __name__ == "__main__":
    app()
