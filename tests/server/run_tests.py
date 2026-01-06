#!/usr/bin/env python3
"""
Test runner for all testrift-server tests.
"""

from pathlib import Path

import pytest


def run_all_tests() -> int:
    test_dir = Path(__file__).parent
    return pytest.main(
        [
            str(test_dir),
            "-v",
            "--tb=short",
            "-x",  # stop on first failure
        ]
    )


if __name__ == "__main__":
    raise SystemExit(run_all_tests())
