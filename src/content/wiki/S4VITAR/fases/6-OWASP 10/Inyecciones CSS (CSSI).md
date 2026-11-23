---
title: "Inyecciones CSS (CSSI)"
category: ["S4VITAR", "fases", "6-OWASP 10", "Inyecciones CSS (CSSI)"]
---

**CSS Injections** (**CSSI**) are a type of web vulnerability that allows an attacker to inject malicious CSS code into a webpage. This occurs when a web application trusts untrusted user input and uses it directly in its CSS code without proper validation.

The injected malicious CSS code can alter the page's style and layout, enabling attackers to perform actions such as **identity spoofing** or **stealing sensitive information**.

CSS Injections (CSSI) can be used by attackers as an attack vector to exploit **Cross-Site Scripting** (**XSS**) vulnerabilities. Imagine a web application that allows users to input text into a field displayed on a webpage. If the application developer does not properly validate and filter the user's input, an attacker could inject malicious code into the input field, including JavaScript code.

If the injected CSS code is "complex enough," it can trick the web browser into interpreting the code as JavaScript. This means the malicious CSS code can be used to inject JavaScript into the webpage, known as CSS-Induced JavaScript Injection.

Once the JavaScript code has been injected into the page, the attacker can use it to perform a Cross-Site Scripting (XSS) attack. At this point, the attacker could inject a malicious script to steal user credentials or redirect them to a fake webpage, among many other possible attack vectors.
