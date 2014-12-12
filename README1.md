partitionpy
===========

A framework to detect errors like lost writes when network partitions occur in Distributed databases.
Distributed data systems can be exceptionally hard to get right. In this paper we present Par-titionPy (inspired by Jepsen[1]), a framework that can verify the correctness of distributed data systems in the presence of network parti-tions. PartitionPy can be used to test the cor-rectness of writes in key value stores, pub-sub systems, distributed message queues and dis-tributed databases. 

PartitionPy has a state machine can automati-cally detect lost writes and simulate the pres-ence of failures like network partitions, nodes being isolated from each other, asymmetric link failures, crashed nodes, delayed packets, dropped packets etc.  PartitionPy does this by a systematic exploration of all failure scenari-os and verifying that writes are consistent after all failures heal. In addition, PartitionPy can also be configured to simulate a particular se-quence of failures to detect errors in replica-tion protocols. We also envision PartitionPy as a tool that can be used by the systems com-munity in writing tests that verify writes in the presence of partitions. 

We show that Partitionpy actually works by using it to detect bugs in two popular open source projects that are widely used in the in-dustry - Redis, a distributed Key Value store and Apache Kafka, state-of-the art open source messaging system.
