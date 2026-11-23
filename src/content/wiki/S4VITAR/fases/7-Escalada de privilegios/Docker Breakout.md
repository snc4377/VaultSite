---
title: "Docker Breakout"
category: ["S4VITAR", "fases", "7-Escalada de privilegios", "Docker Breakout"]
---

Note title: Untitled

In today's class, we will explore various techniques to abuse **Docker** with the goal of elevating our user privileges and escaping the container to the host machine. We will examine specific scenarios and discuss the security implications in each case.

The techniques covered in this class include:

- Using mounts in container deployments to access privileged system files on the host. We will analyze how an attacker can leverage mounts to manipulate host files and compromise system security.
- Deploying containers with process sharing (**--pid=host**) and privileged permissions (**--privileged**). We will see how to inject malicious shellcode into a running process as root, which could allow an attacker to take control of the system.
- Using **Portainer** to manage container deployment. We will discuss how, through the use of mounts, an attacker could gain access and manipulate privileged system files on the host and escape the container.
- Abusing the **Docker** **API** on port **2375** to create images, deploy containers, and inject privileged commands on the host machine. We will examine how an attacker can exploit the Docker API to compromise host security and achieve execution of elevated-privilege commands.






