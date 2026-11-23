---
title: "Install & Config"
category: ["HOMELAB", "Hermes Agent", "Install & Config"]
---

First of all, let's go to https://community-scripts.org/scripts and search for the Hermes agent to install it in a Proxmox LXC container  
![Pasted image 20261110184042](/VaultSite/wiki-images/Pasted%20image%2020261110184042.png)  
```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/community-scripts/ProxmoxVE/main/ct/hermesagent.sh)"
```

We start the installation on the Proxmox node, and it will automatically create a container  
![Pasted image 20261110184124](/VaultSite/wiki-images/Pasted%20image%2020261110184124.png)  
![Pasted image 20261110192134](/VaultSite/wiki-images/Pasted%20image%2020261110192134.png)  
![Pasted image 20261110184215](/VaultSite/wiki-images/Pasted%20image%2020261110184215.png)  

We will enter the *hermes-setup* line. It's important to choose the full setup as it will allow us to use OpenRoute  
![Pasted image 20261110193902](/VaultSite/wiki-images/Pasted%20image%2020261110193902.png)  
We select OpenRoute as the provider  
![Pasted image 20261110193925](/VaultSite/wiki-images/Pasted%20image%2020261110193925.png)  
Now it will ask for the API KEY  
![Pasted image 20261110194009](/VaultSite/wiki-images/Pasted%20image%2020261110194009.png)  

Let's go to the OpenRoute website and register with our email  

Now we go to the KEYS section and create a new API KEY  
![Pasted image 20261110194233](/VaultSite/wiki-images/Pasted%20image%2020261110194233.png)  
![Pasted image 20261110194223](/VaultSite/wiki-images/Pasted%20image%2020261110194223.png)  
![Pasted image 20261110194409](/VaultSite/wiki-images/Pasted%20image%2020261110194409.png)![Pasted image 20261110194426](/VaultSite/wiki-images/Pasted%20image%2020261110194426.png)  

We return to the container and paste the API KEY  

Now we will choose the AI model and copy its name  
![Pasted image 20261110200328](/VaultSite/wiki-images/Pasted%20image%2020261110200328.png)  
We paste it into the console menu  
![Pasted image 20261110200359](/VaultSite/wiki-images/Pasted%20image%2020261110200359.png)  

Now it will ask us to configure the communication method with the AI. We will choose Telegram  
![Pasted image 20261110200458](/VaultSite/wiki-images/Pasted%20image%2020261110200458.png)  
We press Enter, and it will now explain how to configure Telegram  
![Pasted image 20261110200604](/VaultSite/wiki-images/Pasted%20image%2020261110200604.png)  
We see that it gives us two options: via QR code or manually by creating a bot. We will choose to create a bot with @BotFather  

Let's go to Telegram and search for the bot in the search bar  
![Pasted image 20261110201104](/VaultSite/wiki-images/Pasted%20image%2020261110201104.png)  

Next, we create a new bot and give it a name  
![Pasted image 20261110201159](/VaultSite/wiki-images/Pasted%20image%2020261110201159.png)  
We create the bot, and it will give us the token that we need to input into Hermes  
![Pasted image 20261110201337](/VaultSite/wiki-images/Pasted%20image%2020261110201337.png)  

![Pasted image 20261110201417](/VaultSite/wiki-images/Pasted%20image%2020261110201417.png)  

Now we will need our Telegram ID so that the bot can only communicate with us (we follow the steps provided, and we will have the ID)  
![Pasted image 20261110201527](/VaultSite/wiki-images/Pasted%20image%2020261110201527.png)  
![Pasted image 20261110201741](/VaultSite/wiki-images/Pasted%20image%2020261110201741.png)  
Now it will ask if we want Hermes to start automatically. We choose no  
![Pasted image 20261110201930](/VaultSite/wiki-images/Pasted%20image%2020261110201930.png)  

