Search operators are like search engines' secret codes. These special commands and modifiers unlock a new level of precision and control, allowing you to pinpoint specific types of information amidst the vastness of the indexed web.

While the exact syntax may vary slightly between search engines, the underlying principles remain consistent. Let's delve into some essential and advanced search operators:

|Operator|Operator Description|Example|Example Description|
|:--|:--|:--|:--|
|`site:`|Limits results to a specific website or domain.|`site:example.com`|Find all publicly accessible pages on example.com.|
|`inurl:`|Finds pages with a specific term in the URL.|`inurl:login`|Search for login pages on any website.|
|`filetype:`|Searches for files of a particular type.|`filetype:pdf`|Find downloadable PDF documents.|
|`intitle:`|Finds pages with a specific term in the title.|`intitle:"confidential report"`|Look for documents titled "confidential report" or similar variations.|
|`intext:` or `inbody:`|Searches for a term within the body text of pages.|`intext:"password reset"`|Identify webpages containing the term “password reset”.|
|`cache:`|Displays the cached version of a webpage (if available).|`cache:example.com`|View the cached version of example.com to see its previous content.|
|`link:`|Finds pages that link to a specific webpage.|`link:example.com`|Identify websites linking to example.com.|
|`related:`|Finds websites related to a specific webpage.|`related:example.com`|Discover websites similar to example.com.|
|`info:`|Provides a summary of information about a webpage.|`info:example.com`|Get basic details about example.com, such as its title and description.|
|`define:`|Provides definitions of a word or phrase.|`define:phishing`|Get a definition of "phishing" from various sources.|
|`numrange:`|Searches for numbers within a specific range.|`site:example.com numrange:1000-2000`|Find pages on example.com containing numbers between 1000 and 2000.|
|`allintext:`|Finds pages containing all specified words in the body text.|`allintext:admin password reset`|Search for pages containing both "admin" and "password reset" in the body text.|
|`allinurl:`|Finds pages containing all specified words in the URL.|`allinurl:admin panel`|Look for pages with "admin" and "panel" in the URL.|
|`allintitle:`|Finds pages containing all specified words in the title.|`allintitle:confidential report 2023`|Search for pages with "confidential," "report," and "2023" in the title.|
|`AND`|Narrows results by requiring all terms to be present.|`site:example.com AND (inurl:admin OR inurl:login)`|Find admin or login pages specifically on example.com.|
|`OR`|Broadens results by including pages with any of the terms.|`"linux" OR "ubuntu" OR "debian"`|Search for webpages mentioning Linux, Ubuntu, or Debian.|
|`NOT`|Excludes results containing the specified term.|`site:bank.com NOT inurl:login`|Find pages on bank.com excluding login pages.|
|`*` (wildcard)|Represents any character or word.|`site:socialnetwork.com filetype:pdf user* manual`|Search for user manuals (user guide, user handbook) in PDF format on socialnetwork.com.|
|`..` (range search)|Finds results within a specified numerical range.|`site:ecommerce.com "price" 100..500`|Look for products priced between 100 and 500 on an e-commerce website.|
|`" "` (quotation marks)|Searches for exact phrases.|`"information security policy"`|Find documents mentioning the exact phrase "information security policy".|
|`-` (minus sign)|Excludes terms from the search results.|`site:news.com -inurl:sports`|Search for news articles on news.com excluding sports-related content.|

### Google Dorking

Google Dorking, also known as Google Hacking, is a technique that leverages the power of search operators to uncover sensitive information, security vulnerabilities, or hidden content on websites, using Google Search.

