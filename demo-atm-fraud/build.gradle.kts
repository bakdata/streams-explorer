description = "ATM fraud detection with Common Kafka Streams"
plugins {
    java
    idea
    id("io.freefair.lombok") version "6.5.1"
    id("com.google.cloud.tools.jib") version "3.1.1"
    id("com.github.davidmc24.gradle.plugin.avro") version "1.2.0"
}

group = "com.bakdata.kafka"

tasks.withType<Test> {
    maxParallelForks = 1
    useJUnitPlatform()
}

repositories {
    mavenCentral()
    maven(url = "https://packages.confluent.io/maven/")
}


configure<JavaPluginConvention> {
    sourceCompatibility = JavaVersion.VERSION_11
    targetCompatibility = JavaVersion.VERSION_11
}

dependencies {
    implementation(group = "com.bakdata.seq2", name = "seq2", version = "1.0.0")
    val confluentVersion: String by project
    implementation(group = "io.confluent", name = "kafka-streams-avro-serde", version = confluentVersion)
    implementation(group = "com.bakdata.kafka", name = "streams-bootstrap", version = "2.3.0")
    implementation(group = "com.bakdata.kafka", name = "error-handling-avro", version = "1.3.0")
    implementation(group = "org.elasticsearch", name = "elasticsearch", version = "7.10.0")
    implementation(group = "org.slf4j", name = "slf4j-log4j12", version = "1.7.26")
    implementation(group = "org.json", name = "json", version = "20201115")

    val junitVersion: String by project
    testImplementation(group = "org.junit.jupiter", name = "junit-jupiter-api", version = junitVersion)
    testImplementation(group = "org.junit.jupiter", name = "junit-jupiter-params", version = junitVersion)
    testRuntimeOnly(group = "org.junit.jupiter", name = "junit-jupiter-engine", version = junitVersion)
    testImplementation(group = "org.assertj", name = "assertj-core", version = "3.23.1")
    testImplementation(group = "log4j", name = "log4j", version = "1.2.17")
    val kafkaVersion: String by project
    val fluentKafkaVersion = "2.7.0"
    testImplementation(
            group = "com.bakdata.fluent-kafka-streams-tests",
            name = "fluent-kafka-streams-tests-junit5",
            version = fluentKafkaVersion
    )
    testImplementation(group = "net.mguenther.kafka", name = "kafka-junit", version = kafkaVersion) {
        exclude(group = "org.slf4j", module = "slf4j-log4j12")
    }
    implementation(group = "com.opencsv", name = "opencsv", version = "5.2")
    testImplementation(
        group = "com.bakdata.fluent-kafka-streams-tests",
        name = "schema-registry-mock-junit5",
        version = fluentKafkaVersion
    )
    implementation(group = "info.picocli", name = "picocli", version = "4.6.1")

}
