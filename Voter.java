/** Stores voter eligibility separately from the candidate they select. */
public final class Voter {
    private final String id;
    private final String name;
    private boolean hasVoted;
    public Voter(String id, String name) {
        this.id = validateText(id, "Voter ID");
        this.name = validateText(name, "Voter name");
    }

    public String getId() { return id; }
    public String getName() { return name; }
    public boolean hasVoted() { return hasVoted; }

    void markVoted() { hasVoted = true; }

    private static String validateText(String value, String fieldName) {
        if (value == null || value.trim().isEmpty()) {
            throw new IllegalArgumentException(fieldName + " cannot be blank.");
        }
        return value.trim();
    }
}
