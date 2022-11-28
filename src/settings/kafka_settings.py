import os
from autotech_sdk.kafka import ConfluentPublisherConfig


class KafkaTopic:
    GMAIL_NOTIFY = "gmail_notify"


CONFLUENT_KAFKA_PRODUCER_CONFIG = ConfluentPublisherConfig(
    bootstrap_servers=os.environ.get("BOOTSTRAP_SERVERS", "localhost:9092"),
    security_protocol=os.environ.get("SECURITY_PROTOCOL", "SASL_SSL"),
    sasl_mechanisms=os.environ.get("SASL_MECHANISMS", "PLAIN"),
    sasl_username=os.environ.get("SASL_USERNAME", ""),
    sasl_password=os.environ.get("SASL_PASSWORD", ""),
)
