# Host marker repair — version 2

The supplied Ubuntu failure is a checker syntax limitation, not a candidate/runtime defect. The exact cffi 2.1.1 requirement is `pycparser; implementation_name != "PyPy"`. `implementation_name` is now read from `sys.implementation.name`; the comparison remains case-sensitive and unchanged. It is not replaced by platform.python_implementation(), and the dependency is not skipped.

One line of code/dependency_check.py changed. Eleven fresh focused controls reproduce the old rejection, check true/false and exact case semantics, ensure pycparser is actually required, reject missing dependencies/unknown names/calls, and check fresh-process behavior. The original 44 BR controls are reused, not rerun or relabelled. The candidate, launcher, runtime source bytes, lock, environment pins and public gate are unchanged. The failed checker and supplied host transcript remain under failures/.

Host version evidence remains supported by the supplied addendum. Successful public runtime compatibility is still pending the Ubuntu command; no new host execution is claimed. Original ENVIRONMENT/COMPATIBILITY report bodies remain to be captured for separate semantic reconciliation. No persistent session is authorized.

This v2 ZIP replaces the correction transport for review. Keep the original correction and reviews unchanged. UBUNTU-VERIFY.sh is unchanged and still uses only fresh temporary state. No install, lifecycle, policy/limit change or persistent initialization occurs. SOURCE-ONLY; readiness/final binding BLOCKED; streams UNCOMPUTED; admission disabled.
