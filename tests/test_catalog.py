from agentix_framework_demos import DEFAULT_SCENARIO, list_frameworks


def test_catalog_has_eight_frameworks() -> None:
    frameworks = list_frameworks()
    assert len(frameworks) == 8


def test_default_scenario_is_sql_governance() -> None:
    assert DEFAULT_SCENARIO.id == "sql-lineage-triage"
    assert DEFAULT_SCENARIO.domain == "Data/SQL governance"
