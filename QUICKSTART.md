# Quick Start: Production Deployment

This guide helps you deploy the LLM FAQ API to AWS with full CI/CD pipeline in under 30 minutes.

## Prerequisites Checklist

- [ ] AWS Account with appropriate permissions
- [ ] GitHub account and repository access
- [ ] Local machine with required tools

## Step 1: Install Required Tools

### macOS (using Homebrew)
```bash
brew install awscli terraform kubectl
```

### Ubuntu/Debian
```bash
# AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip && sudo ./aws/install

# Terraform
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install terraform

# kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```

## Step 2: Configure AWS

```bash
# Configure AWS credentials
aws configure
# Enter your AWS Access Key ID, Secret Access Key, and region (us-east-1)

# Verify configuration
aws sts get-caller-identity
```

## Step 3: Prepare Infrastructure

```bash
# Create S3 bucket for Terraform state
aws s3 mb s3://llm-faq-terraform-state-$(date +%s) --region us-east-1

# Note the bucket name and update terraform/main.tf
```

## Step 4: Fork and Clone Repository

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/llm-faq-api.git
cd llm-faq-api
```

## Step 5: Configure GitHub Secrets

Go to your GitHub repository → Settings → Secrets and variables → Actions

Add these secrets:
- `AWS_ACCESS_KEY_ID`: Your AWS access key
- `AWS_SECRET_ACCESS_KEY`: Your AWS secret key

## Step 6: Deploy Infrastructure

### Option A: Automated Deployment
```bash
# Deploy everything in one command
./deploy.sh
```

### Option B: Manual Step-by-step
```bash
# Deploy infrastructure only
./deploy.sh infrastructure-only

# Wait for infrastructure to be ready, then deploy application
./deploy.sh application-only
```

## Step 7: Verify Deployment

```bash
# Check cluster status
kubectl get nodes

# Check application status
kubectl get pods -n production
kubectl get services -n production

# Get application URL
kubectl get ingress -n production
```

## Step 8: Set Up CI/CD

Once infrastructure is deployed, any push to:
- `main` branch → deploys to production
- `develop` branch → deploys to staging

## Quick Commands

```bash
# View application logs
kubectl logs -f deployment/llm-faq-api -n production

# Scale application
kubectl scale deployment llm-faq-api --replicas=5 -n production

# Check auto-scaling status
kubectl get hpa -n production

# Update application (after code changes)
git push origin main  # This triggers CI/CD pipeline

# Check deployment status
kubectl rollout status deployment/llm-faq-api -n production
```

## Cost Estimate

**Monthly AWS costs (us-east-1):**
- EKS Cluster: ~$73/month
- EC2 Instances (2x t3.medium): ~$60/month
- Load Balancer: ~$16/month
- ECR: ~$1/month
- **Total: ~$150/month**

*Costs may vary based on usage and region*

## Cleanup

To destroy all resources:

```bash
# Delete Kubernetes resources
kubectl delete namespace production staging

# Destroy infrastructure
cd terraform
terraform destroy

# Delete ECR images manually if needed
aws ecr delete-repository --repository-name llm-faq-api --force
```

## Troubleshooting

### Common Issues

1. **AWS Permission Errors**
   ```bash
   # Verify your AWS permissions
   aws iam get-user
   aws eks list-clusters
   ```

2. **kubectl Connection Issues**
   ```bash
   # Update kubeconfig
   aws eks update-kubeconfig --region us-east-1 --name llm-faq-cluster
   ```

3. **Terraform State Issues**
   ```bash
   # Reset Terraform state if needed
   cd terraform
   terraform init -reconfigure
   ```

4. **Application Won't Start**
   ```bash
   # Check pod logs
   kubectl logs -f deployment/llm-faq-api -n production
   
   # Check events
   kubectl get events --sort-by=.metadata.creationTimestamp -n production
   ```

## Next Steps

- Configure custom domain and SSL certificate
- Set up monitoring and alerting
- Implement backup strategies
- Configure auto-scaling policies
- Set up development workflows

## Support

- 📚 Full documentation: [DEPLOYMENT.md](DEPLOYMENT.md)
- 🐛 Issues: [GitHub Issues](https://github.com/parthoece/llm-faq-api/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/parthoece/llm-faq-api/discussions)

---

**Estimated setup time: 20-30 minutes**  
**Difficulty level: Intermediate**
