# tracing.py
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

def setup_tracer(service_name: str):
    resource = Resource.create({"service.name": service_name})
    provider = TracerProvider(resource=resource)

    processor = BatchSpanProcessor(
        OTLPSpanExporter(endpoint="http://jaeger:4317", insecure=True)
    )
    provider.add_span_processor(processor)

    trace.set_tracer_provider(provider)
    return trace.get_tracer(service_name)
