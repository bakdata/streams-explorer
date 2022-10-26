from __future__ import annotations

from typing import TYPE_CHECKING

from kubernetes_asyncio.client import V1beta1CronJob

import streams_explorer.core.k8s_app as k8s
from streams_explorer.core.extractor.extractor import ProducerAppExtractor

if TYPE_CHECKING:
    from streams_explorer.core.k8s_app import K8sAppCronJob


class StreamsBootstrapProducer(ProducerAppExtractor):
    def on_cron_job_parsing(self, cron_job: V1beta1CronJob) -> K8sAppCronJob | None:
        producer = k8s.K8sAppCronJob(cron_job)
        if producer.is_streams_app:
            return producer
