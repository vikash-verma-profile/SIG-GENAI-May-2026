"""
Lab 3 helper — AI-assisted dbt scaffolding.

Given a short natural-language mart description, print starter model YAML
you can paste under models/. Requires Ollama like other labs.
"""

from llm import ask_llm


def exposure_yaml_stub(exposure_name: str, owner_email: str, depends_on: str) -> str:
    prompt = f"""Generate a minimal dbt exposures YAML snippet for:
name: {exposure_name}
owner email: {owner_email}
depends_on model: {depends_on}

Output YAML only, valid for dbt exposures block."""
    return ask_llm(prompt).strip()


if __name__ == "__main__":
    name = input("Exposure name (e.g. exec_region_kpis): ").strip() or "exec_region_kpis"
    owner = input("Owner email: ").strip() or "analytics@example.com"
    model = input("Upstream model ref (e.g. fct_order_lines): ").strip() or "fct_order_lines"
    print("\n--- suggested exposures.yml fragment ---\n")
    print(exposure_yaml_stub(name, owner, model))
