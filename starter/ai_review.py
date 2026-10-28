# This module was written by an AI coding assistant. The prompt was:
#
#   "Write two helper functions for our wire-fraud tool.
#    1. extract_refs(text): return every invoice reference in a memo.
#       An invoice reference is INV- followed by exactly 4 digits,
#       e.g. INV-3341.
#    2. find_round_trip(graph, start): the graph is an adjacency dict
#       {account: [(dest, amount), ...]}. Return a chain of accounts showing
#       money leaving start and coming back to it, like [start, ..., start], or
#       [] if money never comes back."
#
# It looks reasonable. It is not. Your job is to find out why.

import re


def extract_refs(text: str) -> list[str]:
    """Return every INV reference followed by exactly four digits."""
    pattern = r"(?<![A-Za-z0-9])INV-[0-9]{4}(?![0-9-])"
    return re.findall(pattern, text)


def _visit(graph, account, start, path):
    for dest, _ in graph.get(account, []):
        if dest == start:
            path.append(dest)
            return True
        if dest not in path:
            path.append(dest)

            if _visit(graph, dest, start, path):
                return True

            path.pop()

    return False


def find_round_trip(graph: dict, start: str) -> list[str]:
    """Return a path back to start, or an empty list when none exists."""
    path = [start]
    if _visit(graph, start, start, path):
        return path
    return []
