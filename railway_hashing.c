#include <stdio.h>

#define TABLE_SIZE 13
#define BOOKING_COUNT 7

static const int booking_ids[BOOKING_COUNT] = {23, 43, 13, 33, 53, 63, 73};

typedef enum {
    LINEAR,
    QUADRATIC,
    DOUBLE_HASHING
} ProbeMethod;

static int primary_hash(int key) {
    return key % 10;
}

static int secondary_hash(int key) {
    return 1 + key % 11;
}

static int probe_index(int key, int attempt, ProbeMethod method) {
    int index;

    switch (method) {
        case LINEAR:
            index = primary_hash(key) + attempt;
            break;
        case QUADRATIC:
            index = primary_hash(key) + attempt * attempt;
            break;
        case DOUBLE_HASHING:
            index = primary_hash(key) + attempt * secondary_hash(key);
            break;
        default:
            return -1;
    }

    return index % TABLE_SIZE;
}

static void insert(int table[TABLE_SIZE], int key, ProbeMethod method) {
    for (int attempt = 0; attempt < TABLE_SIZE; ++attempt) {
        int index = probe_index(key, attempt, method);
        if (table[index] == -1) {
            table[index] = key;
            return;
        }
    }

    fprintf(stderr, "Insertion failed for booking ID %d\n", key);
}

/* Returns probes through the found key or first empty slot. */
static int search(const int table[TABLE_SIZE], int key, ProbeMethod method) {
    for (int attempt = 0; attempt < TABLE_SIZE; ++attempt) {
        int index = probe_index(key, attempt, method);
        if (table[index] == key || table[index] == -1) {
            return attempt + 1;
        }
    }

    return TABLE_SIZE;
}

static void print_table(const char *name, const int table[TABLE_SIZE]) {
    printf("\n%s\nIndex: ", name);
    for (int i = 0; i < TABLE_SIZE; ++i) {
        printf("%3d", i);
    }

    printf("\nValue: ");
    for (int i = 0; i < TABLE_SIZE; ++i) {
        if (table[i] == -1) {
            printf("%3s", "-");
        } else {
            printf("%3d", table[i]);
        }
    }
    putchar('\n');
}

int main(void) {
    int tables[3][TABLE_SIZE];
    const ProbeMethod methods[3] = {LINEAR, QUADRATIC, DOUBLE_HASHING};
    const char *names[3] = {"Linear Probing", "Quadratic Probing", "Double Hashing"};
    const int search_keys[] = {23, 73, 80};

    for (int method = 0; method < 3; ++method) {
        for (int i = 0; i < TABLE_SIZE; ++i) {
            tables[method][i] = -1;
        }
        for (int i = 0; i < BOOKING_COUNT; ++i) {
            insert(tables[method], booking_ids[i], methods[method]);
        }
        print_table(names[method], tables[method]);
    }

    printf("\nSearch probe counts\n");
    printf("Key   Result       Linear  Quadratic  Double Hashing\n");
    for (unsigned int i = 0; i < sizeof(search_keys) / sizeof(search_keys[0]); ++i) {
        int key = search_keys[i];
        int found = key == 23 || key == 73;
        printf("%-5d %-12s %-7d %-10d %d\n",
               key, found ? "Found" : "Not found",
               search(tables[0], key, LINEAR),
               search(tables[1], key, QUADRATIC),
               search(tables[2], key, DOUBLE_HASHING));
    }

    printf("\nLoad factor = %d / %d = %.3f (%.1f%%)\n",
           BOOKING_COUNT, TABLE_SIZE,
           (double)BOOKING_COUNT / TABLE_SIZE,
           100.0 * BOOKING_COUNT / TABLE_SIZE);
    return 0;
}
