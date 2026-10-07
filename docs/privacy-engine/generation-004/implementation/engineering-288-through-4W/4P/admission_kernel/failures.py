"""S83/S90 inherited failure order, copied as data, never redefined by callers."""
ORDER = ('INVALID-PROFILE-SCHEMA', 'PROFILE-DIGEST-MISMATCH', 'INVALID-EVIDENCE-AUTHORITY',
         'MISSING-EVIDENCE', 'INVALID-EVIDENCE-AUTHENTICATION', 'INVALID-EVIDENCE-DIGEST',
         'INVALID-SURFACE-LABELS', 'INVALID-ACTION-CONTEXT', 'INCOMPLETE-EVIDENCE-UNIVERSE',
         'COMPONENT-COUNT-MISMATCH', 'UNNECESSARY-COMPONENT', 'PUBLIC-PRIVATE-VALUE',
         'REUSABLE-IDENTIFIER', 'OPENING-DISCLOSURE', 'UNIQUENESS-FAILURE',
         'CORRELATION-FAILURE', 'ACTOR-RECONSTRUCTION-RISK', 'COMPONENT-FAILURE')
EXPERIMENT_FAILURE = {'COLLISION': 'UNIQUENESS-FAILURE',
                      'CROSS-ACTION-TRACKING': 'CORRELATION-FAILURE',
                      'ACTOR-INFORMATION': 'ACTOR-RECONSTRUCTION-RISK'}


class Failures:
    def __init__(self):
        self.reasons = {}

    def add(self, code, detail):
        if code not in ORDER:
            raise ValueError('No new external failure vocabulary: ' + str(code))
        self.reasons.setdefault(code, []).append(detail)

    def result(self, mode, bindings=None):
        ordered = [code for code in ORDER if code in self.reasons]
        return {'result': 'REJECTED' if ordered else 'CONDITIONAL-BINDING-AND-ADMISSION-CHECKS-PASS',
                'earliest_failure': ordered[0] if ordered else 'NONE', 'failures': ordered,
                'reasons': self.reasons, 'mode': mode, 'bindings': bindings or {},
                'profile_admitted': False, 'actual_qualification_established': False,
                'runtime_effect_performed': False, 'full_model_integration_witness': False}
