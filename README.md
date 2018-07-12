# CNAPPS

[![License Apache 2][badge-license]](LICENSE)

## Description

Cloud Native Applications in differents languages:

* [ ] Python
* [ ] Go

Features :

* Metrics
* Tracing
* Logging
* Versioning
* Health
* Stateless

## Development

### Minikube

Create a new cluster (will create a virtual machine named *cnapps*) using
Minikube:

    $ ./scripts/minikube.sh

Check cluster :

    $ KUBECONFIG=./deploy/minikube-kube-config kubectl version

Check the *cnapps* namespace:

    $ KUBECONFIG=./deploy/minikube-kube-config kubectl get namespaces

You could use minikube command with profile *cnapps* :

    $ KUBECONFIG=./deploy/minikube-kube-config minikube dashboard -p cnapps

### Cockroachdb

Deploy CockroachDB into the Kubernetes minikube cluster:

    $ ./scripts/kubernetes.sh minikube local create latest

Configure your `/etc/hosts`:

    $ echo $(KUBECONFIG=./deploy/minikube-kube-config minikube ip) cockroach.cnapps.minikube | sudo tee -a /etc/hosts

### Applications

* [python-flask/README.md] Flask

## License

See [LICENSE](LICENSE) for the complete license.

## Changelog

A changelog is available [here](ChangeLog.md).

## Contact

Nicolas Lamirault <nicolas.lamirault@gmail.com>



[badge-license]: https://img.shields.io/badge/license-Apache2-green.svg?style=flat
