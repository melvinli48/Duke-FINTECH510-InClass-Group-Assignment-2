# Report — Follow the Money

**Group members and roles**

| Name | Role (Parser / Searcher / Reviewer) |
|---|---|
|Iris|Reviewer|
|Mia|Parser|
|Max|Searcher|
|Melvin|Reviewer,Searcher|

---

## Part C — AI code review

One row per bug. "Failing test" is the test function name in
`test_ai_review.py`.

| # | Function | Failing test | Input that triggers it | What the AI's code did | What it should do | Your fix |
|---|---|---|---|---|---|---|
| 1 | `extract_refs` | `test_extract_refs_allows_zero_digit` | `"Payment for INV-0000"` | Returned `[]` | Return `["INV-0000"]` | Changed the regex digit range from `[1-9]` to `[0-9]`. |
| 2 | `extract_refs` | `test_extract_refs_requires_exactly_four_digits` | `"Payment for INV-12345"` | Returned `["INV-1234"]` | Return `[]` | Added regex boundary checks so a match is not extracted from a longer numeric reference. |
| 3 | `find_round_trip` | `test_find_round_trip_dead_end_does_not_pollute_result` | Dead end `A→B→C`, followed by valid path `A→D→A` | Returned `["A", "B", "C", "D", "A"]` | Return `["A", "D", "A"]` | Added `path.pop()` after an unsuccessful recursive search to backtrack and remove the dead-end node. |
| 4 | `find_round_trip` | `test_find_round_trip_cycle_not_returning_to_start_terminates` | Graph `A→B→C→B`, starting at `A` | Raised `RecursionError` | Return `[]` without infinite recursion | Checked whether `dest` was already in the current path before recursing, preventing repeated visits within a cycle. |

---

## Part D — Investigation

Run `python wire_trace.py ../data/wires.txt` from `starter/`.

**Q1. Rejected lines.** How many lines were rejected? For each one, which rule
does it break?

The program loaded 28 wires and rejected 6 lines. The blank line was skipped.

| Rejected line | Rule it breaks |
|---|---|
| `2026-10-06 10:02 WIRE $4,200.00 from ACCT-2045 to ACCT-33010 ref INV-1060` | The sender account has only 4 digits; accounts must have exactly 5 digits after `ACCT-`. |
| `2026-10-07 11:40 WIRE $1,150.00 from acct-20789 to ACCT-41122 ref INV-1071` | The sender account uses lowercase `acct-`; the prefix must be uppercase `ACCT-`. |
| `2026-10-08 09:05 WIRE 3,000.00 from ACCT-41500 to ACCT-20456 ref INV-1080` | The amount is missing its `$` sign. |
| `2026-10-09 14:22 ACH $850.00 from ACCT-20456 to ACCT-33010 ref INV-1090` | The transfer type is `ACH`; only `WIRE` is accepted. |
| `2026-10-10 16:18 WIRE $9,900.00 from ACCT-61204 ref INV-3310` | The `to` clause and destination account are missing. |
| `2026-10-12 09:30 WIRE $9,800.5 from ACCT-33010 to ACCT-90001 ref INV-3311` | The amount has only 1 digit of cents; cents must have exactly 2 digits when present. |

**Q2. Within 2 hops of ACCT-50117.** List the accounts and hop counts.
ACCT-10234 exchanged money with ACCT-50117. Why is it not on the list?

| Account | Fewest hops from ACCT-50117 |
|---|---|
| `ACCT-33010` | 1 |
| `ACCT-61204` | 1 |
| `ACCT-61388` | 1 |
| `ACCT-41122` | 2 |
| `ACCT-72019` | 2 |
| `ACCT-73550` | 2 |

`ACCT-10234` sent money to `ACCT-50117`. The graph is directed, so this creates
an edge `ACCT-10234 -> ACCT-50117`, not an edge in the reverse direction.
There is no outgoing path from `ACCT-50117` to `ACCT-10234`, so it is not listed.

**Q3. Shortest chain to ACCT-90001.** Give the chain. Name one other chain the
money could have taken, and say why BFS did not return it.

The shortest chain uses 3 wires:

```text
ACCT-50117 -> ACCT-61204 -> ACCT-72019 -> ACCT-90001
```

Another possible chain uses 4 wires:

```text
ACCT-50117 -> ACCT-61388 -> ACCT-73550 -> ACCT-84102 -> ACCT-90001
```

BFS explores accounts one hop at a time, so it reaches `ACCT-90001` through
the 3-wire chain before reaching it through the 4-wire chain. It minimizes
the number of wires, regardless of their dollar amounts. DFS could follow
the longer branch first and would not guarantee the fewest hops.

**Q4. Round trip.** What did `find_round_trip` print **before** you fixed
`ai_review.py`, and what does it print after? Which wire in the "before" chain
does not exist in the log?

Using the original `ai_review.py` recovered from Git history, with working
Parts A and B, the investigation printed:

```text
ACCT-50117 -> ACCT-61388 -> ACCT-73550 -> ACCT-84102 -> ACCT-90001 -> ACCT-50117
```

Using the fixed `ai_review.py`, it printed:

```text
ACCT-50117 -> ACCT-61388 -> ACCT-73550 -> ACCT-84102 -> ACCT-50117
```

The wire `ACCT-90001 -> ACCT-50117` in the original output does not exist in
the log. The original search visited the dead end `ACCT-90001` but left it
in the path when backtracking. The actual return wire is
`ACCT-84102 -> ACCT-50117` (`INV-3309`). Adding `path.pop()` removes the
dead-end account, so the fixed output contains only real connections.
