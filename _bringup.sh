kubectl config use-context yololens-cluster
echo "[BRING UP]\nCurrent Kube context: `kubectl config current-context`\n"
az vm start -n 'aks-nodepool1-41528601-0' -g 'MC_YOLOLENS-CLUSTER_YOLOLENS-CLUSTER_WESTEUROPE' -o table
sleep 60
az aks scale -n 'yololens-cluster' -g 'yololens-cluster' -c 2 -o table
sleep 60
az vm deallocate -n 'aks-nodepool1-41528601-0' -g 'MC_YOLOLENS-CLUSTER_YOLOLENS-CLUSTER_WESTEUROPE' -o table
echo '--- BRING UP DONE. ---'
