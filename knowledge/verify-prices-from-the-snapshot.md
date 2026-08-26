# Never state a price, multiple or return without pulling it that session

Standing rule for this workspace, mirroring the gamerun rule "verify against code, not memory".

Every number in this knowledge base was true when written and decays from that moment.
Multiples decay fastest because the numerator moves every day while the file does not.

**How to apply:** run `scripts/fetch_daily.py` before reasoning about any price. If a number
appears in a journal note without a matching row in that day's snapshot, it should not be there.
Fundamentals live in `data/fundamentals/` with a date in the filename; anything older than a
week gets refreshed before it is quoted. Related: [[data-quality-rules]] in `playbooks/`.
