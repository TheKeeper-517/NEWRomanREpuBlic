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


__all__ = ["InternalMonitor"]
