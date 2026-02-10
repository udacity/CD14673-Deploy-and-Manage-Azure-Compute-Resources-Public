# Build the project
sam build

# Deploy the project
sam deploy --stack-name udshopping --resolve-s3 --capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND

# List the Outputs from the deployed stack and save to a file
sam list stack-outputs --stack-name udshopping --output json > ./state.json

# Read the API base URL and S3 bucket name from the stack outputs
bucket_name=$(./read_stack_outputs ./state.json WebsiteBucketName)
api_base_url=$(./read_stack_outputs ./state.json ApiBaseUrl)

# Edit frontend/url.js then sync to S3
cat > frontend/url.js <<EOF
window.shoppingCartAPIBaseURL = "${api_base_url}";
document.addEventListener("DOMContentLoaded", () => {
  const apiDocEl = document.getElementById("apiDoc");
  if (apiDocEl) {
    apiDocEl.innerHTML = "API: ${api_base_url}";
  }
});
EOF
aws s3 sync ./frontend s3://${bucket_name}

echo "Deployment Complete"
sam list stack-outputs --stack-name udshopping