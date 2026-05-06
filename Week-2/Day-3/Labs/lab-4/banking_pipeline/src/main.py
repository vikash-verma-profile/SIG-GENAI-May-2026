"""Banking ETL entrypoint."""
import logging
import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from fraud import detect_fraud  # noqa: E402
from load import load_data  # noqa: E402
from save import save_data  # noqa: E402
from transform import aggregate_by_account, clean_data  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
LOG = logging.getLogger(__name__)

LAB_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_PATH = LAB_ROOT / "data" / "transactions.csv"
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"


def run_pipeline() -> None:
    LOG.info("Pipeline started")
    df = load_data(DATA_PATH)
    df = clean_data(df)
    df = detect_fraud(df)
    agg = aggregate_by_account(df)
    save_data(df, OUTPUT_DIR / "clean.csv")
    save_data(agg, OUTPUT_DIR / "agg.csv")
    LOG.info("Pipeline finished")


if __name__ == "__main__":
    run_pipeline()
