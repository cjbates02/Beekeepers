#!/bin/bash
curl -L https://github.com/projectcalico/calico/releases/download/v3.28.2/calicoctl-darwin-amd64 -o kubectl-calico
cp ./kubectl-calico /usr/local/bin/ # mac os installation only