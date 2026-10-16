# Going live and handing over

## Verify on the real domain

```
python scripts/verify_live.py https://theirdomain.com --pages index.html about.html contact.html
```

It checks every page and asset returns OK, that images load, that share tags are present and the share image is reachable, and prints a plain summary. If a page returns 403 to the script but loads in a browser, it's usually the host's bot protection. Check it in a real browser before worrying.

Also open the homepage in a real browser with a fresh load. If an old version shows, it's browser caching (see `route-hosting-panel.md`, "Caching").

## The handover message

Short, plain, and complete. Template:

> **Your site is live at theirdomain.com** 🎉
>
> **What's there:** Home, About, Menu, Contact. Checked on desktop and phone.
>
> **If you see the old version:** press Ctrl+Shift+R (Cmd+Shift+R on a Mac). New visitors already see the new one.
>
> **Your old site:** saved as a backup at [where]. Nothing was deleted.
>
> **Access you gave me:** [the WordPress user / API token / SSH key / collaborator access]. To remove it: [exact steps]. *(Or: none, since you logged in yourself.)*
>
> **Still to do (if any):** [e.g. the contact form needs a form service to deliver messages; let me know which email to use.]
>
> **Changing things later:** just tell me what to change. [Repeatable route set up? "I can update it directly." / Otherwise: "We'll do the same quick log-in together."]
>
> **Sources** for the facts on the site: [list]

## On-behalf mode

Send the owner their own version of the handover (or have the builder forward it), especially the access list and how to remove it.
