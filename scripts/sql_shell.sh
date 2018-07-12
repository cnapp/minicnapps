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

if [ $# -ne 3 ]; then
	echo "Usage: <cluster> <env> <database>"
	exit 1
fi

cluster=$1
env=$2
db=$3

kube_context ${cluster} ${env}

echo -e "${OK_COLOR}Find CockroachDB pod${NO_COLOR}"
pods=$(kubectl --kubeconfig=${kubeconfig} get pods ${namespace} -l app=cockroachdb -o 'jsonpath={.items[*].metadata.name}')
if [ -z "${pods}" ]; then
    echo -e "${ERROR_COLOR}No pod found.${NO_COLOR}"
    exit 1
fi
pod=$(echo ${pods}| awk -F" " '{print $1}')
echo -e "Use pod: ${pod}"

echo -e "${OK_COLOR}Execute SQL shell${NO_COLOR}"
kubectl --kubeconfig=${kubeconfig} exec ${pod} ${namespace} -it -- /cockroach/cockroach sql --insecure -d ${db}
