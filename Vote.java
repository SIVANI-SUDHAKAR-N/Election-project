import java.time.Instant;

/** One accepted ballot, linking a voter, candidate, and submission time. */
public final class Vote {
    private final Voter voter;
    private final Candidate candidate;
    private final Instant timestamp;

    public Vote(Voter voter, Candidate candidate, Instant timestamp) {
        if (voter == null || candidate == null || timestamp == null) {
            throw new IllegalArgumentException("A vote needs a voter, candidate, and timestamp.");
        }
        this.voter = voter;
        this.candidate = candidate;
        this.timestamp = timestamp;
    }

    public Voter getVoter() { return voter; }
    public Candidate getCandidate() { return candidate; }
    public Instant getTimestamp() { return timestamp; }
}
