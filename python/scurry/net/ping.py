import subprocess
import typing

from dataclasses import dataclass


@dataclass
class PingHostResult:
    def __init__(self, host: str, sequence: int, latency: float):
        self.host = host
        self.latency = latency
        self.sequence = sequence


@dataclass
class PingResults:
    def __init__(self):
        self.results: typing.List[PingHostResult] = []

    def __len__(self):
        return len(self.results)


def parse_ping_line(line: str):
    parts = line.split(" ")

    host = parts[3].rstrip(":")

    sequence = int(parts[4].split("=")[1])
    latency = float(parts[6].split("=")[1])

    return PingHostResult(host=host, sequence=sequence, latency=latency)


def ping(host: str, count: int = 3) -> PingResults:
    results = subprocess.run(
        ["ping", "-c", str(count), host],
        capture_output=True,
    )

    ret = PingResults()

    for line in results.stdout.decode("utf-8").split("\n")[1:]:
        if not line.startswith("64 bytes from "):
            continue
        result = parse_ping_line(line)
        ret.results.append(result)

    return ret