Here are some common examples of Google Dorks, for more examples, refer to the [Google Hacking Database](https://www.exploit-db.com/google-hacking-database):

- Finding Login Pages:
    - `site:example.com inurl:login`
    - `site:example.com (inurl:login OR inurl:admin)`
- Identifying Exposed Files:
    - `site:example.com filetype:pdf`
    - `site:example.com (filetype:xls OR filetype:docx)`
- Uncovering Configuration Files:
    - `site:example.com inurl:config.php`
    - `site:example.com (ext:conf OR ext:cnf)` (searches for extensions commonly used for configuration files)
- Locating Database Backups:
    - `site:example.com inurl:backup`
    - `site:example.com filetype:sql`


Thats a huge List of google dorks made by [BullsEye0](https://github.com/BullsEye0/google_dork_list.git)
![[Content Bin/google_Dorks.txt]]

### Some Examples 

|**Google Dork**|**Description**|
|---|---|
|`intitle:"Index of" password.txt`|Displays directories containing text files with names like "password.txt".|
|`intitle:"Index of" /admin`|Displays administration directories on websites.|
|`filetype:xls inurl:"email.xls"`|Displays lists of exposed emails.|
|`inurl:"login" site:example.com`|Finds login pages on a specific website.|
|`filetype:log inurl:"password.log"`|Finds log files containing "password" in their name.|
|`intitle:index.of id_rsa -id_rsa.pub`|Finds SSH private keys.|
|`site:.gov intitle:"secret" filetype:pdf`|Finds government files exposed on the internet.|
|`intext:"Welcome to phpMyAdmin"`|Searches for pages containing the string "Welcome to phpMyAdmin" in their content.|
|`inurl:/wp-content/uploads/ filetype:pdf`|Finds PDF files in the "uploads" folder of WordPress-based websites.|
|`intitle:"Index of" /backup`|Displays directories containing backup files.|
|`site:example.com ext:sql`|Finds SQL files on the specified website.|
|`intitle:"index of" "database.sql"`|Finds SQL database files.|
|`intitle:"SQL Injection" site:example.com`|Finds web pages containing the phrase "SQL Injection" on a specific website.|
|`site:example.com ext:doc`|Finds Microsoft Word documents on the specified website.|
|`site:example.com ext:xml`|Finds XML documents on the specified website.|
|`site:example.com ext:conf`|Searches for configuration files on the specified website.|
|`inurl:"/cgi-bin/pass.txt"`|Searches for text files named "pass.txt" in "cgi-bin" folders.|
|`intitle:"WebcamXP 5"`|Finds webcams accessible via WebcamXP 5.|
|`site:example.com inurl:config`|Searches for configuration files on the specified website.|
|`intitle:"index of" intext:config.php`|Displays directories containing PHP configuration files.|
|`intitle:"index of" intext:.htpasswd`|Finds directories containing .htpasswd files.|
|`intitle:"index of" intext:.env`|Searches for directories containing .env files.|
|`intitle:"index of" "wp-content/uploads" site:example.com`|Finds uploaded WordPress files on a specific website.|
|`filetype:xls inurl:"email.xls"`|Finds Excel spreadsheet files containing "email" in their name.|
|`intext:"Powered by phpBB"`|Displays websites that use the phpBB content management system.|
|`intext:"Powered by Wordpress"`|Displays websites that use WordPress.|
|`intext:"@outlook.com" site:example.com`|Finds websites containing Outlook email addresses on a specific site.|
|`inurl:/dana-na/ filetype:cgi`|Finds CGI pages in the "/dana-na/" folder.|
|`inurl:server-info "Apache Server Information"`|Displays Apache server information.|
|`intext:"sql syntax near"`|Displays websites with potential SQL syntax errors.|
|`intext:"confidential" site:example.com`|Finds web pages containing the word "confidential" on a specific website.|
|`inurl:/proc/self/cwd`|Displays the current working directory of a server.|
|`intitle:"index of" intext:web.config`|Finds web configuration files in indexed directories.|
|`filetype:reg reg HKEY_CURRENT_USER username`|Searches for registry files containing the string "username" in the HKEY_CURRENT_USER key.|
|`inurl:"ViewerFrame?Mode="`|Finds webcams accessible via viewer scripts.|
|`intext:"powered by vBulletin"`|Displays websites that use the vBulletin content management system.|
|`intitle:"index of" inurl:ftp`|Finds FTP servers that have indexed directories.|
|`intitle:"index of" "WhatsAppDB.csv"`|Displays directories containing WhatsApp database CSV files.|
|`filetype:env intext:APP_ENV`|Searches for configuration files with information about the application environment.|
|`inurl:"/phpinfo.php"`|Displays PHP server information.|
|`intitle:"index of" intext:sftp-config.json`|Finds SFTP configuration files in indexed directories.|
