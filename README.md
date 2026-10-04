# Election Management System

A Java-based election management project that lets a user register candidates and voters, record votes, generate receipts, and display collective results. The project demonstrates object-oriented design through classes such as `Candidate`, `Voter`, `Vote`, `VoteReceipt`, and `VotingManager`.

## Overview

This system models a simple election workflow:

- Register candidates with unique IDs and party details
- Register voters with unique IDs and names
- Accept votes for valid candidates only
- Prevent duplicate voting by the same registered voter
- Produce a receipt for each vote attempt
- Calculate election totals and identify leaders or ties
- Export results to output files

## Features

- Candidate registration and validation
- Voter registration and validation
- Vote casting with status tracking
- Duplicate-vote prevention
- Receipt generation for each vote
- Election result summary and winner detection
- Text and CSV export support
- Console-based user interaction

## Project files

- `Main.java` – entry point for the console application
- `VotingManager.java` – core election logic
- `Candidate.java` – candidate model
- `Voter.java` – voter model
- `Vote.java` – vote record
- `VoteReceipt.java` – vote outcome and message output
- `VoteStatus.java` – vote status enum
- `ElectionResult.java` – final election calculation results
- `ResultsExporter.java` – exports election results to files
- `voting-results.txt` and `voting-results.csv` – generated outputs

## How to run

From the project folder, compile and run:

```bash
javac *.java
java Main
```

When the program starts, it asks for:

1. Voting duration in minutes
2. Number of candidates
3. Candidate details
4. Number of registered voters
5. Voter details

Then it enters the voting loop until you type `exit` as the voter ID.

## Browser demo

This repository also includes a browser-based prototype for viewing the election flow in a webpage. To try it, open `index.html` in a browser.

## Notes

This project is designed as a demonstration of Java OOP and console-based election logic. It does not replace a production-grade election system or a secure database-backed voting platform.
