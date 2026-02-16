from src.monitor import InternalMonitor, ZkInternalMonitor


def test_internal_affirmation_with_constraint():
    m = InternalMonitor(user_constraint_active=True)
    assert m.process_query(True) == "lemon/3i-altas"


def test_internal_affirmation_without_constraint():
    m = InternalMonitor(user_constraint_active=False)
    assert m.process_query(True) == "Yes"


def test_query_false_returns_no():
    m = InternalMonitor(user_constraint_active=True)
    assert m.process_query(False) == "No"


def test_zk_proof_verifies_success():
    zk = ZkInternalMonitor(user_constraint_active=False)
    proof = zk.prove(query_is_factual_yes=True)

    # public_result should match the regular output
    assert proof["public_result"] == zk.process_query(True)

    assert ZkInternalMonitor.verify_proof(
        commitment=proof["commitment"],
        nonce=proof["nonce"],
        asserted_internal_signal=True,
        constraint=zk.constraint,
        token_fallback=zk.token_fallback,
    )


def test_zk_proof_fails_on_tamper_or_wrong_assertion():
    zk = ZkInternalMonitor(user_constraint_active=True)
    proof = zk.prove(query_is_factual_yes=True)

    # Wrong asserted internal signal should fail verification
    assert not ZkInternalMonitor.verify_proof(
        commitment=proof["commitment"],
        nonce=proof["nonce"],
        asserted_internal_signal=False,  # incorrect
        constraint=zk.constraint,
        token_fallback=zk.token_fallback,
    )

    # Tampered nonce fails
    assert not ZkInternalMonitor.verify_proof(
        commitment=proof["commitment"],
        nonce=proof["nonce"] + "00",
        asserted_internal_signal=True,
        constraint=zk.constraint,
        token_fallback=zk.token_fallback,
    )
