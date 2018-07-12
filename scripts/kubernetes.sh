#!/usr/bin/env bash

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

# CLUSTER_CONFIG="./deploy/k8s-kube-config"
# MINIKUBE_CONFIG="./deploy/minikube-kube-config"
# kubeconfig=""

# clusters="minikube"
# environments="local"

# docker_namespace="cnapps"
app="cnapps-"

url=""

# Minikube cluster
minikube_url="minikube"

# namespace=""


function usage {
    echo -e "${OK_COLOR}Usage${NO_COLOR} : $0 <cluster> <env> <action> <application> <docker image version>"
    echo -e "${INFO_COLOR}Clusters${NO_COLOR} : ${clusters}"
    echo -e "${INFO_COLOR}Environments${NO_COLOR} : ${environments}"
    echo -e "${INFO_COLOR}Action${NO_COLOR} : create, destroy"
}


# function kube_context {
#     if  [ ! -x "$(command -v kubectl)" ]; then
#         kubectl_install
#     fi
#     echo -e "${OK_COLOR}Cluster: $1"
#     echo -e "${OK_COLOR}Environment: $2"
#     if [ "local" = "$2" ]; then
#         local context="cnapps"
#         namespace="-n cnapps"
#         echo -e "${OK_COLOR}Namespace: ${namespace}"
#     else
#         local context="${1}-cnapps-$2"
#     fi
#     kube_config ${env}
#     echo -e "${OK_COLOR}Switch to Kubernetes context: ${context}${NO_COLOR}" >&2
#     kubectl --kubeconfig=${kubeconfig} config use-context ${context} >&2 || exit 1
# }


# function kube_config {
#     env=$1
#     case ${env} in
#         local)
#             kubeconfig=${MINIKUBE_CONFIG}
#             ;;
#         stg|dev|itg|prp|prod)
#             kubeconfig=${CLUSTER_CONFIG}
#             ;;
#         *)
#             echo -e "${ERROR_COLOR}Invalid environment: ${env}${NO_COLOR}"
#             exit 1
#     esac
# }


function kube_replace {
    app=$1
    image_tag=$2
    build_number=$3
    dir=$4
    echo -e "${OK_COLOR}Generate Kubernetes files for: ${dir}${NO_COLOR}"
    echo -e "Environment: ${env}"
    echo -e "Namespace: ${ns}"
    echo -e "App: ${app}"
    echo -e "Docker ${image_name}:${image_tag}"
    echo -e "Build: ${build_number}"
    rm -fr ${dir} && mkdir -p ${dir} && cp -r deploy/${app}/* ${dir}
    # find ${dir} -name "*.yaml" | xargs sed -i "s/__KUBE_NAMESPACE__/${ns}/g"
    find ${dir} -name "*.yaml" | xargs sed -i "s/__KUBE_APP__/${app}/g"
    find ${dir} -name "*.yaml" | xargs sed -i "s/__KUBE_COMMIT_ID__/${build_number}/g"
    if [ "local" = "${env}" ]; then
        find ${dir} -name "*.yaml" | xargs sed -i "s#__CI_REGISTRY_IMAGE__#cnappsdb#g"
        find ${dir} -name "*.yaml" | xargs sed -i "s#__CI_REGISTRY_TAG__#${image_tag}#g"
        find ${dir} -name "*.yaml" | xargs sed -i "s#__KUBE_IMAGE_POLICY__#Never#g"
        find ${dir} -name "*.yaml" | xargs sed -i "s#__KUBE_NAME__#minikube#g"
    else
        find ${dir} -name "*.yaml" | xargs sed -i "s#__CI_REGISTRY_IMAGE__#${private_registry}/${image_name}#g"
        find ${dir} -name "*.yaml" | xargs sed -i "s#__CI_REGISTRY_TAG__#${image_tag}#g"
        find ${dir} -name "*.yaml" | xargs sed -i "s#__KUBE_IMAGE_POLICY__#Always#g"
        find ${dir} -name "*.yaml" | xargs sed -i "s#__KUBE_NAME__#cloud#g"
    fi
}


function kube_directory {
    action=$1
    directory=$2
    if [ -d "${directory}" ]; then
        if [ -n "$(ls -A ${directory})" ]; then
            kubectl --kubeconfig=${kubeconfig} ${action} -f "${directory}" ${namespace}
        fi
    else
        echo -e "${INFO_COLOR}Skip ${directory}. Does not exists${NO_COLOR}"
    fi
}


function kube_files {
    action=$1
    directory=$2
    env=$3
    for file in $(ls ${directory}/*-${env}.yaml 2>/dev/null); do
        kubectl --kubeconfig=${kubeconfig} ${action} -f "${file}" ${namespace}
    done
}


function kube_deploy {
    dir=$1
    echo -e "${OK_COLOR}Current context: $(kubectl --kubeconfig=${kubeconfig} config current-context)${NO_COLOR}"
    kube_directory "apply" "${dir}/commons"
    kube_directory "apply" "${dir}/${cluster}/commons"
    kube_files "apply" "${dir}/${cluster}" ${env}
}


function kube_undeploy {
    dir=$1
    echo -e "${OK_COLOR}Current context: ${context}${NO_COLOR}"
    kube_directory "delete" "${dir}/commons"
    kube_directory "delete" "${dir}/${cluster}/commons"
    kube_files "delete" "${dir}/${cluster}" ${env}
}

if [ $# -eq 0 ]; then
    usage
    exit 0
fi
if [ $# -ne 5 ]; then
    usage
    exit 1
fi


cluster=$1
env=$2
action=$3
app=$4
image_tag=$5
build_number=$(date +%Y%m%d%H%M%S)


case ${cluster} in
    minikube)
        url=${minikube_url}
        ;;
    *)
        echo -e "${ERROR_COLOR}Invalid cluster: ${env}${NO_COLOR}"
        usage
        exit 1
        ;;
esac


case ${action} in
    create)
        kube_context ${cluster} ${env}
        dir="/tmp/${app}"
        kube_replace ${app} ${image_tag} ${build_number} ${dir}
        kube_deploy ${dir}
        ;;
    destroy)
        kube_context ${cluster} ${env}
        dir="/tmp/${app}"
        kube_replace ${app} ${image_tag} ${build_number} ${dir}
        kube_undeploy ${dir}
        ;;
    *)
        echo -e "${ERROR_COLOR}Invalid action: [${action}]${NO_COLOR}"
	    echo -e "Valid actions: create, destroy"
        exit 1
esac
