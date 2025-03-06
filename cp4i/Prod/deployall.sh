oc create secret tls repapp01-keystore -n mq-apac --key="repapp01.key" --cert="repapp01.crt"
oc create secret tls repapp02-keystore -n mq-apac --key="repapp02.key" --cert="repapp02.crt"
oc create secret tls aceapp01-keystore -n mq-apac --key="aceapp01.key" --cert="aceapp01.crt"
oc create secret tls mftapp01-keystore -n mq-apac --key="mftapp01.key" --cert="mftapp01.crt"
oc create secret tls crdapp01-keystore -n mq-apac --key="crdapp01.key" --cert="crdapp01.crt"

oc create secret generic mq-truststore -n mq-apac --from-file=mqexpo.crt=mqexpo.crt

oc create -n mq-apac -f repapp01-default-config.yaml
oc create -n mq-apac -f repapp02-default-config.yaml
oc create -n mq-apac -f aceapp01-default-config.yaml
oc create -n mq-apac -f mftapp01-default-config.yaml
oc create -n mq-apac -f crdapp01-default-config.yaml

oc create -n mq-apac -f mq-restapi.yaml

oc create -n mq-apac -f repapp01-admin-route.yaml
oc create -n mq-apac -f repapp02-admin-route.yaml
oc create -n mq-apac -f aceapp01-admin-route.yaml
oc create -n mq-apac -f mftapp01-admin-route.yaml
oc create -n mq-apac -f crdapp01-admin-route.yaml

oc create -n mq-apac -f pod-repapp01.yaml
oc create -n mq-apac -f pod-repapp02.yaml
oc create -n mq-apac -f pod-aceapp01.yaml
oc create -n mq-apac -f pod-mftapp01.yaml
oc create -n mq-apac -f pod-crdapp01.yaml
