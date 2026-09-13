# Online Voting System — Design Document

## Class design

| Class | Attributes | Main methods | Purpose |
| --- | --- | --- | --- |
| `Voter` | ID, name, `hasVoted` | getters, `hasVoted()`, `markVoted()` | Stores a registered voter's eligibility. |
| `Candidate` | ID, name, political party, vote count | getters, `recordVote()` | Stores a candidate and their total. |
| `Vote` | voter, candidate, timestamp | getters | Represents one accepted ballot. |
| `VotingManager` | voter registry, candidate registry, votes, opening/closing time | registration, `authenticateVoter()`, `castVote()`, `results()` | Applies election rules and produces results. |
| `ElectionResult` | ranked candidates, leaders, total, generated time | getters, `hasVotes()`, `isTie()` | Read-only result snapshot. |
| `ResultsExporter` | none | `exportTextReport()` | Writes the final text report. |

## Relationships

`VotingManager` manages many `Voter`, `Candidate`, and `Vote` objects. Each `Vote` connects one voter to one candidate with a timestamp. `ResultsExporter` receives an `ElectionResult` from the manager.

## Validation

- Voter and candidate IDs cannot be blank or duplicated.
- A voter ID must exist in the registry to authenticate.
- Votes before opening or after closing are rejected.
- A voter is marked as voted only after the candidate is valid and the vote is recorded.
- `castVote()` is synchronized, preventing concurrent repeat voting with one ID.
