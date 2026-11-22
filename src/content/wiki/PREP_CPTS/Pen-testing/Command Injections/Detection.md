The process of detecting basic OS Command Injection vulnerabilities is the same process for exploiting such vulnerabilities. We attempt to append our command through various injection methods. If the command output changes from the intended usual result, we have successfully exploited the vulnerability. This may not be true for more advanced command injection vulnerabilities because we may utilize various fuzzing methods or code reviews to identify potential command injection vulnerabilities. We may then gradually build our payload until we achieve command injection. 

---
## Command Injection Detection

When we visit the web application in the below exercise, we see a `Host Checker` utility that appears to ask us for an IP to check whether it is alive or not:![Image of a Host Checker interface with a text field labeled 'Enter an IP Address' containing '127.0.0.1' and a 'Check' button below.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/109/cmdinj_basic_exercise_1.jpg)

We can try entering the localhost IP `127.0.0.1` to check the functionality, and as expected, it returns the output of the `ping` command telling us that the localhost is indeed alive:![Host Checker interface with a text field for entering an IP address, '127.0.0.1' entered, a 'Check' button, and ping results displayed below.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/109/cmdinj_basic_exercise_2.jpg)

Although we do not have access to the source code of the web application, we can confidently guess that the IP we entered is going into a `ping` command since the output we receive suggests that. As the result shows a single packet transmitted in the ping command, the command used may be as follows:

`ping -c 1 OUR_INPUT`

If our input is not sanitized and escaped before it is used with the `ping` command, we may be able to inject another arbitrary command. So, let us try to see if the web application is vulnerable to OS command injection.

---

## Command Injection Methods

To inject an additional command to the intended one, we may use any of the following operators:

| **Injection Operator** | **Injection Character** | **URL-Encoded Character** | **Executed Command**                       |
| ---------------------- | ----------------------- | ------------------------- | ------------------------------------------ |
| Semicolon              | `;`                     | `%3b`                     | Both                                       |
| New Line               | `\n`                    | `%0a`                     | Both                                       |
| Background             | `&`                     | `%26`                     | Both (second output generally shown first) |
| Pipe                   | \|                      | `%7c`                     | Both (only second output is shown)         |
| AND                    | `&&`                    | `%26%26`                  | Both (only if first succeeds)              |
| OR                     | \| \|                   | `%7c%7c`                  | Second (only if first fails)               |
| Sub-Shell              | ` `` `                  | `%60%60`                  | Both **(Linux-only)**                      |
| Sub-Shell              | `$()`                   | `%24%28%29`               | Both **(Linux-only)**                      |

We can use any of these operators to inject another command so `both` or `either` of the commands get executed. `We would write our expected input (e.g., an IP), then use any of the above operators, and then write our new command.`

In general, for basic command injection, all of these operators can be used for command injections `regardless of the web application language, framework, or back-end server`. So, if we are injecting in a `PHP` web application running on a `Linux` server, or a `.Net` web application running on a `Windows` back-end server, or a `NodeJS` web application running on a `macOS` back-end server, our injections should work regardless.

Note: The only exception may be the semi-colon `;`, which will not work if the command was being executed with `Windows Command Line (CMD)`, but would still work if it was being executed with `Windows PowerShell`.

## Injecting Our Command

We can add a semi-colon after our input IP `127.0.0.1`, and then append our command (e.g. `whoami`), such that the final payload we will use is (`127.0.0.1; whoami`), and the final command to be executed would be:


`ping -c 1 127.0.0.1; whoami`

First, let's try running the above command on our Linux VM to ensure it does run:

```
ping -c 1 127.0.0.1; whoami

PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data.
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=1.03 ms

--- 127.0.0.1 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 1.034/1.034/1.034/0.000 ms
21y4d
```

As we can see, the final command successfully runs, and we get the output of both commands (as mentioned in the previous table for `;`). Now, we can try using our previous payload in the `Host Checker` web application:![Host Checker interface with a text field for entering an IP address, showing '127.0.0.1; whoami' entered, a 'Check' button, and a tooltip saying 'Match the requested format'.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/109/cmdinj_basic_injection.jpg)

As we can see, the web application refused our input, as it seems only to accept input in an IP format. However, from the look of the error message, it appears to be originating from the front-end rather than the back-end. We can double-check this with the `Firefox Developer Tools` by clicking `[CTRL + SHIFT + E]` to show the Network tab and then clicking on the `Check` button again:

![Developer tools interface showing Network tab. Instructions: Perform a request or click 'Reload' for network activity details. Click stopwatch icon for performance analysis. No requests displayed.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/109/cmdinj_basic_injection_network.jpg)

As we can see, no new network requests were made when we clicked on the `Check` button, yet we got an error message. This indicates that the `user input validation is happening on the front-end`.

This appears to be an attempt at preventing us from sending malicious payloads by only allowing user input in an IP format. `However, it is very common for developers only to perform input validation on the front-end while not validating or sanitizing the input on the back-end.` This occurs for various reasons, like having two different teams working on the front-end/back-end or trusting front-end validation to prevent malicious payloads.

However, as we will see, front-end validations are usually not enough to prevent injections, as they can be very easily bypassed by sending custom HTTP requests directly to the back-end.

---

## Bypassing Front-End Validation

The easiest method to customize the HTTP requests being sent to the back-end server is to use a web proxy that can intercept the HTTP requests being sent by the application. To do so, we can start `Burp Suite` or `ZAP` and configure Firefox to proxy the traffic through them. Then, we can enable the proxy intercept feature, send a standard request from the web application with any IP (e.g. `127.0.0.1`), and send the intercepted HTTP request to `repeater` by clicking `[CTRL + R]`, and we should have the HTTP request for customization:

#### Burp POST Request

![HTTP request details in raw format, showing headers like Host, User-Agent, and Content-Type, with IP set to 127.0.0.1.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/109/cmdinj_basic_repeater_1.jpg)

We can now customize our HTTP request and send it to see how the web application handles it. We will start by using the same previous payload (`127.0.0.1; whoami`). We should also URL-encode our payload to ensure it gets sent as we intend. We can do so by selecting the payload and then clicking `[CTRL + U]`. Finally, we can click `Send` to send our HTTP request:

#### Burp POST Request

![Interface showing an HTTP request and response. The request includes headers like Host and User-Agent, with IP '127.0.0.1; whoami'. The response displays HTML with a ping result for 127.0.0.1.](https://cdn.services-k8s.prod.aws.htb.systems/content/modules/109/cmdinj_basic_repeater_2.jpg)

As we can see, the response we got this time contains the output of the `ping` command and the result of the `whoami` command, `meaning that we successfully injected our new command`.