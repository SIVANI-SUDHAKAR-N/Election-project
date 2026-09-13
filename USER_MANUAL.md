# Online Voting System — User Manual

## Requirements

Install JDK 11 or later and open PowerShell in this project folder.

## Run

```powershell
javac *.java
java Main
```

## Steps

1. Enter the voting duration in minutes.
2. Enter the number of candidates, then each candidate's ID, name, and political party.
3. Enter the number of voters, then each voter's ID and name.
4. Each voter enters their registered ID and one candidate ID.
5. Type `exit` at the voter ID prompt to close the console session.
6. Review the results on screen and open `voting-results.txt` for the exported report.

`ACCEPTED` means a vote was saved. Other status messages explain a rejected vote, such as an unknown voter, unknown candidate, duplicate vote, or closed time window.