We leave the CLI tools as Defaults  
![Pasted image 20261110202213](/VaultSite/wiki-images/Pasted%20image%2020261110202213.png)  

Now it will ask in which browser we want the Hermes dashboard to be deployed  
We select Local Browser  
![Pasted image 20261110202441](/VaultSite/wiki-images/Pasted%20image%2020261110202441.png)  

Now we choose to skip since we don't want to generate images with this tool  
![Pasted image 20261110202543](/VaultSite/wiki-images/Pasted%20image%2020261110202543.png)  

As the search engine, we will use Tavily  
![Pasted image 20261110202836](/VaultSite/wiki-images/Pasted%20image%2020261110202836.png)  

Let's go to the Tavily website, register, and copy the API KEY  
![Pasted image 20261110203134](/VaultSite/wiki-images/Pasted%20image%2020261110203134.png)  

We select the default tools again  
![Pasted image 20261110203649](/VaultSite/wiki-images/Pasted%20image%2020261110203649.png)  

We repeat the configuration, and Hermes agent will now be installed  
![Pasted image 20261110203739](/VaultSite/wiki-images/Pasted%20image%2020261110203739.png)  

The main issue now is that Hermes doesn't allow us to deploy the web dashboard because the Telegram bot is already using the port 


```
hermes@hermesagent:~$ hermes dashboard --tui --no-open --host 0.0.0.0 --insecure
Refusing to start: this host is already served by PID 4642 (127.0.0.1:9119; profiles: default).
  You asked for --host 0.0.0.0 (the host owner is bound to 127.0.0.1).
  Stop that backend, or drop the flag to use the running one.
hermes@hermesagent:~$ 
```

To solve this, we'll install tmux which will allow us to launch services in a separate terminal.

- Kill the Hermes service from root: *pkill -f hermes*
- Next, download tmux and launch a terminal:
  - `apt update && apt install -y tmux`
  - `tmux new -s hermes-dash`
- Then execute the dashboard (it will still prompt for a username and password even when using --insecure):
  - `hermes dashboard --tui --no-open --host 0.0.0.0 --insecure`
![Pasted image 20261117175206](/VaultSite/wiki-images/Pasted%20image%2020261117175206.png)
![Pasted image 20261117175216](/VaultSite/wiki-images/Pasted%20image%2020261117175216.png)
Once we confirm the service starts correctly, we'll stop it and launch the Telegram bot gateway:
![Pasted image 20261117175759](/VaultSite/wiki-images/Pasted%20image%2020261117175759.png)

Now we'll use the key combination Ctrl+B followed by double quotes.
We'll see two terminals created, one below the other:
![Pasted image 20261117175946](/VaultSite/wiki-images/Pasted%20image%2020261117175946.png)
Next, we'll simply assign a new port to the Hermes dashboard:
![Pasted image 20261117180113](/VaultSite/wiki-images/Pasted%20image%2020261117180113.png)

To automate this startup process whenever the container boots, we'll create a script:
![Pasted image 20261118180805](/VaultSite/wiki-images/Pasted%20image%2020261118180805.png)
![Pasted image 20261118180843](/VaultSite/wiki-images/Pasted%20image%2020261118180843.png)
Save with Ctrl+O and Ctrl+X.

Now we'll create the dashboard autostart:
![Pasted image 20261118180950](/VaultSite/wiki-images/Pasted%20image%2020261118180950.png)
![Pasted image 20261118181036](/VaultSite/wiki-images/Pasted%20image%2020261118181036.png)
Save with Ctrl+O and Ctrl+X.

Now we'll tell Linux to read these two new files and mark them to execute on every system startup:
![Pasted image 20261118181219](/VaultSite/wiki-images/Pasted%20image%2020261118181219.png)

And we'll verify that the services are active:
![Pasted image 20261118181328](/VaultSite/wiki-images/Pasted%20image%2020261118181328.png)

