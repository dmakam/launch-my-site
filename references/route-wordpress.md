# Route: existing WordPress site

First ask which they want, in plain words:

> Your current site runs on WordPress. Do you want to **(a)** replace it with the new design, or **(b)** keep WordPress so you can keep editing it yourself, and make it look like the new design?

## (a) Replace WordPress with the new site

Don't uninstall or delete WordPress. Put the new static site in the same folder so it takes over the homepage, and leave WordPress untouched behind it. Use the mechanics in `route-hosting-panel.md` (file manager, or credentials). Then:

- Check the homepage shows the new site. If WordPress still shows, the server is picking `index.php`: add `DirectoryIndex index.html index.php` to the top of `.htaccess` (explain and ask first; delete the line to undo).
- Existing WordPress pages and blog posts keep working at their old addresses unless the new site uses the same file names. Mention this, and offer to link to the blog from the new site.
- If they have a shop, bookings or a membership plugin, stop and discuss. Replacing the homepage may hide those.

## (b) Keep WordPress, apply the new design

### Rung 1: Invite

Ask them (or the owner, in on-behalf mode) to add a user:

> In WordPress, go to **Users → Add New**. Enter the email, choose the role **Editor** (or **Administrator** if the design needs a new theme or plugin), and tick "Send the new user an email". The person gets an invite and sets their own password.

Editor can create and edit pages. Administrator is needed to install a theme or a page-builder plugin. Ask for the lowest role that works, and remind them at handover to remove the user if this was a one-off.

### Rung 2: They log in, you do it with them

They sign in to `theirdomain.com/wp-admin`. With a browser tool and their permission, create or edit pages yourself. Without one, guide them step by step.

### How to put the design into WordPress

Pick the lightest option that their setup supports:

- **Block editor with Custom HTML blocks.** Paste a section's HTML into a "Custom HTML" block. Put shared CSS in **Appearance → Customize → Additional CSS** (classic themes) or the site editor's custom CSS (block themes). Use a full-width or "blank" page template if the theme offers one, so the theme's header and sidebar don't fight the design. Keep class names prefixed (e.g. `lms-`) so they don't clash with the theme.
- **Recreate with native blocks.** Better for long-term editing by the owner: rebuild each section with Group, Columns, Heading, Image and Button blocks, matching the design's colours and spacing. Slower, but they can change text themselves later.
- **Page builder already installed** (Elementor, Divi, Beaver Builder and similar): use its HTML or code widget for complex sections, its native widgets for the rest.

Always save as **Draft** first, share the preview link, and publish only after they say yes.

### Rung 3: Credentials (repeat updates)

A WordPress **Application Password** lets `scripts/publish_wordpress.py` create and update pages through WordPress's built-in API, with no login screens. Setup steps are in `credentials.md`. Pages are created as drafts unless the person has approved publishing.

## Things to check

- Caching or security plugins can block uploads or hide changes. If changes don't show, look for a "Clear cache" button in the WordPress top bar.
- Hosts with "managed WordPress" sometimes have no file manager. Then (b) is the only route, or ask the host's support.
