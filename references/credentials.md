# Last resort: credential routes

Use only when no secret-free route works, the owner wants regular hands-off updates, or they're technical and ask. Read the "Secrets" section of `SKILL.md` first.

## How to frame it

Explain the trade-off in one or two sentences, then let them choose:

> To update your site without you logging in each time, I'd need a special key from your hosting account. It only allows changing the website files, it can expire automatically, and you can switch it off any time. Setting it up takes about ten minutes, and I'll guide you through every click. Or we can keep doing it together whenever you want a change. Which would you prefer?

## Universal safety rules

- **Narrowest access, with an expiry.** Pick the smallest scope the provider offers, and an expiry date if offered.
- **Never in the chat.** The secret goes into a `.env` file next to the scripts, on the machine that runs them. Show them how: "Open the file called `.env.example`, save a copy named `.env`, paste the key after the `=` sign, and save."
- **You never type it into a web form.** If it has to go into a provider's screen (rare), the person does it.
- **If it's pasted into the chat:** don't use it. Ask them to delete it in the provider and create a new one, and say why in one kind sentence.
- **Revoke at the end** if updates aren't ongoing. Put the revoke steps in the handover.

## Control panel API token (cPanel-style panels)

Used by `scripts/deploy_cpanel.py`.

1. "Log in to your hosting and open the **control panel**." (Some hosts open it from a button called "cPanel", "Advanced" or "Manage hosting".)
2. "Use the search box at the top to search for **API Tokens** and open it." (Usually under Security.)
3. "Click **Create**. Name it `website-updates`. If there's an expiry option, pick a date a few months away. Click **Create** again."
4. "Copy the long code it shows; it's only shown once. Paste it into your `.env` file after `CPANEL_TOKEN=`."
5. The other values (`CPANEL_HOST`, `CPANEL_USER`) are usually shown on the control panel's home screen (server name and username). Ask for a screenshot and read them off it yourself rather than making them hunt.

Revoke: same screen, **Revoke/Delete** next to `website-updates`.

## SFTP / SSH key (almost any host)

Used by `scripts/deploy_sftp.py`. A key pair is safer than a password and can be removed without changing any password.

1. Generate the key pair yourself on the machine that will deploy (`ssh-keygen -t ed25519 -f ./deploy_key -N ""`). The private key never leaves that machine.
2. The *public* key (`deploy_key.pub`) isn't secret. The person pastes it into their host's "SSH Access"/"SSH Keys" page and clicks Authorize/Add. Guide them there by search: "Search the control panel for **SSH**."
3. The host, port and username are on that same page. Ask for a screenshot.
4. If the host doesn't support keys, SFTP with a password works the same way via `.env`. Prefer a separate FTP/SFTP account limited to the website folder over their main password. Many panels let you create one under "FTP Accounts", restricted to one directory.

Revoke: delete the key (or the extra FTP account) on the same page.

## WordPress Application Password

Used by `scripts/publish_wordpress.py`. Lets the script create and edit pages through WordPress's built-in API. It's separate from their login password and revocable on its own.

1. "Log in to WordPress, then go to **Users → Profile** (or click your name at the top right)."
2. "Scroll down to **Application Passwords**. Type `website-updates` as the name and click **Add New Application Password**."
3. "Copy the code it shows (spaces are fine) into your `.env` after `WP_APP_PASSWORD=`, and your WordPress username after `WP_USER=`."

If there's no Application Passwords section, the site may be on an old WordPress version, have it disabled by a security plugin, or not use HTTPS. Fall back to the invite or log-in routes.

Revoke: same section, **Revoke**.

## Static host deploy token

For hosts like Netlify or Cloudflare Pages when they want automatic updates: prefer connecting a Git repository (no token to handle). If a token is required, create it with the narrowest scope and an expiry, and store it in `.env` the same way.
