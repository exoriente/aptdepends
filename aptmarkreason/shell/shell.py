from subprocess import run
from typing import Iterable, Sequence, Tuple


def make_call_to_shell(
    command: Sequence[str],
) -> Tuple[int, Iterable[str], Iterable[str]]:
    result = run(command, capture_output=True)
    return (
        result.returncode,
        result.stdout.decode().splitlines(),
        result.stderr.decode().splitlines(),
    )
