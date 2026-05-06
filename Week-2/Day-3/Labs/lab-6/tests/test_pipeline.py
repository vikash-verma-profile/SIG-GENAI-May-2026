import importlib.util
from pathlib import Path


LAB_ROOT = Path(__file__).resolve().parent.parent


def _load_lab_pipeline():
    path = LAB_ROOT / "pipeline.py"
    spec = importlib.util.spec_from_file_location("lab6_products_pipeline", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_day_snapshots_exist():
    assert (LAB_ROOT / "data" / "products_day1.csv").is_file()
    assert (LAB_ROOT / "data" / "products_day2.csv").is_file()
    assert (LAB_ROOT / "data" / "products_day3.csv").is_file()


def test_merge_schema_unions_columns():
    lab = _load_lab_pipeline()
    df1 = lab.load(LAB_ROOT / "data" / "products_day1.csv")
    df2 = lab.load(LAB_ROOT / "data" / "products_day2.csv")
    df3 = lab.load(LAB_ROOT / "data" / "products_day3.csv")

    merged = lab.merge_schema([df1, df2, df3])
    cleaned = lab.clean(merged)

    assert set(cleaned.columns) == {"product_id", "name", "category", "price", "brand", "discount"}
    assert cleaned["brand"].isna().sum() == 0
    assert cleaned["discount"].isna().sum() == 0


def test_pipeline_writes_final_products_csv(tmp_path, monkeypatch):
    lab = _load_lab_pipeline()
    monkeypatch.setattr(lab, "OUTPUT_DIR", tmp_path)

    lab.run_pipeline()

    out = tmp_path / "final_products.csv"
    assert out.is_file()
