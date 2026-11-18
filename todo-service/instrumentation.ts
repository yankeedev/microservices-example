import { NodeSDK } from '@opentelemetry/sdk-node'; 
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-grpc'; 
import { GrpcInstrumentation } from '@opentelemetry/instrumentation-grpc'; 
import { Resource } from '@opentelemetry/resources'; 
import { SemanticResourceAttributes } from '@opentelemetry/semantic-conventions'; 

const sdk = new NodeSDK({ 
  resource: new Resource({ [SemanticResourceAttributes.SERVICE_NAME]: 'todo-service' }), 
  traceExporter: new OTLPTraceExporter({ url: 'http://otel-collector:4317' }), 
  instrumentations: [new GrpcInstrumentation()], 
}); 
sdk.start();
