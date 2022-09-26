package com.bakdata.kafka;

import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.channels.AsynchronousServerSocketChannel;
import java.nio.charset.StandardCharsets;
import java.util.Map;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

class AccountProducerTest {

    private String filename = "test_accounts.txt";
    AccountProducer accountProducer = new AccountProducer();

    @Test
    void shouldCreateAccount() {
        String account_id = "a2", first_name = "Robert", last_name = "Taylor", email = "ygarcia@example.net", phone =
                "241-531-3839x99962", address = "45679 Choi Brooks\nMillertown, VA 96527", country = "Togo";
        Account account =
                accountProducer.createAccount(account_id, first_name, last_name, email, phone, address, country);
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

        ClassLoader classLoader = getClass().getClassLoader();
        InputStream inputStream = classLoader.getResourceAsStream(filename);
        InputStreamReader streamReader = new InputStreamReader(inputStream, StandardCharsets.UTF_8);

        Map<Integer, String[]> loadedAccounts = accountProducer.loadCsvData(streamReader);
        Assertions.assertEquals(10, loadedAccounts.size(), "Verifying that all accounts was loaded");
        Assertions.assertEquals("a1", loadedAccounts.get(0)[0], "The AccountID name was loaded correctly");
        Assertions.assertEquals("Richard", loadedAccounts.get(0)[1], "The first name was loaded correctly");

    }
}
