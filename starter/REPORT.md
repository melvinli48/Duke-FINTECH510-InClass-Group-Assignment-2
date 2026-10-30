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

**Q2. Within 2 hops of ACCT-50117.** List the accounts and hop counts.
ACCT-10234 exchanged money with ACCT-50117. Why is it not on the list?

**Q3. Shortest chain to ACCT-90001.** Give the chain. Name one other chain the
money could have taken, and say why BFS did not return it.

**Q4. Round trip.** What did `find_round_trip` print **before** you fixed
`ai_review.py`, and what does it print after? Which wire in the "before" chain
does not exist in the log?
