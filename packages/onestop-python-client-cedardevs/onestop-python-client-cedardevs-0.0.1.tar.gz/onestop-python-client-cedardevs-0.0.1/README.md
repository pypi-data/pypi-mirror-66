#OneStop Clients

This python package provides an API to connect to OneStop's event stream (aka Inventory Manager). At this early stage there is only a single module for consuming messages from the kafka brokers that back OneStop. 

Our first example, [smeFunc.py](#examples/smeFunc.py), imports our onestop_client package, and passes to it the id, topic, and message handler function. Our library then handles the work to connect to kafka and deserialize the message.

The dockerfile in the example directory will create an image with the smeFunc.py python script built in.

Here is an example of how the script gets called-

`python onestop-consumer.py -b onestop-dev-cp-kafka -s http://onestop-dev-cp-schema-registry:8081 -t psi-registry-collection-parsed-changelog -g sme-test`

Here is how to run it in k8s so that it can actually connect to the kafka broker and schema registry-
`kubectl apply -f examples/pyconsumer-pod.yml`

At the moment, that pod will tail -f /dev/null to stay open so you can exec into the container with -
`kubectl exec -it pyconsumer bash`

And then there should be env vars available so you can run this -
`python ./smeFunc.py -b $KAFKA_BROKERS -s $SCHEMA_REGISTRY -t $TOPIC -g $GROUP_ID`

or adjust it as needed.
