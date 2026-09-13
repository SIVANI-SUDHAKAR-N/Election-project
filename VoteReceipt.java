import java.time.Instant;
public final class VoteReceipt {
    private final VoteStatus status;
    private final Instant processedAt;
    private final String message;

    public VoteReceipt(VoteStatus status, Instant processedAt, String message) {
        this.status = status;
        this.processedAt = processedAt;
        this.message = message;
    }

    public VoteStatus getStatus() { return status; }
    public Instant getProcessedAt() { return processedAt; }
    public String getMessage() { return message; }
    public boolean isAccepted() { return status == VoteStatus.ACCEPTED; }
}