Once inside the dashboard, we'll configure the skills:
![Pasted image 20261117180314](/VaultSite/wiki-images/Pasted%20image%2020261117180314.png)
- **CHAT**: Main interface for real-time conversation with the AI agent and sending commands.
- **SESSIONS**: History where you can review, resume, or delete previous conversation threads.
- **FILES**: Explorer to manage local documents and files in your LXC that the agent can access.
- **MODELS**: Panel to configure and change the AI engine powering the agent (like Nemotron 3 Ultra).
- **LOGS**: Technical record of events and errors, crucial for diagnosing system failures or network blocks.
- **CRON**: Task scheduler for the bot to automatically run scans, reminders, or commands at set intervals.
- **SKILLS**: Catalog of predefined instructions that teach the agent to act as an expert in specific tasks (very useful for your pentesting environment).
- **DOCUMENTATION**: Direct access to the official manual and project commands for quick troubleshooting.
- **PLUGINS**: Manager for additional modules that add new capabilities and third-party tools to Hermes' core.
- **MCP**: Configuration of the _Model Context Protocol_, a standard for securely connecting the model to external tools or databases.
- **CHANNELS**: Settings for external communication platforms where the bot listens and speaks, like your Telegram integration.
- **WEBHOOKS**: Network links to automate tasks, allowing other applications to send alerts or data directly to Hermes.
- **PAIRING**: Security tool to safely pair new devices or remote clients to this server.
- **PROFILES**: Manager to create different isolated work environments (e.g., one profile for hacking and another for general use).
- **CONFIG**: Global settings panel where you modify the server's overall behavior and interface.
- **KEYS**: Secure vault to store your passwords and access tokens (OpenRouter API keys, Telegram, etc.).
- **SYSTEM**: Monitor showing the health status, reboots, and updates of your container.
- **DOCUMENTATION**: Direct access to the official manual and project commands for quick troubleshooting.

# SKILLS

This section, along with cron and profiles, is one of the most important.

This skill catalog allows us to teach the agent to act as an expert in specific tasks, such as basic pentesting like host reconnaissance.

We'll install the godmode skills:
![Pasted image 20261117184504](/VaultSite/wiki-images/Pasted%20image%2020261117184504.png)

And the Anthropic skill:
![Pasted image 20261117184522](/VaultSite/wiki-images/Pasted%20image%2020261117184522.png)
It's also important to note that we can create our own skills manually in different ways. For example, if we want to make an SQLi skill, we could search for HackerOne reports on SQLi or look up the vulnerability in HackTricks, then pass the URL and a prompt to create the skill around that vulnerability.

Now let's go to the *Profiles* section.

Here we can see the profiles:
![Pasted image 20261117184645](/VaultSite/wiki-images/Pasted%20image%2020261117184645.png)
To put it simply: each profile would be a different "person" with the skills we assign (cybersecurity, development, marketing, etc.). We can create as many profiles as we want, keeping in mind that each profile will use tokens individually and will use the AI engine we specify with the prompt we want.

Let's configure the prompt for this cybersecurity profile.

Default:
![Pasted image 20261117230153](/VaultSite/wiki-images/Pasted%20image%2020261117230153.png)

Our Prompt:
![Pasted image 20261117231653](/VaultSite/wiki-images/Pasted%20image%2020261117231653.png)

Now let's go to the left Kanban section, which will allow us to use the configured profile as if it were a team of people rather than just one:
![Pasted image 20261118184312](/VaultSite/wiki-images/Pasted%20image%2020261118184312.png)

Here we can see different boards like triage, to-do, etc.

## Creating the Team

We'll create two more profiles: one for a programmer and another to generate reports and organize everything, each with their respective skills:
![Pasted image 20261118185748](/VaultSite/wiki-images/Pasted%20image%2020261118185748.png)

These two profiles will use Deepseek as their AI model since it offers a high token volume at a very low price and is delivering excellent results in benchmarks. 