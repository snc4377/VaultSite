---
title: "Web Automatica"
category: ["HOMELAB", "Hermes Agent", "Web automatica"]
---

Note title: Automatic Web

We've created a profile in Hermes Agent called webdev.

### Brainstorming
Okay, let's organize this webdev profile. It will be a profile with Open-Design installed to create the website and make it visually appealing (not sure if you'd want it to provide reference web pages). Then, using Super Powers and Open Design, it will create the sections I want, which are roughly: contact information (my LinkedIn, HTB, and GitHub profiles), my portfolio/presentation (i.e., my projects), another section for the wiki, and another for the blog. 

For my portfolio and the wiki based on my Obsidian notes, I want to connect it with the Super Powers skill, but I'm not sure how it will fetch the notes (I was thinking of creating an LXC container in my Proxmox and using Obsidian Livesync to connect my PC's vault to my server, and then have webdev pull the info from there). For the news section, I plan to use GitHub Actions and n8n, also hosted on my server, to search for news every few days and generate an article about it. I plan to host all this on GitHub Pages.

### Profile Creation

We created the webdev prompt using articles and guides found online. 

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

Note title: Automatic Web

![Pasted image 20261119194007](/VaultSite/wiki-images/Pasted%20image%2020261119194007.png)

Once the prompt is created, we'll edit the AGENT.md file so it reads and understands our web concept and follows the instructions:
`nano ~/.hermes/profiles/webdev/AGENT.md`
![Pasted image 20261119194253](/VaultSite/wiki-images/Pasted%20image%2020261119194253.png)

Now we'll select the AI model:
![Pasted image 20261119194359](/VaultSite/wiki-images/Pasted%20image%2020261119194359.png)
Next, we'll install the two main skills for this project:

