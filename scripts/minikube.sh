#!/bin/bash

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

SCRIPT=$(readlink -f "$0")
# echo $SCRIPT
SCRIPTPATH=$(dirname "$SCRIPT")
# echo $SCRIPTPATH

. ${SCRIPTPATH}/commons.sh

driver=${1:-virtualbox}
KUBECONFIG_FILE=${2:-"./deploy/minikube-kube-config"}
memory=${3:-3072}

PROFILE="cnapps"

MINIKUBE_URI="https://storage.googleapis.com/minikube"
KUBE_URI="https://storage.googleapis.com/kubernetes-release"

# if [ ! -x "$(command -v minikube)" ]; then
#   echo "Download minikube"
#   curl -Lo minikube ${MINIKUBE_URI}/releases/latest/minikube-linux-amd64 \
#     && chmod +x minikube
#   export PATH=${PATH}:.
# fi
minikube_install

# if [ ! -x "$(command -v kubectl)" ]; then
#   echo "Download kubectl"
#   curl -Lo kubectl ${KUBE_URI}/release/$(curl -s ${KUBE_URI}/release/stable.txt)/bin/linux/amd64/kubectl \
#     && chmod +x kubectl
#   export PATH=${PATH}:.
# fi
kubectl_install

export MINIKUBE_WANTUPDATENOTIFICATION=false
export MINIKUBE_WANTREPORTERRORPROMPT=false
export CHANGE_MINIKUBE_NONE_USER=true

export MINIKUBE_HOME=$HOME


export KUBECONFIG=${KUBECONFIG_FILE}
minikube start --profile ${PROFILE} \
  --vm-driver=${driver} \
  --memory ${memory} \
  --logtostderr --loglevel 0 \
  --bootstrapper localkube \
  --docker-env HTTP_PROXY=${HTTP_PROXY} \
	--docker-env HTTPS_PROXY=${HTTPS_PROXY} \
	--docker-env NO_PROXY=192.168.99.0/24 \
  --extra-config=controller-manager.ClusterSigningCertFile="/var/lib/localkube/certs/ca.crt" \
  --extra-config=controller-manager.ClusterSigningKeyFile="/var/lib/localkube/certs/ca.key" \
  --extra-config=apiserver.Admission.PluginNames=NamespaceLifecycle,LimitRanger,ServiceAccount,PersistentVolumeLabel,DefaultStorageClass,DefaultTolerationSeconds,MutatingAdmissionWebhook,ValidatingAdmissionWebhook,ResourceQuota

# this for loop waits until kubectl can access the api server that Minikube has created
for i in {1..300}; do # timeout for 10 minutes
  kubectl get po &> /dev/null
  if [ $? -ne 1 ]; then
    echo "Kubernetes is ready"
    break
  fi
  echo "Wait for Kubernetes ..."
  sleep 2
done

echo -e "${OK_COLOR}Kubernetes configuration file: ${KUBECONFIG_FILE}${NO_COLOR}"
if [ ! -f ${KUBECONFIG} ]; then
  echo "Kubectl configuration file does not exist"
  exit 1
fi
cat ${KUBECONFIG_FILE}

echo -e "${OK_COLOR}Configure Minikube for cnapps${NO_COLOR}"
kubectl apply -f deploy/minikube/namespace.yaml

echo -e "${OK_COLOR}Minikube enable addons:${NO_COLOR}"
minikube addons enable ingress --profile ${PROFILE}

echo -e "${OK_COLOR}Minikube status:${NO_COLOR}"
minikube status --profile ${PROFILE}

echo -e "${OK_COLOR}Kubernetes info:${NO_COLOR}"
kubectl cluster-info
