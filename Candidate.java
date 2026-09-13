/** Represents one person standing in the election. */
public final class Candidate {
    private final String id;
    private final String name;
    private final String politicalParty;
    private int voteCount;

    public Candidate(String id, String name, String politicalParty) {
        this.id = validateText(id, "Candidate ID");
        this.name = validateText(name, "Candidate name");
        this.politicalParty = validateText(politicalParty, "Political party");
    }

    public String getId() { return id; }
    public String getName() { return name; }
    public String getPoliticalParty() { return politicalParty; }
    public int getVoteCount() { return voteCount; }

    // Only the voting service should call this after it validates a ballot.
    void recordVote() { voteCount++; }

    private static String validateText(String value, String fieldName) {
        if (value == null || value.trim().isEmpty()) {
            throw new IllegalArgumentException(fieldName + " cannot be blank.");
        }
        return value.trim();
    }
}
