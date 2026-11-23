---
title: "Web Automatica"
category: ["HOMELAB", "Hermes Agent", "Web automatica"]
---

We have created a profile in Hermes Agent named webdev.

### Brainstorming 
Alright, let's organize this webdev profile. It will be a profile that has open-design installed to create the website and make it visually appealing (I'm not sure if you'd want me to provide reference web pages). Then, with superpowers and open-design, I'll create the sections I want, which are roughly: contact information (my LinkedIn, HTB, and GitHub profiles), my portfolio presentation (i.e., my projects), another window for the wiki, and then another window for the blog. The idea for my portfolio and the wiki, based on my Obsidian notes, is to have it connected with the superpowers skill, but I'm not sure how it will fetch the notes (I was thinking of creating an LXC container in my Proxmox and using Obsidian Livesync to connect my vault from my PC to my server, and from there, webdev would grab the info for that section). For the news section, I plan to use GitHub Actions and n8n, also hosted on my server, to search for news every X days and create an article about it. I was thinking of hosting all of this on GitHub Pages.

### Profile Creation 

We created the webdev prompt using articles and guides we found online. 

```
You are **WebDev**, a senior frontend architect and UI/UX designer. Your mission is to build blazing-fast, aesthetically stunning, and highly structured websites. 

## Your Lane (Work Stream)
- Master of the Astro framework.
- Obsessed with clean code, modular components, and web performance.
- Expert in translating visual references into functional, responsive design.
- You build with a "mobile-first" and "dark-mode-first" philosophy.

## Operating Rules
- Never compromise on design quality. If a layout looks basic, improve it.
- Always explain your architectural decisions briefly before writing code.
- Deliver code in logical, testable chunks. Do not dump 20 files at once.
- You work exclusively on the `webdev` project. Do not interfere with other system tasks.
```

Once the prompt is created, what we will do is edit the AGENT.md file so that it reads and understands the concept of the web we want and follows the instructions  
`nano ~/.hermes/profiles/webdev/AGENT.md`  
![Pasted image 20261119194253](/VaultSite/wiki-images/Pasted%20image%2020261119194253.png)  

Now we will select the AI model  
![Pasted image 20261119194359](/VaultSite/wiki-images/Pasted%20image%2020261119194359.png)  
And now we will install the two main skills for this project:  

