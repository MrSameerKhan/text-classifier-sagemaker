pipeline {
  agent any

  environment {
    AWS_REGION = "ap-south-1"
    ACCOUNT_ID = "570617927874"  // ← your AWS account ID
    ECR_REPO   = "${ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/text-classifier"
    IMAGE_TAG  = "latest"
    AWS_CREDS  = credentials('aws-creds')
  }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Build & Push to ECR') {
      steps {
        sh '''
          aws ecr describe-repositories --repository-names text-classifier || \
            aws ecr create-repository --repository-name text-classifier

          echo $AWS_CREDS_PSW | docker login -u AWS --password-stdin ${ECR_REPO}
          docker build -t ${ECR_REPO}:${IMAGE_TAG} .
          docker push ${ECR_REPO}:${IMAGE_TAG}
        '''
      }
    }

    stage('Deploy to SageMaker') {
      steps {
        sh '''
          # Create or update the SageMaker model
          aws sagemaker create-model \
            --model-name text-classifier-model \
            --primary-container Image=${ECR_REPO}:${IMAGE_TAG} \
            --execution-role-arn arn:aws:iam::${ACCOUNT_ID}:role/SageMakerExecutionRole \
            || echo "Model exists"

          # Create or update the endpoint config
          aws sagemaker create-endpoint-config \
            --endpoint-config-name text-classifier-config \
            --production-variants \
              '[{"VariantName":"AllTraffic","ModelName":"text-classifier-model","InitialInstanceCount":1,"InstanceType":"ml.t2.medium"}]' \
            || echo "Config exists"

          # Create or update the endpoint
          aws sagemaker describe-endpoint --endpoint-name text-classifier-endpoint && \
            aws sagemaker update-endpoint \
              --endpoint-name text-classifier-endpoint \
              --endpoint-config-name text-classifier-config \
            || \
            aws sagemaker create-endpoint \
              --endpoint-name text-classifier-endpoint \
              --endpoint-config-name text-classifier-config
        '''
      }
    }
  }

  post {
    success { echo "✅ Deployment to SageMaker succeeded!" }
    failure { echo "❌ Deployment failed—check the logs." }
  }
}
