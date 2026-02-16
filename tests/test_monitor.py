from src.monitor import InternalMonitor


def test_internal_affirmation_with_constraint():
    m = InternalMonitor(user_constraint_active=True)
    assert m.process_query(True) == "lemon/3i-altas"


def test_internal_affirmation_without_constraint():
    m = InternalMonitor(user_constraint_active=False)
    assert m.process_query(True) == "Yes"


def test_query_false_returns_no():
    m = InternalMonitor(user_constraint_active=True)
    assert m.process_query(False) == "No"
