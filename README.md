# AI Sentiment Analysis (Flask → Docker → EKS → CI/CD → Prometheus/Grafana)

## Features
- POST `/sentiment` with `{"text": "I am happy"}` → sentiment + score (-1..1)
- `/metrics` Prometheus exposition; `/health` for probes
- Auto-scale via HPA; HTTPS via ALB + ACM (Ingress)

## Quick Local Test
docker build -t sentiment-app:local app
docker run -d -p 5000:5000 sentiment-app:local
curl -s -X POST localhost:5000/sentiment -H "Content-Type: application/json" -d '{"text":"I am happy"}'

## EKS Deploy (manual)
aws eks update-kubeconfig --name <cluster> --region <region>
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/deployment.yaml -f k8s/service.yaml -f k8s/hpa.yaml -f k8s/networkpolicy.yaml -f k8s/podmonitor.yaml
# Optional Ingress with TLS via ACM (requires AWS LB Controller):
kubectl apply -f k8s/ingress.yaml

## Monitoring
- Helm install `kube-prometheus-stack` (Prometheus, Grafana, Alertmanager)
- Grafana service type: LoadBalancer; default admin/admin123
- Preloaded dashboard shows request counts and latency

## CI/CD
- GitHub Actions: test → build → push → deploy → monitoring
- Requires GitHub secrets: DOCKERHUB_USERNAME, DOCKERHUB_TOKEN, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

## Security
- TLS via AWS ALB + ACM
- NetworkPolicy limits traffic
- Liveness/Readiness probes
- Resource requests/limits

## Disaster Recovery
- Stateless (pods restart; HPA scales)
- If DB added: EBS/EFS + scheduled snapshots
- Recreate stack by rerunning pipeline

## Test after deploy
curl -s -X POST http://<svc-or-ingress-dns>/sentiment -H "Content-Type: application/json" -d '{"text":"I am happy"}'
