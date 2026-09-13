# Online Voting System — Test Cases

| Test | Input or action | Expected outcome |
| --- | --- | --- |
| Valid vote | Registered `V1` submits candidate `C1` in time | `ACCEPTED`; C1 gets one vote. |
| Repeat vote | Submit `V1`, `C1` twice | Second attempt is `ALREADY_VOTED`; total remains one. |
| Unknown voter | Submit `V9`, `C1` | `UNKNOWN_VOTER`; count does not change. |
| Unknown candidate | Submit `V1`, `C9` | `UNKNOWN_CANDIDATE`; voter can try again with a valid candidate. |
| Duplicate registration | Add two voters with ID `V1` | Second registration is rejected. |
| Closed window | Submit after the configured duration | `WINDOW_CLOSED`; no vote is added. |
| Tie | One vote each for C1 and C2 | Result reports a tie. |
| Export | Type `exit` after voting | `voting-results.txt` contains candidate, party, count, and outcome. |

## Sample session

```text
Enter voting duration in minutes: 30
How many candidates? 1
Candidate ID: C1
Candidate name: Asha Patel
Political party: Progress Party
How many registered voters? 1
Voter ID: V1
Voter name: Meera Singh
Voter ID: V1
Candidate ID: C1
ACCEPTED: Vote recorded successfully.
Voter ID: exit
```
