description = "ATM fraud detection with Common Kafka Streams"
plugins {
    java
    id("io.freefair.lombok") version "5.1.0"
    id("com.google.cloud.tools.jib") version "1.2.0"
    id("com.commercehub.gradle.plugin.avro") version "0.19.1"
}

group = "com.bakdata.kafka"

tasks.withType<Test> {
    maxParallelForks = 4
    useJUnitPlatform()
}

repositories {
    mavenCentral()
    maven(url = "http://packages.confluent.io/maven/")
}


configure<JavaPluginConvention> {
    sourceCompatibility = JavaVersion.VERSION_11
    targetCompatibility = JavaVersion.VERSION_11
}

dependencies {
    implementation(group = "com.bakdata.seq2", name = "seq2", version = "1.0.0")
    val confluentVersion: String by project
    implementation(group = "io.confluent", name = "kafka-streams-avro-serde", version = confluentVersion)
    implementation(group = "com.bakdata.common-kafka-streams", name = "common-kafka-streams", version = "1.5.3")
    implementation(group = "com.bakdata.kafka", name = "error-handling", version = "1.0.0")
    implementation(group = "org.elasticsearch", name = "elasticsearch", version = "7.10.0")
    implementation(group = "org.slf4j", name = "slf4j-log4j12", version = "1.7.26")
    implementation(group = "org.json", name = "json", version = "20201115")

    val junitVersion: String by project
    testImplementation(group = "org.junit.jupiter", name = "junit-jupiter-api", version = junitVersion)
    testImplementation(group = "org.junit.jupiter", name = "junit-jupiter-params", version = junitVersion)
    testRuntimeOnly(group = "org.junit.jupiter", name = "junit-jupiter-engine", version = junitVersion)
    testImplementation(group = "org.assertj", name = "assertj-core", version = "3.13.2")
    testImplementation(group = "log4j", name = "log4j", version = "1.2.17")
    testImplementation(group = "com.bakdata.fluent-kafka-streams-tests", name = "fluent-kafka-streams-tests-junit5", version = "2.2.0")
}
