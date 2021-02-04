from kubernetes.client import V1beta1CronJob


class Extractor:
    sources = None
    sinks = None

    def on_streaming_app_env_parsing(self, env, streaming_app_name: str):
        pass

    def on_connector_config_parsing(self, config, connector_name: str):
        pass

    def on_cron_job_parsing(self, cron_job: V1beta1CronJob):
        pass
