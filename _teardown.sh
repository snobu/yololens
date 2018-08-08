echo "[TEARDOWN]\nCurrent Kube context: `kubectl config current-context`\n"
kubectl delete pod yololens --now
az aks scale -n 'yololens-cluster' -g 'yololens-cluster' -c 1 -o table
az vm deallocate -n 'aks-nodepool1-41528601-1' -g 'MC_YOLOLENS-CLUSTER_YOLOLENS-CLUSTER_WESTEUROPE' --no-wait -o table
echo '--- TEARDOWN COMPLETE. ---'
