# Incident Response Playbook — Kafka Consumer Lag (Kubernetes)

## Symptoms

- Alerts: consumer lag threshold breached
- Packet processing delayed (e.g., 15+ minutes)
- Downstream dashboards stale
- Increased queue backlog
- Elevated CPU/memory on consumer pods

## Possible causes

- Consumer pods throttled (CPU limits), OOMKilled, or crash-looping
- Broker issues (disk full, partition leader changes, network)
- Topic partition imbalance / hot partitions
- Downstream dependency slow (DB/Elasticsearch), causing backpressure
- Bad deployment (new version slower or stuck)

## Investigation steps

### 1) Confirm the blast radius

- Which topics/consumer groups are lagging?
- Is lag growing or stable?
- Which services are impacted?

### 2) Check Kubernetes health

```bash
kubectl get pods -n <ns>
kubectl describe pod <pod> -n <ns>
kubectl top pods -n <ns>
kubectl logs <pod> -n <ns> --tail=200
```

### 3) Check consumer metrics/logs

- Throughput (messages/sec)
- Processing time per message
- Retry/error counts
- Commit failures / rebalances

### 4) Check Kafka broker health

- Broker CPU/mem/disk
- ISR status, under-replicated partitions
- Network errors

## Commands to execute (example set)

```bash
kubectl get deploy -n <ns>
kubectl rollout status deploy/<consumer-deploy> -n <ns>
kubectl scale deploy/<consumer-deploy> --replicas=5 -n <ns>
kubectl logs deploy/<consumer-deploy> -n <ns> --tail=200
```

## Mitigation & recovery actions

- Scale consumers horizontally (if partitions allow)
- Increase CPU/memory limits if throttling/OOM
- Roll back to last known good image if regression suspected
- Pause/slow producers if possible (traffic shaping)
- Investigate hot partitions and rebalance keys/partitions

## Rollback procedures

```bash
kubectl rollout undo deploy/<consumer-deploy> -n <ns>
kubectl rollout status deploy/<consumer-deploy> -n <ns>
```

## Escalation matrix (fill for your org)

- **On-call SRE**: first responder, mitigation owner
- **Data/Streaming team**: Kafka/topic configuration, broker escalation
- **Service owner**: consumer code, performance regressions
- **Infra**: cluster capacity / node issues

## SLA considerations

- Track “data freshness” SLO (e.g., < 5 minutes delay)
- Define breach thresholds for:
  - lag
  - time-to-mitigate
  - time-to-recover
- Communicate status updates at a fixed cadence (e.g., every 15 minutes)

