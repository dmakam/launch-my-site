# On-behalf mode: building for someone else

The builder is talking to you; the site owner isn't. Every access route must be **granted by the owner** and **removable by the owner**. The builder never asks the owner for their main login password.

## Ask the builder

- Who owns the domain and hosting, and how do you reach them (email, phone, WhatsApp)?
- Is the owner comfortable with screens and logins, or should we keep their part to one or two clicks?
- One-off launch, or will you maintain the site after?

## Run detection first

`detect_site.py` tells you the situation without bothering the owner. Then pick the route below that asks the least of the owner.

## Routes, easiest for the owner first

1. **Owner invites the builder.**
   - WordPress: owner adds the builder as a user (Editor, or Administrator if needed).
   - Site builders: owner adds the builder as a contributor or collaborator.
   - Hosting: many hosting companies let an owner add a **user or collaborator with limited access** to the account (look for "Users", "Team", "Collaborators" or "Account access" in their dashboard). This is the cleanest route for hosting.
2. **Owner sends files' worth of access, not passwords.** E.g. the owner creates a restricted FTP/SFTP account limited to the website folder, or authorizes the builder's SSH public key (the builder sends the public key; nothing secret travels to the builder). See `credentials.md`.
3. **Short call, owner logs in.** The owner shares their screen or sits with the builder, logs in themselves, and the builder (with Claude) does the publish. Nothing changes hands.
4. **Owner uploads the file.** The builder sends `site.zip` plus a three-step guide for the owner's provider (`route-hosting-panel.md`, rung 4: download and drag).
5. **Owner asks their host's support** using a message the builder drafts.

## Write the owner's message for the builder

Keep it to what the owner needs to do, in plain words, with the reason and how to undo it. Example (WordPress invite):

> Hi Maria, the new site is ready for you to look at: [preview link]. To put it live, I need access to your website. It takes one minute:
> 1. Log in to your website at mariasbakery.com/wp-admin
> 2. Go to **Users → Add New**
> 3. Enter my email (builder@example.com), choose the role **Editor**, and click **Add New User**.
> I'll only change the pages for the new design. Once it's live, you can remove me from the same Users screen.

## Approval and records

- The owner, not the builder, gives the final "yes, publish". Share screenshots or a preview link with the owner directly.
- Keep a short record for the owner: what was changed, where the backup is, what access exists and how to remove it. This goes in the handover.
- If the builder doesn't have the owner's permission to build or publish, stop. Building a site for a business or person without them knowing isn't something this skill does.
