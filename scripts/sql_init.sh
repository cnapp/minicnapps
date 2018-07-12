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

if [ $# -ne 2 ]; then
	echo "Usage: <cluster> <env>"
	exit 1
fi
cluster=$1
env=$2

kube_context ${cluster} ${env}

echo -e "${INFO_COLOR}Find CockroachDB pod${NO_COLOR}"
pods=$(kubectl --kubeconfig=${kubeconfig} get pods ${namespace} -l app=cockroachdb -o 'jsonpath={.items[*].metadata.name}')
if [ -z "${pods}" ]; then
	echo -e "${ERROR_COLOR}No pod${NO_COLOR}"
	exit
fi
pod=$(echo ${pods}| awk -F" " '{print $1}')
echo -e "Use pod: ${pod}"

echo -e "${INFO_COLOR}Create database for Cnapps${NO_COLOR}"
kubectl --kubeconfig=${kubeconfig} exec ${pod} ${namespace} -it -- /cockroach/cockroach sql --insecure -e "CREATE DATABASE IF NOT EXISTS cnapps"

echo -e "${INFO_COLOR}Create user for Cnapps${NO_COLOR}"
kubectl --kubeconfig=${kubeconfig} exec ${pod} ${namespace} -it -- /cockroach/cockroach sql --insecure -e "CREATE USER cnapps"
kubectl --kubeconfig=${kubeconfig} exec ${pod} ${namespace} -it -- /cockroach/cockroach sql --insecure -e "GRANT ALL ON DATABASE cnapps TO cnapps"
