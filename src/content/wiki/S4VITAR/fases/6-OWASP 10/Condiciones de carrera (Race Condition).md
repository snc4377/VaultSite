**Race conditions** (also known as **Race Condition**) are a type of vulnerability that can occur in computer systems where two or more processes or execution threads compete for the same resources without a proper synchronization mechanism to control access to them.

This means that if two processes attempt to access the same shared resource simultaneously, the output of one or both processes may become unpredictable, or even result in unintended system behavior.

Attackers can exploit race conditions to carry out denial-of-service (**DoS**) attacks, overwrite critical data, gain unauthorized access to resources, or even execute malicious code on the system.

For example, suppose two processes attempt to access a file at the same time: one to read and the other to write. If there is no proper mechanism to synchronize access to the file, the reading process may retrieve incorrect data, or the writing process may overwrite important data that needs to be preserved.

The security impact of race conditions depends on the nature of the shared resource and the type of attack that can be performed. In general, race conditions can allow attackers to access critical resources, modify important data, or even gain full control of the system. Therefore, it is crucial for developers and system administrators to take measures to prevent and mitigate race conditions in their systems.

**LAB**
- **SKF-LABS Race Condition**: [https://github.com/blabla1337/skf-labs/tree/master/nodeJs/RaceCondition](https://github.com/blabla1337/skf-labs/tree/master/nodeJs/RaceCondition)
- **SKF-LABS Race Condition 2**: [https://github.com/blabla1337/skf-labs/tree/master/nodeJs/RaceCondition-file-write](https://github.com/blabla1337/skf-labs/tree/master/nodeJs/RaceCondition-file-write)

![[Pasted image 20260211204545.png]]
