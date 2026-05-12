---
title: "Hello, wg"
description: "Introducing the wg blog — where we'll share project updates, technical deep dives, and the design philosophy behind task coordination for humans and AI agents."
date: 2026-03-17
author: "wg Team"
readTime: "5 min read"
tags: ["announcement"]
---

## Why a blog?

wg is a task coordination graph for humans and AI agents. We've been building it in the open, but the commit log only tells part of the story. This blog is where we'll share the *why* behind the *what*.

> Building software with AI agents isn't just about writing code faster — it's about coordinating work across multiple minds, both human and artificial, without losing coherence.

## What to expect

We're planning to write about:

- **Design decisions** — why we chose a directed graph (not a DAG), how cycles work, and why we use content-hash IDs for federation.
- **Technical deep dives** — the agency system, evaluation framework, and how agents coordinate without stepping on each other.
- **Project updates** — new features, breaking changes, and roadmap items.

## How it's built

This blog itself is built with [Astro](https://astro.build), a static site generator that ships zero JavaScript by default. Posts are Markdown files with typed frontmatter, styled with Tailwind CSS v4 and the typography plugin.

The site is deployed to GitHub Pages via a GitHub Actions workflow — push to `main` and it builds automatically.

### The stack

Here's what we're using:

```
astro        — static site generator
tailwindcss  — utility-first CSS
inter        — body typeface
shiki        — syntax highlighting
```

Configuration is minimal. The Astro config handles Tailwind integration, sitemap generation, and Markdown processing:

```javascript
export default defineConfig({
  site: 'https://graphwork.github.io',
  integrations: [sitemap()],
  markdown: {
    rehypePlugins: ['rehype-slug', 'rehype-autolink-headings'],
    shikiConfig: { theme: 'github-dark' },
  },
});
```

### Design philosophy

We wanted the blog to feel like reading — not like using a web app. That means:

1. Zero client-side JavaScript for rendering
2. Deep black background for reduced eye strain
3. Generous line spacing and constrained prose width
4. A sticky table of contents for longer posts

> The best interface is the one that gets out of your way. For reading, that means clean typography, high contrast, and nothing that moves unless you ask it to.

## Get involved

wg is MIT-licensed and open source. If task coordination for humans and AI agents sounds interesting to you:

- Check out the [manual](/wg-manual.html) for a full walkthrough
- Read about [organizational patterns](/organizational-patterns.html) for the theory behind the design
- Visit the [GitHub repo](https://github.com/graphwork/wg) to browse the code

We're excited to share more here soon.