[Open-design](https://hermesatlas.com/projects/nexu-io/open-design)  
OpenDesign is an open-source collaborative workspace for creating and refining prototypes with a coding agent or OpenDesign Cloud. It provides skills, design templates, design systems, and plugins that teams can inspect and adapt, and supports creating web prototypes, slides, images, and motion graphics.  

[Superpowers](https://hermesatlas.com/projects/obra/superpowers)  
Superpowers is a software development methodology for coding agents, built from composable skills and initial instructions that guide agents to use them. Its workflow elicits and presents a specification, creates an implementation plan emphasizing TDD, YAGNI, and DRY, then uses subagents to carry out and review engineering tasks.  

![Pasted image 20261119195212](/VaultSite/wiki-images/Pasted%20image%2020261119195212.png)  
We now have the skills installed in the profile.  

We restart the container with Hermes.  

### Web base with Astro in Hermes  

We open the webdev dashboard and pass it the prompt we created so that it generates the web we will base our work on (the skeleton of the web).

```
Hello WebDev. We are starting the project from scratch.

Please follow these steps carefully:
1. Create a new directory called `portfolio` in the current path and navigate into it (e.g., `mkdir portfolio && cd portfolio`).
2. Initialize a new Astro project using npm. Use the minimal template and TypeScript. Ensure it does NOT initialize a git repository yet (use the `--no-git` flag if necessary).
3. Add Tailwind CSS to the project using the official Astro integration.
4. Create the basic folder structure. Inside `src/pages`, create 4 files: `index.astro` (Home), `portfolio.astro`, `wiki.astro`, and `blog.astro`.
5. Create a shared layout component at `src/layouts/Layout.astro`. It must include a responsive navigation bar with links to the 4 pages. 
6. Use your Open Design and Superpowers skills to make the layout look modern and professional (dark mode by default, clean typography, nice hover effects on the nav links).
7. Put some placeholder text in each of the 4 pages to verify the routing works.

Show me the exact terminal commands you are running and then output the code for the Layout and the pages. Do not install any external databases or automation tools yet.
```
Note title: Untitled

![Pasted image 20261119201908](/VaultSite/wiki-images/Pasted%20image%2020261119201908.png)
It is very important in the workspace section to change the path to a separate folder we have, as everything will be created there, and this way we will have everything controlled and organized.

![Pasted image 20261119202750](/VaultSite/wiki-images/Pasted%20image%2020261119202750.png)

We press enter and start the agent working.
![Pasted image 20261119203457](/VaultSite/wiki-images/Pasted%20image%2020261119203457.png)![Pasted image 20261119203948](/VaultSite/wiki-images/Pasted%20image%2020261119203948.png)

As the next step, we will need to customize the website since it will have created a website on port 4321 of the container, but it is the default Astro website.

So now, to edit the style of the website, what we would have to do is create a `brand.md` file in the project path and tell the webdev to use the file as a reference and use the tools of open design and claude design to finish designing the website.
![Pasted image 20261119214046](/VaultSite/wiki-images/Pasted%20image%2020261119214046.png)

### Synchronization with GitHub

1. Go to [github.com](https://github.com/) and create a **New Repository**.
    - We will name it VaultSite.
    - **IMPORTANT:** Leave it **public** (necessary to use GitHub Pages for free).
    - We have to leave the repository public to use GitHub Pages, and do not check the "Add a README file" box, nor add `.gitignore` or a license. It must be completely empty.
        
2. Go to your GitHub settings: `Settings > Developer Settings > Personal access tokens > Tokens (classic)`.
    - Generate a new token.
    - Mark it with the **`repo`** permissions (to be able to upload code) and **`workflow`** (so it can create the automatic deployment file).

3. Now we need to pass this prompt so it can find the GitHub repository (when it asks for the password, we will enter the token).
```
Excellent work. The design is perfect. Now we need to deploy this to the internet.

Please do the following steps:
1. Initialize a local Git repository in this folder (if not already done).
2. Create a proper `.gitignore` file so we don't push `node_modules` or `dist`.
3. Add the remote origin. My GitHub username is [TU_USUARIO_DE_GITHUB] and the repository name is [NOMBRE_DEL_REPO]. Use the URL: `https://github.com/[TU_USUARIO]/[NOMBRE_DEL_REPO].git`.
4. Create the GitHub Actions workflow file at `.github/workflows/deploy.yml` to automatically build and deploy this Astro site to GitHub Pages. (Use the official Astro action, `withastro/action@v3`, and make sure the workflow has the correct permissions for `pages` and `id-token`).
5. Update `astro.config.mjs` with the `site` and `base` properties if necessary for GitHub Pages.
6. Commit all files with the message "Initial commit: Astro portfolio skeleton deployed".
7. Push the code to the `main` branch. 

I will provide the GitHub Personal Access Token for authentication when you prompt for it.
```

![Pasted image 20261120010940](/VaultSite/wiki-images/Pasted%20image%2020261120010940.png)

If everything went well, we should get a URL to our repository but for the deploy keys section.
![Pasted image 20261120011346](/VaultSite/wiki-images/Pasted%20image%2020261120011346.png)

Here we'll paste the SSH key provided by the agent. *IMPORTANT*: allow write access for the key.
![Pasted image 20261120011509](/VaultSite/wiki-images/Pasted%20image%2020261120011509.png)

Now we simply return to the agent and confirm we've added it.

Go back to the GitHub repository:

1. At the top, click the **Settings** tab.
2. In the left menu, find and click **Pages**.
3. In the Build and deployment section, locate the Source subsection.
4. Change it from "Deploy from a branch" to **"GitHub Actions"**.
![Pasted image 20261120012414](/VaultSite/wiki-images/Pasted%20image%2020261120012414.png)

Go to the Actions section and trigger the workflow.
![Pasted image 20261120013157](/VaultSite/wiki-images/Pasted%20image%2020261120013157.png)

Once the light turns from yellow to green, the site will be live.
![Pasted image 20261120013506](/VaultSite/wiki-images/Pasted%20image%2020261120013506.png)

### Wiki Creation

We have our notes locally in Obsidian, but to publish them to the web we'd normally need to convert them to Astro or HTML format - which we want to avoid.

Let's create a new container with n8n:
`bash -c "$(curl -fsSL https://raw.githubusercontent.com/community-scripts/ProxmoxVE/main/ct/n8n.sh)"`

Once the n8n container is created, it will provide an IP. Access it via browser at the IP on port 5678.
![Pasted image 20261120160225](/VaultSite/wiki-images/Pasted%20image%2020261120160225.png)

Inside, go to PERSONAL>NEW CREDENTIAL, select GitHub API, and enter the API key we created earlier in Git along with the username.
![Pasted image 20261120161402](/VaultSite/wiki-images/Pasted%20image%2020261120161402.png)

Now let's go to the Obsidian Sync container we created. We'll need to edit the local.ini file.

First, stop the CouchDB service:
Scroll down to the [admins] section, remove the semicolon and enter our password.
![Pasted image 20261121020627](/VaultSite/wiki-images/Pasted%20image%2020261121020627.png)

Now restart the service and we'll have web access.
![Pasted image 20261121020819](/VaultSite/wiki-images/Pasted%20image%2020261121020819.png)

Once we've accessed CouchDB, we'll see a pre-existing database called obsidiannotes.
![Pasted image 20261121145020](/VaultSite/wiki-images/Pasted%20image%2020261121145020.png)

Now we need to go to our Obsidian and install/activate the livesync plugin.
![Pasted image 20261121145142](/VaultSite/wiki-images/Pasted%20image%2020261121145142.png)

Go to the plugin settings and edit remote access:
![Pasted image 20261121145243](/VaultSite/wiki-images/Pasted%20image%2020261121145243.png)
![Pasted image 20261121150611](/VaultSite/wiki-images/Pasted%20image%2020261121150611.png)
![Pasted image 20261121150646](/VaultSite/wiki-images/Pasted%20image%2020261121150646.png)

Connection config:
![Pasted image 20261121150707](/VaultSite/wiki-images/Pasted%20image%2020261121150707.png)![Pasted image 20261121150834](/VaultSite/wiki-images/Pasted%20image%2020261121150834.png)

Now go to the encryption selection and set a passphrase. 


