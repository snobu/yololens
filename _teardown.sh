echo "[TEARDOWN]\nCurrent Kube context: `kubectl config current-context`\n"
az vm deallocate -n 'aks-nodepool1-41528601-0' -g 'MC_YOLOLENS-CLUSTER_YOLOLENS-CLUSTER_WESTEUROPE' -o table
sleep 30
az aks scale -n 'yololens-cluster' -g 'yololens-cluster' -c 1 --no-wait -o table
echo '--- TEARDOWN COMPLETE. ---'