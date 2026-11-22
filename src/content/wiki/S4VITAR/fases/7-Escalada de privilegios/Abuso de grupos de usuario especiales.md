In the context of Linux, **groups** are used to **organize** users and **assign** **permissions** to access system resources. Users can belong to one or multiple groups, and groups can have different permission levels to access system resources.

There are special groups in Linux, such as ‘**lxd**’ or ‘**docker**’, which are used to allow users to run containers securely and efficiently. However, if a malicious user gains access to one of these groups, they could exploit it to obtain elevated privileges on the system.

For example, if a user has access to the ‘**docker**’ group, they could use the Docker tool to deploy new containers on the system. During the deployment process, the user could exploit **mounts** to make certain inaccessible resources on the host machine available inside the container. By gaining access to the container as the ‘**root**’ user, the malicious user could infer or manipulate the contents of these resources from within the container.

To mitigate the risk of abuse of special user groups, it is important to carefully restrict access to these groups and ensure they are only assigned to trusted users who genuinely need access.


If we run `id`, we can see that we are part of the `sudo` group with the current user, which allows us—if we enter our password—to execute commands as if we were root.  
![[Pasted image 20260216164206.png]]

Another example would be the `docker` group, which would allow us to list Docker images, containers, and deploy new machines.  
![[Pasted image 20260216164402.png]]

What's interesting about this group? For example, let's imagine we don't know the current user's password but see they are in this group. We could try to deploy a container with the command `-v /:/mnt/root`, which would take the entire root of the host machine and copy it entirely into the container. Since we are root in the container, we could, for example, view `/etc/passwd`.  
![[Pasted image 20260216164716.png]]  
![[Pasted image 20260216164730.png]]  
![[Pasted image 20260216164745.png]]  
![[Pasted image 20260216164751.png]]

Even more interesting is that the mount connects the directory we specify with a directory in the container (in this case, `/mnt`). So, if we edit something in the container, it will immediately reflect in the host's path.

Let’s add SUID permissions to `bash` in the container’s `/bin` path, and we’ll see that it has been edited outside the container, allowing us to get an interactive TTY as root.  
![[Pasted image 20260216165254.png]]

Other groups could be `adm` or `lxd`.

With the **ADM** group, we could read system logs.  
![[Pasted image 20260216165404.png]]  
![[Pasted image 20260216165431.png]]  
![[Pasted image 20260216165445.png]]

**LXD Group**  

LXD is very similar to Docker, and what we can do with it is quite similar to what we did with Docker.  
![[Pasted image 20260216165617.png]]

If we search for LXD in Searchsploit, we’ll find a script to automate privilege escalation.  
![[Pasted image 20260216165715.png]]  
![[Pasted image 20260216165726.png]]  
![[Pasted image 20260216165733.png]]  
We would just need to follow the script, which tells us step by step what to do if we read it.

But what it tells us is that on our attacking machine, with Alpine and the URL provided, we should mount the container, and this script will create a compressed file with the Alpine image.

Now we’ll get a couple of files as output, which we need to transfer to the victim machine.  
![[Pasted image 20260216170222.png]]

And with the following command, we would achieve privilege escalation:  
![[Pasted image 20260216170327.png]]  
Now we would go to the `/mnt` directory, where the script made the mount, and we could modify and edit files.  
![[Pasted image 20260216170500.png]]

