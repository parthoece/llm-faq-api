#!/bin/bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
AWS_REGION=${AWS_REGION:-us-east-1}
ENVIRONMENT=${ENVIRONMENT:-production}
CLUSTER_NAME=${CLUSTER_NAME:-llm-faq-cluster}

echo -e "${GREEN}Starting deployment of LLM FAQ API infrastructure...${NC}"

# Check prerequisites
check_prerequisites() {
    echo -e "${YELLOW}Checking prerequisites...${NC}"
    
    if ! command -v terraform &> /dev/null; then
        echo -e "${RED}Terraform is not installed${NC}"
        exit 1
    fi
    
    if ! command -v aws &> /dev/null; then
        echo -e "${RED}AWS CLI is not installed${NC}"
        exit 1
    fi
    
    if ! command -v kubectl &> /dev/null; then
        echo -e "${RED}kubectl is not installed${NC}"
        exit 1
    fi
    
    # Check AWS credentials
    if ! aws sts get-caller-identity &> /dev/null; then
        echo -e "${RED}AWS credentials not configured${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}Prerequisites check passed${NC}"
}

# Deploy infrastructure with Terraform
deploy_infrastructure() {
    echo -e "${YELLOW}Deploying infrastructure with Terraform...${NC}"
    
    cd terraform
    
    # Initialize Terraform
    terraform init
    
    # Plan deployment
    terraform plan -var="aws_region=$AWS_REGION" -var="environment=$ENVIRONMENT" -var="cluster_name=$CLUSTER_NAME"
    
    # Apply deployment
    echo -e "${YELLOW}Applying Terraform configuration...${NC}"
    terraform apply -auto-approve -var="aws_region=$AWS_REGION" -var="environment=$ENVIRONMENT" -var="cluster_name=$CLUSTER_NAME"
    
    # Get outputs
    ECR_REPOSITORY_URL=$(terraform output -raw ecr_repository_url)
    CLUSTER_NAME=$(terraform output -raw cluster_name)
    
    echo -e "${GREEN}Infrastructure deployment completed${NC}"
    echo "ECR Repository: $ECR_REPOSITORY_URL"
    echo "EKS Cluster: $CLUSTER_NAME"
    
    cd ..
}

# Configure kubectl
configure_kubectl() {
    echo -e "${YELLOW}Configuring kubectl...${NC}"
    
    aws eks update-kubeconfig --region $AWS_REGION --name $CLUSTER_NAME
    
    # Verify connection
    if kubectl cluster-info &> /dev/null; then
        echo -e "${GREEN}kubectl configured successfully${NC}"
    else
        echo -e "${RED}Failed to configure kubectl${NC}"
        exit 1
    fi
}

# Build and push Docker image
build_and_push_image() {
    echo -e "${YELLOW}Building and pushing Docker image...${NC}"
    
    # Get ECR repository URL from Terraform output
    cd terraform
    ECR_REPOSITORY_URL=$(terraform output -raw ecr_repository_url)
    cd ..
    
    # Login to ECR
    aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REPOSITORY_URL
    
    # Build image
    docker build -f Dockerfile.prod -t llm-faq-api:latest .
    
    # Tag and push image
    docker tag llm-faq-api:latest $ECR_REPOSITORY_URL:latest
    docker tag llm-faq-api:latest $ECR_REPOSITORY_URL:$(git rev-parse --short HEAD)
    
    docker push $ECR_REPOSITORY_URL:latest
    docker push $ECR_REPOSITORY_URL:$(git rev-parse --short HEAD)
    
    echo -e "${GREEN}Docker image pushed successfully${NC}"
    echo "Image: $ECR_REPOSITORY_URL:$(git rev-parse --short HEAD)"
}

# Deploy to Kubernetes
deploy_to_kubernetes() {
    echo -e "${YELLOW}Deploying to Kubernetes...${NC}"
    
    # Get ECR repository URL and image tag
    cd terraform
    ECR_REPOSITORY_URL=$(terraform output -raw ecr_repository_url)
    cd ..
    
    IMAGE_TAG=$(git rev-parse --short HEAD)
    
    # Update deployment manifests
    if [ "$ENVIRONMENT" = "production" ]; then
        MANIFEST_DIR="k8s/production"
    else
        MANIFEST_DIR="k8s/staging"
    fi
    
    # Replace placeholders in deployment files
    sed -i.bak "s|{{ECR_REGISTRY}}/llm-faq-api:{{IMAGE_TAG}}|$ECR_REPOSITORY_URL:$IMAGE_TAG|g" $MANIFEST_DIR/deployment.yaml
    
    # Apply Kubernetes manifests
    kubectl apply -f $MANIFEST_DIR/
    
    # Wait for deployment to be ready
    kubectl rollout status deployment/llm-faq-api -n $ENVIRONMENT --timeout=600s
    
    # Restore original files
    mv $MANIFEST_DIR/deployment.yaml.bak $MANIFEST_DIR/deployment.yaml
    
    echo -e "${GREEN}Kubernetes deployment completed${NC}"
}

# Verify deployment
verify_deployment() {
    echo -e "${YELLOW}Verifying deployment...${NC}"
    
    # Check pod status
    kubectl get pods -n $ENVIRONMENT
    
    # Check service status
    kubectl get services -n $ENVIRONMENT
    
    # Get service URL
    if [ "$ENVIRONMENT" = "production" ]; then
        SERVICE_URL=$(kubectl get service llm-faq-api-service -n production -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
        if [ -n "$SERVICE_URL" ]; then
            echo -e "${GREEN}Service URL: http://$SERVICE_URL${NC}"
        fi
    fi
    
    echo -e "${GREEN}Deployment verification completed${NC}"
}

# Main execution
main() {
    echo -e "${GREEN}LLM FAQ API Deployment Script${NC}"
    echo "Environment: $ENVIRONMENT"
    echo "AWS Region: $AWS_REGION"
    echo "Cluster Name: $CLUSTER_NAME"
    echo ""
    
    check_prerequisites
    
    if [ "$1" = "infrastructure-only" ]; then
        deploy_infrastructure
        configure_kubectl
    elif [ "$1" = "application-only" ]; then
        configure_kubectl
        build_and_push_image
        deploy_to_kubernetes
        verify_deployment
    else
        deploy_infrastructure
        configure_kubectl
        build_and_push_image
        deploy_to_kubernetes
        verify_deployment
    fi
    
    echo -e "${GREEN}Deployment completed successfully!${NC}"
}

# Run main function with all arguments
main "$@"
