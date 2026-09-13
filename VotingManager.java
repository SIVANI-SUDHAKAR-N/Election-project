import java.time.Clock;
import java.time.Instant;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/** Handles voter authentication, vote validation, result calculation, and vote storage. */
public final class VotingManager {
    private final Map<String, Voter> voters = new LinkedHashMap<>();
    private final Map<String, Candidate> candidates = new LinkedHashMap<>();
    private final List<Vote> votes = new ArrayList<>();
    private final Instant openingTime;
    private final Instant closingTime;
    private final Clock clock;

    public VotingManager(Instant openingTime, Instant closingTime, Clock clock) {
        if (openingTime == null || closingTime == null || clock == null || !openingTime.isBefore(closingTime)) {
            throw new IllegalArgumentException("Opening time must be before closing time.");
        }
        this.openingTime = openingTime;
        this.closingTime = closingTime;
        this.clock = clock;
    }

    public void registerVoter(Voter voter) {
        if (voter == null) throw new IllegalArgumentException("Voter is required.");
        if (voters.putIfAbsent(voter.getId(), voter) != null) {
            throw new IllegalArgumentException("Duplicate voter ID: " + voter.getId());
        }
    }

    public void registerCandidate(Candidate candidate) {
        if (candidate == null) throw new IllegalArgumentException("Candidate is required.");
        if (candidates.putIfAbsent(candidate.getId(), candidate) != null) {
            throw new IllegalArgumentException("Duplicate candidate ID: " + candidate.getId());
        }
    }

    /** Authentication is performed by checking the supplied ID against registered voters. */
    public boolean authenticateVoter(String voterId) {
        return voters.containsKey(normalize(voterId));
    }

    /** A synchronized operation ensures one voter ID cannot succeed twice concurrently. */
    public synchronized VoteReceipt castVote(String voterId, String candidateId) {
        Instant now = clock.instant();
        if (now.isBefore(openingTime) || now.isAfter(closingTime)) {
            return receipt(VoteStatus.WINDOW_CLOSED, now, "Voting is currently closed.");
        }
        Voter voter = voters.get(normalize(voterId));
        if (voter == null) return receipt(VoteStatus.UNKNOWN_VOTER, now, "Voter authentication failed.");
        if (voter.hasVoted()) return receipt(VoteStatus.ALREADY_VOTED, now, "This voter has already cast a ballot.");
        Candidate candidate = candidates.get(normalize(candidateId));
        if (candidate == null) return receipt(VoteStatus.UNKNOWN_CANDIDATE, now, "Candidate ID does not exist.");

        votes.add(new Vote(voter, candidate, now));
        candidate.recordVote();
        voter.markVoted();
        return receipt(VoteStatus.ACCEPTED, now, "Vote recorded successfully.");
    }

    public synchronized ElectionResult results() {
        List<Candidate> ranked = new ArrayList<>(candidates.values());
        ranked.sort(Comparator.comparingInt(Candidate::getVoteCount).reversed().thenComparing(Candidate::getName));
        List<Candidate> leaders = new ArrayList<>();
        if (!votes.isEmpty() && !ranked.isEmpty()) {
            int highScore = ranked.get(0).getVoteCount();
            for (Candidate candidate : ranked) {
                if (candidate.getVoteCount() != highScore) break;
                leaders.add(candidate);
            }
        }
        return new ElectionResult(ranked, leaders, votes.size(), clock.instant());
    }

    private VoteReceipt receipt(VoteStatus status, Instant time, String message) {
        return new VoteReceipt(status, time, message);
    }
    private static String normalize(String value) { return value == null ? "" : value.trim(); }
}
