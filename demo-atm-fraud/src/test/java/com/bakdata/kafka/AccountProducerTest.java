package com.bakdata.kafka;

import static org.assertj.core.api.Assertions.assertThat;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.junit.jupiter.api.Test;

class AccountProducerTest {

    @Test
    void shouldCreateAccount() {
        final String accountId = "a2";
        final String firstName = "Robert";
        final String lastName = "Taylor";
        final String email = "ygarcia@example.net";
        final String phone = "241-531-3839x99962";
        final String address = "45679 Choi Brooks\nMillertown, VA 96527";
        final String country = "Togo";

        final JSONObject accountDetails = new JSONObject();
        accountDetails.put("account_id", accountId);
        accountDetails.put("first_name", firstName);
        accountDetails.put("last_name", lastName);
        accountDetails.put("email", email);
        accountDetails.put("phone", phone);
        accountDetails.put("address", address);
        accountDetails.put("country", country);
        final Account account = AccountProducer.parseAccount(accountDetails);

        assertThat(account.getAccountId()).isEqualTo(accountId);
        assertThat(account.getFirstName()).isEqualTo(firstName);
        assertThat(account.getLastName()).isEqualTo(lastName);
        assertThat(account.getEmail()).isEqualTo(email);
        assertThat(account.getPhone()).isEqualTo(phone);
        assertThat(account.getAddress()).isEqualTo(address);
        assertThat(account.getCountry()).isEqualTo(country);
    }

    @Test
    void shouldLoadJSON() {
        final String filename = "test_accounts.json";
        final JSONArray loadedAccounts = AccountProducer.loadJSON(filename);
        final String regex = "^a([0-9]{1,3})";

        assertThat(loadedAccounts).hasSize(5);
        for (final Object accountObj : loadedAccounts) {
            final JSONObject account = (JSONObject) accountObj;
            assertThat(account.get("account_id").toString()).matches(regex);
        }
    }
}
