kubectl apply -f statefulset-defintion.yaml

ksm@kubesinglemaster:~$ kubectl get pods
NAME                  READY   STATUS    RESTARTS   AGE
nginx-statefulset-0   1/1     Running   0          3m54s
nginx-statefulset-1   1/1     Running   0          3m51s
nginx-statefulset-2   1/1     Running   0          3m48s


kubectl scale statefulset nginx-statefulset --replicas=5

ksm@kubesinglemaster:~$ kubectl get pods
NAME                  READY   STATUS    RESTARTS   AGE
nginx-statefulset-0   1/1     Running   0          3m54s
nginx-statefulset-1   1/1     Running   0          3m51s
nginx-statefulset-2   1/1     Running   0          3m48s
nginx-statefulset-3   1/1     Running   0          2m39s
nginx-statefulset-4   1/1     Running   0          2m36s

Pods are created, scaled and deleted in a specific, ordered sequence.
