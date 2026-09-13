import java.time.Instant;
import java.util.Collections;
import java.util.List;
public final class ElectionResult {
    private final List<Candidate> candidates;
    private final List<Candidate> leaders;
    private final int totalVotes;
    private final Instant generatedAt;

    ElectionResult(List<Candidate> candidates, List<Candidate> leaders,
                   int totalVotes, Instant generatedAt) {
        this.candidates = Collections.unmodifiableList(candidates);
        this.leaders = Collections.unmodifiableList(leaders);
        this.totalVotes = totalVotes;
        this.generatedAt = generatedAt;
    }

    public List<Candidate> getCandidates() { return candidates; }
    public List<Candidate> getLeaders() { return leaders; }
    public int getTotalVotes() { return totalVotes; }
    public Instant getGeneratedAt() { return generatedAt; }
    public boolean hasVotes() { return totalVotes > 0; }
    public boolean isTie() { return leaders.size() > 1; }
}
