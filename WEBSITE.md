# Janmat — The People's Vote

A small, self-contained website inspired by the Java election management system in this folder. It keeps the original ideas—registered voter IDs, candidate registration, one vote per voter, receipts, and a live result tally—in a browser-based demonstration.

## Open the website

Open `index.html` in a modern browser. No build step or server is required.

## Try the sample election

Use any of these registered voter IDs in the ballot:

- `VOTER-001`
- `VOTER-002`
- `VOTER-003`
- `VOTER-004`
- `VOTER-005`
- `VOTER-006`

Each ID can cast one vote in this browser. The tally and election setup are stored in that browser's local storage. Use **Election organiser** near the bottom of the page to edit candidates and voter IDs, or restore the sample election.

## Scope

This is a front-end demo for exploring the voting flow. Browser local storage is not a secure election database and does not sync across devices. The Java console application remains available through `java Main` and is documented in the project README and source files in this folder.
