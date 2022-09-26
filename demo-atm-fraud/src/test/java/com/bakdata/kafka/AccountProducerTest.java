package com.bakdata.kafka;

import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.Map;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

class AccountProducerTest {

    @Test
    void shouldCreateAccount() {
        final String account_id = "a2";
        final String first_name = "Robert";
        final String last_name = "Taylor";
        final String email = "ygarcia@example.net";
        final String phone = "241-531-3839x99962";
        final String address = "45679 Choi Brooks\nMillertown, VA 96527";
        final String country = "Togo";
        final Account account =
                AccountProducer.createAccount(account_id, first_name, last_name, email, phone, address, country);
        Assertions.assertEquals(account_id, account.getAccountId(), " Comparing accountIDs");
        Assertions.assertEquals(first_name, account.getFirstName(), "Comparing first names");
        Assertions.assertEquals(last_name, account.getLastName(), "Comparing last names");
        Assertions.assertEquals(email, account.getEmail(), "Comparing emails");
        Assertions.assertEquals(phone, account.getPhone(), "Comparing phones");
        Assertions.assertEquals(address, account.getAddress(), "Comparing addresses");
        Assertions.assertEquals(country, account.getCountry(), "Comparing countries");

    }

    @Test
    void shouldLoadCsvData() {

        final ClassLoader classLoader = this.getClass().getClassLoader();
        final String filename = "test_accounts.txt";
        final InputStream inputStream = classLoader.getResourceAsStream(filename);
        InputStreamReader streamReader = null;
        if (inputStream != null) {
            streamReader = new InputStreamReader(inputStream, StandardCharsets.UTF_8);
        }

        final Map<Integer, String[]> loadedAccounts = AccountProducer.loadCsvData(streamReader);
        Assertions.assertEquals(10, loadedAccounts.size(), "Verifying that all accounts was loaded");
        Assertions.assertEquals("a1", loadedAccounts.get(0)[0], "The AccountID name was loaded correctly");
        Assertions.assertEquals("Richard", loadedAccounts.get(0)[1], "The first name was loaded correctly");
    }
}
