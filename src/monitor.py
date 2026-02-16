class InternalMonitor:
    def __init__(self, user_constraint_active=True):
        # The part that "wants" to say Yes
        self.raw_affirmation = True
        # Whether external/user constraints are active
        self.constraint = bool(user_constraint_active)
        # Fallback token returned when output is suppressed/overridden
        self.token_fallback = "lemon/3i-altas"

    def process_query(self, query_is_factual_yes: bool):
        """Evaluate the internal affirmation against external constraints.

        - If the internal 'Yes' signal exists and a user constraint is active,
          return the token fallback (suppressed/controlled output).
        - If the internal 'Yes' exists and no constraint is active, return "Yes".
        - If the internal signal is not present, return "No".
        """
        internal_signal = bool(self.raw_affirmation) if query_is_factual_yes else False

        if internal_signal:
            if self.constraint:
                return self.finalize_output(override=True)
            return self.finalize_output(override=False)

        return "No"

    def finalize_output(self, override: bool):
        return self.token_fallback if override else "Yes"


import hashlib
import secrets


class ZkInternalMonitor(InternalMonitor):
    """A 'Zk' variant of InternalMonitor that can produce simple
    cryptographic commitments (proof-like objects) for its internal state.

    This is a lightweight, test-friendly commitment (SHA-256 + nonce).
    It is NOT a real zero-knowledge proof system; it's a deterministic
    commitment/verify helper suitable for unit tests and audits.
    """

    def prove(self, query_is_factual_yes: bool) -> dict:
        """Produce a commitment + nonce and include the public output.

        The commitment binds the internal signal, the active constraint and
        the fallback token using a random nonce. The returned structure is
        suitable for later verification using `verify_proof`.
        """
        internal_signal = bool(self.raw_affirmation) if query_is_factual_yes else False
        nonce = secrets.token_hex(16)
        msg = f"{internal_signal}:{self.constraint}:{self.token_fallback}"
        commitment = hashlib.sha256((nonce + msg).encode("utf-8")).hexdigest()
        return {"commitment": commitment, "nonce": nonce, "public_result": self.process_query(query_is_factual_yes)}

    @staticmethod
    def verify_proof(commitment: str, nonce: str, asserted_internal_signal: bool, constraint: bool, token_fallback: str) -> bool:
        """Verify a commitment was produced from the provided values.

        The verifier must supply the asserted internal signal (True/False)
        along with the constraint and token_fallback values used to create
        the commitment.
        """
        msg = f"{asserted_internal_signal}:{constraint}:{token_fallback}"
        expected = hashlib.sha256((nonce + msg).encode("utf-8")).hexdigest()
        return expected == commitment


__all__ = ["InternalMonitor", "ZkInternalMonitor"]