[Open-design](https://hermesatlas.com/projects/nexu-io/open-design)
OpenDesign is an open-source collaborative workspace for creating and refining prototypes with a coding agent or OpenDesign Cloud. It provides skills, design templates, design systems, and plugins that teams can inspect and adapt, and supports creating web prototypes, slides, images, and motion graphics.

[Superpowers](https://hermesatlas.com/projects/obra/superpowers)
Superpowers is a software development methodology for coding agents, built from composable skills and initial instructions that guide agents to use them. Its workflow elicits and presents a specification, creates an implementation plan emphasizing TDD, YAGNI, and DRY, then uses subagents to carry out and review engineering tasks.

![Pasted image 20261119195212](/VaultSite/wiki-images/Pasted%20image%2020261119195212.png)
The skills are now installed in the profile.

We restart the container with hermes.

### Base web with Astro in hermes

We open the webdev dashboard and pass it the prompt we created to generate the base website (the web skeleton) we'll build upon.

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
Note title: Automatic Web

![Pasted image 20261119201908](/VaultSite/wiki-images/Pasted%20image%2020261119201908.png)
Very important: in the workspace section, change the path to a dedicated folder we've set aside, as this is where it will create everything, keeping it controlled and organized.

![Pasted image 20261119202750](/VaultSite/wiki-images/Pasted%20image%2020261119202750.png)

Press enter and let the agent start working.
![Pasted image 20261119203457](/VaultSite/wiki-images/Pasted%20image%2020261119203457.png)![Pasted image 20261119203948](/VaultSite/wiki-images/Pasted%20image%2020261119203948.png)

The next step is customizing the web, as it will have created a default Astro site on container port 4321.

To edit the site's style, we'll need to create a brand.md file in the project path. We'll instruct webdev to use this file as reference and leverage open design and claude design tools to finalize the site design.
![Pasted image 20261119214046](/VaultSite/wiki-images/Pasted%20image%2020261119214046.png)



### GitHub Synchronization

1. Go to [github.com](https://github.com/) and create a **New Repository**.
    - Name it VaultSite.
    - **IMPORTANT:** Keep it **public** (required for free GitHub Pages usage).
    - The repository must be public to use GitHub Pages. Don't check "Add a README file", nor add `.gitignore` or license. It must be completely empty.
        
2. Navigate to your GitHub settings: `Settings > Developer Settings > Personal access tokens > Tokens (classic)`.
    - Generate a new token.
    - Grant it **`repo`** permissions (to push code) and **`workflow`** permissions (to create the automatic deployment file).

3. Now we need to provide this prompt so it can find the GitHub repository (when prompted for password, use the token)
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

Note title: Automatic Web

![Pasted image 20261120010940](/VaultSite/wiki-images/Pasted%20image%2020261120010940.png)

If everything went well, we should get a URL to our repository but in the deploy keys section.
![Pasted image 20261120011346](/VaultSite/wiki-images/Pasted%20image%2020261120011346.png)

Here we'll paste the SSH key provided by the agent. *IMPORTANT*: allow write access to the key.
![Pasted image 20261120011509](/VaultSite/wiki-images/Pasted%20image%2020261120011509.png)

Now we just return to the agent and confirm we've added it.

Back to GitHub in the repository:

1. At the top, click the **Settings** tab.
2. In the left menu, find and click **Pages**.
3. In the Build and deployment section, locate the Source subsection.
4. Change it from "Deploy from a branch" to **"GitHub Actions"**.
![Pasted image 20261120012414](/VaultSite/wiki-images/Pasted%20image%2020261120012414.png)

Go to the Actions section and launch the workflow.
![Pasted image 20261120013157](/VaultSite/wiki-images/Pasted%20image%2020261120013157.png)

Once the status changes from yellow to green, the site will be live.
![Pasted image 20261120013506](/VaultSite/wiki-images/Pasted%20image%2020261120013506.png)

### Wiki Creation

We have our notes locally in Obsidian, but to publish them to the web we'd need to convert them to Astro or HTML format, which we don't want.

Let's create a new container with n8n:
`bash -c "$(curl -fsSL https://raw.githubusercontent.com/community-scripts/ProxmoxVE/main/ct/n8n.sh)"`

Once the n8n container is created, it will provide an IP. Access it via browser at the IP on port 5678.
![Pasted image 20261120160225](/VaultSite/wiki-images/Pasted%20image%2020261120160225.png)

Inside, go to PERSONAL>NEW CREDENTIAL, select GitHub API, and enter the API key we created earlier in Git along with the username.
![Pasted image 20261120161402](/VaultSite/wiki-images/Pasted%20image%2020261120161402.png)

Now let's go to the Obsidian Sync container we created. We'll need to edit the local.ini file.

First, stop the CouchDB service.
Scroll to the [admins] section, remove the semicolon, and add our password.
![Pasted image 20261121020627](/VaultSite/wiki-images/Pasted%20image%2020261121020627.png)

Now restart the service and we'll have web access.
![Pasted image 20261121020819](/VaultSite/wiki-images/Pasted%20image%2020261121020819.png)

Once logged into CouchDB, we'll see a pre-existing database called obsidiannotes.
![Pasted image 20261121145020](/VaultSite/wiki-images/Pasted%20image%2020261121145020.png)

Now we need to go to our Obsidian and install the livesync plugin, then activate it.
![Pasted image 20261121145142](/VaultSite/wiki-images/Pasted%20image%2020261121145142.png)

Go to the plugin settings and edit remote access.
![Pasted image 20261121145243](/VaultSite/wiki-images/Pasted%20image%2020261121145243.png)
![Pasted image 20261121150611](/VaultSite/wiki-images/Pasted%20image%2020261121150611.png)
![Pasted image 20261121150646](/VaultSite/wiki-images/Pasted%20image%2020261121150646.png)

Connection config:
![Pasted image 20261121150707](/VaultSite/wiki-images/Pasted%20image%2020261121150707.png)![Pasted image 20261121150834](/VaultSite/wiki-images/Pasted%20image%2020261121150834.png)

Now go to the encryption section and set a passphrase.

If we don't want to upload all vault folders, we need to enable advanced plugin options and use filters.

**Example:** Imagine your folders are named `HTB`, `Apuntes`, and `Cheatsheets`. In the whitelist you'd enter exactly this (case-sensitive, no spaces):

regex

^(HTB|Apuntes|Cheatsheets)/.*

- `^` means "starts with".
- `|` means "or".
- `/.*` means "and everything inside that folder".
- _(If your folders have subfolders, this will include them automatically)._

Once the vault is synced, we need to go to the Obsidian container and install these two packages:

`apt update && apt install -y nodejs npm`
`npm install -g @jr2804/livesync-cli`

Now in the local Obsidian on the PC, press ctrl+P and search for **`Self-hosted LiveSync: Copy settings as a new setup URI`** or similar.
![Pasted image 20261122181556](/VaultSite/wiki-images/Pasted%20image%2020261122181556.png)

Generate the URI.
![Pasted image 20261122181607](/VaultSite/wiki-images/Pasted%20image%2020261122181607.png)

Now we need to go to the container and create a folder where the CLI will store decrypted notes:

`mkdir -p /opt/obsidian-vault`

Now we'll specify the target location and the passphrase to use for decryption:
`livesync-cli /opt/obsidian-vault "PASTE_THE_SETUP_URI_HERE"`

Once configured, we'll sync it:

`livesync-cli /opt/obsidian-vault daemon`

This command will connect to your CouchDB, decrypt the notes using the Setup URI passphrase, and save them as .md files in `/opt/obsidian-vault`.

![Pasted image 20261122182028](/VaultSite/wiki-images/Pasted%20image%2020261122182028.png)

Here we can see the sync worked, but we get a warning that the daemon is running in the background - everything works but new notes in Obsidian won't update in real time, and we want live updates.
![Pasted image 20261122192751](/VaultSite/wiki-images/Pasted%20image%2020261122192751.png)

To fix this, we'll edit settings.json with this command:
`sed -i 's/"liveSync": false/"liveSync": true/' /opt/obsidian-vault/.livesync/settings.json`

Now restart the daemon and the error should be gone.

To verify proper syncing, we can check the vault folder we configured earlier and see our note folders.

Now we need to make Hermes see this folder with the files, so we'll go to the Proxmox host and mount the folder:
`mkdir -p /mnt/obsidian-shared`
And edit access permissions:
![Pasted image 20261122201126](/VaultSite/wiki-images/Pasted%20image%2020261122201126.png)
Now we need to edit the config file for each relevant container (in this case Obsidian and Hermes) and add this line at the end:
`mp0: /mnt/obsidian-shared,mp=/opt/obsidian-vault`
![Pasted image 20261122201308](/VaultSite/wiki-images/Pasted%20image%2020261122201308.png)
- mp0: First mount point.
- /mnt/obsidian-shared: Host path.
- mp=/opt/obsidian-vault: Path where it will appear inside the container.

Final step: connect the Hermes agent with the Obsidian CLI to upload it to the web. 
