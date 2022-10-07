package com.bakdata.kafka;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.List;
import org.junit.jupiter.api.Test;

class AccountProducerTest {
    @Test
    void shouldLoadJSON() {
        final String filename = "test_accounts.json";
        final List<Account> loadedAccounts = AccountProducer.loadJSON(filename);
        final String regex = "^a([0-9]{1,3})";
        assertThat(loadedAccounts).hasSize(5);
        assertThat(loadedAccounts).allSatisfy(account -> assertThat(account.getAccountId()).matches(regex));
    }
}
