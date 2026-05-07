# Operations Runbook — Restore Monitoring Services

## Goal

Restore failed monitoring/packet-processing services and return to normal data freshness.

## Preconditions

- Access to Kubernetes cluster + namespaces
- Access to Kafka broker metrics and dashboards
- Runbook owner and escalation contacts available

## Recovery steps

### 1) Validate current state

```bash
kubectl get pods -n <ns>
kubectl top pods -n <ns>
```

### 2) Restart Kafka consumers safely

```bash
kubectl rollout restart deploy/<consumer-deploy> -n <ns>
kubectl rollout status deploy/<consumer-deploy> -n <ns>
```

### 3) Scale deployments (if lag growing)

```bash
kubectl scale deploy/<consumer-deploy> --replicas=<n> -n <ns>
```

### 4) Validate offsets and progress

- Confirm consumer group lag is decreasing
- Confirm commits are happening
- Confirm processing throughput is back to expected

### 5) Check broker health

- Disk usage
- Under-replicated partitions
- Broker restarts / network issues

### 6) Validate monitoring exporters

- Prometheus targets “up”
- Dashboards are receiving fresh data

## Post-recovery validation

- Consumer lag below threshold for sustained window (e.g., 15 minutes)
- No crash loops
- Error rates normal
- Data freshness restored

## Rollback / safety notes

- Prefer rollback if a new deployment introduced performance regression.
- Coordinate producer throttling only if approved and documented.

