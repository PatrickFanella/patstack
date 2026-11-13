# Served-page list

A deployed product page carries the pack when it has:

- an `@font-face` rule for every family the CSS names, with the file present; a `font-family` line alone falls back to system fonts, as it did on Kork, Left Field and Dedhed in November 2026;
- `/favicon.ico` and the pack's 16-pixel favicon, plus the larger icons;
- `<title>`, description, canonical and share tags in the served HTML, rather than only added by JavaScript;
- an absolute `og:image` that returns 200, and an `og:title` that says what the product is;
- `theme-color` for each color scheme the site supports, with the identity in the scheme a first visitor gets;
- a first screen that says what the product is, also when the root opens into the app, a sign-in form or a data table;
- for an archive of someone else's work, a not-endorsed line on the site itself and the pack's own mark in the header.

When the integration changes what the site shows, update the pack's `WEBSITE.md` and its observation date in the same change.
