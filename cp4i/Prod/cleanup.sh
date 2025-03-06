oc delete secret repapp01-keystore -n mq-apac
oc delete secret repapp02-keystore -n mq-apac
oc delete secret aceapp01-keystore -n mq-apac
oc delete secret mftapp01-keystore -n mq-apac
oc delete secret crdapp01-keystore -n mq-apac

oc delete secret mq-truststore -n mq-apac

oc delete -n mq-apac -f repapp01-default-config.yaml
oc delete -n mq-apac -f repapp02-default-config.yaml
oc delete -n mq-apac -f aceapp01-default-config.yaml
oc delete -n mq-apac -f mftapp01-default-config.yaml
oc delete -n mq-apac -f crdapp01-default-config.yaml

oc delete -n mq-apac -f mq-restapi.yaml

oc delete -n mq-apac -f repapp01-admin-route.yaml
oc delete -n mq-apac -f repapp02-admin-route.yaml
oc delete -n mq-apac -f aceapp01-admin-route.yaml
oc delete -n mq-apac -f mftapp01-admin-route.yaml
oc delete -n mq-apac -f crdapp01-admin-route.yaml

oc delete -n mq-apac -f pod-repapp01.yaml
oc delete -n mq-apac -f pod-repapp02.yaml
oc delete -n mq-apac -f pod-aceapp01.yaml
oc delete -n mq-apac -f pod-mftapp01.yaml
oc delete -n mq-apac -f pod-crdapp01.yaml

oc delete -n mq-apac pvc --all
