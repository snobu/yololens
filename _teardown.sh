echo "[TEARDOWN]\nCurrent Kube context: `kubectl config current-context`\n"
kubectl delete pod yololens --now
az vm deallocate -n 'aks-nodepool1-41528601-0' -g 'MC_YOLOLENS-CLUSTER_YOLOLENS-CLUSTER_WESTEUROPE' --no-wait -o table
az aks scale -n 'yololens-cluster' -g 'yololens-cluster' -c 1 --no-wait -o table
echo '--- TEARDOWN COMPLETE. ---'