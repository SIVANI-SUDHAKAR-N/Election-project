import java.io.IOException;
import java.nio.file.Path;
import java.time.Clock;
import java.time.Duration;
import java.time.Instant;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Clock clock = Clock.systemUTC();
        try (Scanner input = new Scanner(System.in)) {
            System.out.println("=== ONLINE VOTING SYSTEM ===\n");
            VotingManager election = createElection(input, clock);

            System.out.println("\nPolling is open. Enter 'exit' as a voter ID to close voting and export results.\n");
            while (true) {
                System.out.print("Voter ID: "); String voterId = input.nextLine().trim();
                if (voterId.equalsIgnoreCase("exit")) break;
                System.out.print("Candidate ID: "); String candidateId = input.nextLine().trim();
                if (candidateId.equalsIgnoreCase("exit")) break;
                VoteReceipt receipt = election.castVote(voterId, candidateId);
                System.out.println(receipt.getStatus() + ": " + receipt.getMessage());
            }

            ElectionResult result = election.results();
            printSummary(result);
            Path exportPath = Path.of("voting-results.txt").toAbsolutePath();
            try {
                ResultsExporter.exportTextReport(result, exportPath);
                System.out.println("Results exported to: " + exportPath);
            } catch (IOException error) {
                System.err.println("Could not export results: " + error.getMessage());
            }
        }
    }

    private static VotingManager createElection(Scanner input, Clock clock) {
        int durationMinutes = readPositiveNumber(input, "Enter voting duration in minutes: ");
        Instant openingTime = clock.instant();
        VotingManager election = new VotingManager(
                openingTime,
                openingTime.plus(Duration.ofMinutes(durationMinutes)),
                clock);

        int candidateCount = readPositiveNumber(input, "How many candidates? ");
        for (int number = 1; number <= candidateCount; number++) {
            System.out.println("\nCandidate " + number);
            String id = readRequiredText(input, "Candidate ID: ");
            String name = readRequiredText(input, "Candidate name: ");
            String party = readRequiredText(input, "Political party: ");
            try {
                election.registerCandidate(new Candidate(id, name, party));
            } catch (IllegalArgumentException error) {
                System.out.println(error.getMessage() + " Please enter this candidate again.");
                number--;
            }
        }

        int voterCount = readPositiveNumber(input, "\nHow many registered voters? ");
        for (int number = 1; number <= voterCount; number++) {
            System.out.println("\nVoter " + number);
            String id = readRequiredText(input, "Voter ID: ");
            String name = readRequiredText(input, "Voter name: ");
            try {
                election.registerVoter(new Voter(id, name));
            } catch (IllegalArgumentException error) {
                System.out.println(error.getMessage() + " Please enter this voter again.");
                number--;
            }
        }
        return election;
    }

    private static int readPositiveNumber(Scanner input, String prompt) {
        while (true) {
            System.out.print(prompt);
            String response = input.nextLine().trim();
            try {
                int value = Integer.parseInt(response);
                if (value > 0) return value;
            } catch (NumberFormatException ignored) {
                // The message below explains the expected input.
            }
            System.out.println("Please enter a whole number greater than zero.");
        }
    }

    private static String readRequiredText(Scanner input, String prompt) {
        while (true) {
            System.out.print(prompt);
            String response = input.nextLine().trim();
            if (!response.isEmpty()) return response;
            System.out.println("This field cannot be blank.");
        }
    }
    private static void printSummary(ElectionResult result) {
        System.out.println("\n--- ELECTION RESULTS ---");
        System.out.printf("%-8s %-24s %-20s %s%n", "ID", "Candidate", "Political Party", "Votes");
        for (Candidate c : result.getCandidates()) {
            System.out.printf("%-8s %-24s %-20s %d%n", c.getId(), c.getName(), c.getPoliticalParty(), c.getVoteCount());
        }
        System.out.println("Total votes: " + result.getTotalVotes());
        if (!result.hasVotes()) System.out.println("Outcome: No votes cast.");
        else if (result.isTie()) System.out.println("Outcome: Tie between " + result.getLeaders().stream().map(Candidate::getName).reduce((a, b) -> a + " and " + b).orElse(""));
        else System.out.println("Winner: " + result.getLeaders().get(0).getName());
    }
}
