import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
/** Produces a plain-text final election report. */
public final class ResultsExporter {
    private ResultsExporter() { }

    public static void exportTextReport(ElectionResult result, Path destination) throws IOException {
        StringBuilder out = new StringBuilder();
        out.append("ONLINE VOTING SYSTEM - FINAL RESULTS\n");
        out.append("Generated at: ").append(result.getGeneratedAt()).append("\n");
        out.append("Total votes cast: ").append(result.getTotalVotes()).append("\n\n");
        out.append(String.format("%-12s %-24s %-20s %s%n", "ID", "Candidate", "Political Party", "Votes"));
        out.append("---------------------------------------------------------------------\n");
        for (Candidate candidate : result.getCandidates()) {
            out.append(String.format("%-12s %-24s %-20s %d%n", candidate.getId(), candidate.getName(),
                    candidate.getPoliticalParty(), candidate.getVoteCount()));
        }
        out.append("\nOutcome: ");
        if (!result.hasVotes()) {
            out.append("No votes cast");
        } else if (result.isTie()) {
            out.append("Tie: ").append(names(result));
        } else {
            out.append("Winner: ").append(result.getLeaders().get(0).getName());
        }
        Files.writeString(destination, out.toString(), StandardCharsets.UTF_8);
    }

    private static String names(ElectionResult result) { return result.getLeaders().stream().map(Candidate::getName).reduce((a, b) -> a + "; " + b).orElse(""); }
}
