import os
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from mypy import api
from pylama.context import RunContext
from pylama.lint import LinterV2 as Abstract

regexes = {
    "dmypy_message": re.compile(
        r"(?P<filename>[^:]+):(?P<lnum>\d+):(?P<col>\d+): (?P<type>\w+): (?P<message>.+)"
    )
}


class CachedResult:
    @classmethod
    def create(cls, root, stdout):
        results = defaultdict(list)
        for line in stdout.splitlines():
            if not line:
                continue

            m = regexes["dmypy_message"].match(line)
            if not m:
                continue

            groups = m.groupdict()

            location = root / groups["filename"]

            lnum = int(groups["lnum"])
            col = int(groups["col"])
            mtype = groups["type"][0].upper()
            text = groups["message"].strip()

            results[location].append(
                {"source": "dmypy", "lnum": lnum, "col": col, "type": mtype, "text": text}
            )

        return cls(root, datetime.now(), results)

    def __init__(self, root, when, results):
        self.root = root
        self.when = when
        self.results = results

    @property
    def expired(self):
        return (datetime.now() - self.when).seconds > 60

    def add(self, ctx):
        location = Path(ctx.filename).resolve()
        for info in self.results[location]:
            ctx.push(**info)


cached_results = {}


class Linter(Abstract):
    name = "dmypy"

    def run_check(self, ctx: RunContext):
        """Check code with dmypy."""
        results_or_error = self.check_root(ctx.filename)
        if isinstance(results_or_error, str):
            ctx.push(source="dmypy", lnum=1, col=1, type="E", text=results_or_error)
            return

        results_or_error.add(ctx)

    def check_root(self, filename: str):
        root = Path("/")
        home = Path.home()
        location = Path(filename).resolve().parent

        markers = [".git", "setup.py", "setup.cfg", "pyproject.toml", "mypy.ini"]

        while True:
            files = [f.name for f in location.iterdir()]
            if any(mark in files for mark in markers):
                break
            if location.parent in (root, home):
                break
            location = location.parent

        if location.parent in (root, home):
            return "Failed to find root of the project"

        if location in cached_results and not cached_results[location].expired:
            return cached_results[location]

        cwd = Path.cwd()
        try:
            os.chdir(location)

            _, errors, exit_status = api.run_dmypy(["status"])
            if exit_status != 0:
                api.run_dmypy(["restart"])

            stdout, errors, ret = api.run_dmypy(["run", "--", ".", "--show-column-numbers"])
            cached_results[location] = CachedResult.create(location, stdout)
        finally:
            os.chdir(cwd)

        return cached_results[location]
