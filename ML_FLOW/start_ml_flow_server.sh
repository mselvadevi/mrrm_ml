export MLFLOW_TRACKING_SERVER_CERT_PATH="/etc/nginx/ssl/aifi-preludesys/preludesys-com-chain.pem"
export MLFLOW_TRACKING_SERVER_CERT_PATH="/etc/nginx/ssl/aifi-preludesys/preludesys-com.pem"
#export MLFLOW_TRACKING_INSECURE_TLS=false
mlflow server --backend-store-uri sqlite:///mykpodb.sqlite --host 0.0.0.0 --port 8886
