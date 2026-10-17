# Route: hosting with a control panel

The person pays a hosting company and has a dashboard there. Behind it there's usually a control panel (cPanel, Plesk, DirectAdmin or the company's own) with a **file manager**. The site files go in the website's main folder (often called `public_html`, `httpdocs` or `www`).

## Before uploading: find the right folder and protect other sites

One hosting account can serve several domains, each from its own folder. Uploading into the wrong one replaces somebody's other site.

- Find the folder that serves *this* domain. In most panels there's a "Domains" page listing each domain with its folder ("document root"). The scripts check this automatically. In the browser, look it up before uploading.
- Tell the person in plain words: "Your account has two websites. I'll only change the one for yourname.com; yourothersite.com is in a different folder and won't be touched."
- Look at what's already in the folder. If there's an existing site (WordPress, an old site, a "coming soon" page), plan to leave it in place or move it aside, never delete it.

Rung numbers follow the ladder in `publish-routes.md` (rung 2, invite, rarely applies to plain hosting).

## Rung 1: Connect

If the hosting company offers a connector for Claude, use it: they click Connect and approve on the company's page. Use whatever file or site actions it provides. If it can't upload files, it can still help you find the right account and domain. Combine with rung 3.

## Rung 3: They log in, you upload with them

0. Ask permission first, using the script in `publish-routes.md` ("How to offer rung 3"). They type their own password; you never see it. Wait for a yes.
1. Ask them to log in to their hosting account in their browser and open the file manager. Guide: "Look for something called **File Manager**. It might be under a heading like Files, Hosting, or Advanced. Tell me when you see a list of folders."
2. With a browser tool and their permission: go to the domain's folder, upload the site as one .zip, then use the file manager's "Extract" option. Make sure "overwrite" is only enabled for files you're intentionally replacing.
3. Without a browser tool: walk them through the same steps one at a time, asking for a screenshot at each step.
4. If the folder contains an existing `index.php` (common with WordPress), most servers pick `index.html` first, but not all. After upload, load the live homepage. If the old site still shows, add `DirectoryIndex index.html index.php` to the top of the folder's `.htaccess` file. Say what that does in plain words and get a yes first. Reversible: delete the line.
5. Clean up: remove the uploaded .zip from the public folder (move it to the panel's trash, don't permanently delete).

## Rung 4: Download and drag

Give them `site.zip` and a guide written for their panel, three steps max per message:
1. "Open File Manager and click into the folder called `public_html` (or the one I mention)."
2. "Click **Upload**, choose `site.zip`, and wait until it says 100%."
3. "Go back to the folder, right-click `site.zip`, choose **Extract**, and confirm. Then send me a screenshot."

## Rung 5: Credentials for repeat updates

If they'll want regular changes, set up one of these once (`credentials.md`):
- **Control panel API token** → `scripts/deploy_cpanel.py` (cPanel-compatible panels).
- **SFTP / SSH key** → `scripts/deploy_sftp.py` (works with almost any host).

Both scripts confirm the domain is served by that account, back up what they replace, upload, and verify.

## Rung 6: Ask their hosting company

Draft the support message, attach `site.zip`, and they send it:

> Hi, I'd like to publish a new website on yourdomain.com. Could you please upload the attached site.zip to the main folder for yourdomain.com and extract it there? Please don't delete anything already in that folder; the new files can sit alongside the existing ones. Thank you!

## Caching after updates

Hosts often tell browsers to keep pages for hours. After an update, if the old version shows:
- Version your CSS/JS links (`styles.css?v=2`) and bump the number on every change. The build guide does this by default.
- Tell the person: "If you still see the old version, press Ctrl+Shift+R (Cmd+Shift+R on a Mac). New visitors already see the new one."
- If the host has a caching/CDN toggle in its dashboard, offer to clear it with them.
