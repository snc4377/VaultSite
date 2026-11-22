Note title: Untitled

![[Pasted image 20260401163510.png]]
As we see in the image, the SSH key is encrypted.

We use ssh2john to extract the hashes and then pass those hashes to john or hashcat.
![[Pasted image 20260401163620.png]]
![[Pasted image 20260401163648.png]]
And now we would have the passphrase for the encrypted SSH key.
![[Pasted image 20260401163725.png]]

