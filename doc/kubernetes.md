kubernetes
==========

## Cluster Administration ##

### preflight ###

Check logged in user

```bash
gcloud auth list
# ensure correct active user
# gcloud auth login
```

Check active project

```bash
gcloud config get-value project
# project should be cal-itp-data-infra
# gcloud config set project cal-itp-data-infra
```

Check compute region

```bash
gcloud config get-value compute/region
# region should be us-west1
# gcloud config set compute/region us-west1
```

### quick start ###

```bash
./kubernetes/gke/cluster-create.sh
# ...
export KUBECONFIG=$PWD/kubernetes/gke/kube/admin.yaml
kubectl cluster-info
```

### cluster lifecycle ###

Create the cluster by running `kubernetes/gke/cluster-create.sh`.

The cluster level configuration parameters are stored in
[`kubernetes/gke/config-cluster.sh`](../kubernetes/gke/config-cluster.sh).
Creating the cluster also requires configuring parameters for a node pool
named "default-pool" (unconfigurable name defined by GKE) in
[`kubernetes/gke/config-nodepool.sh`](../kubernetes/gke/config-nodepool.sh).
Any additional node pools configured in this file are also stood up at cluster
creation time.

Once the cluster is created, it can be managed by pointing the `KUBECONFIG`
environment variable to `kubernetes/gke/kube/admin.yaml`.

The cluster can be deleted by running `kubernetes/gke/cluster-delete.sh`.

### nodepool lifecycle ###

Certain features of node pools are immutable (e.g., machine type); to change
such parameters requires creating a new node pool with the desired new values,
migrating workloads off of the old node pool, and then deleting the old node pool.
The node pool lifecycle scripts help simplify this process.

#### create a new node pool ####

Configure a new node pool by adding its name to the `GKE_NODEPOOL_NAMES` array
in [`kubernetes/gke/config-nodepool.sh`](../kubernetes/gke/config-nodepool.sh).
For each nodepool property (`GKE_NODEPOOL_NODE_COUNT`, `GKE_NODEPOOL_NODE_LOCATIONS`, etc)
it is required to add an entry to the array which is mapped to the nodepool name.

Once the new nodepool is configured, it can be stood up by running `kubernetes/gke/nodepool-up.sh [nodepool-name]`,
or by simply running `kubernetes/gke/nodepool-up.sh`, which will stand up all configured node pools which do not yet
exist.

#### drain and delete an old node pool ####

Once a new nodepool has been created to replace an active node pool, the old node pool must be
removed from the `GKE_NODEPOOL_NAMES` array.

Once the old node pool is removed from the array, it can be drained and deleted by running `kubernetes/gke/nodepool-down.sh <nodepool-name>`.