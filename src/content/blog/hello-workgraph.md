---
title: "Hello, Workgraph"
description: "Introducing the Workgraph blog — where we'll share project updates, technical deep dives, and the design philosophy behind task coordination for humans and AI agents."
date: 2026-03-17
author: "Workgraph Team"
readTime: "3 min read"
tags: ["announcement"]
---

## Why a blog?

Workgraph is a task coordination graph for humans and AI agents. We've been building it in the open, but the commit log only tells part of the story. This blog is where we'll share the *why* behind the *what*.

## What to expect

We're planning to write about:

- **Design decisions** — why we chose a directed graph (not a DAG), how cycles work, and why we use content-hash IDs for federation.
- **Technical deep dives** — the agency system, evaluation framework, and how agents coordinate without stepping on each other.
- **Project updates** — new features, breaking changes, and roadmap items.

## How it's built

This blog itself is built with [Astro](https://astro.build), a static site generator that ships zero JavaScript by default. Posts are Markdown files with typed frontmatter, styled with Tailwind CSS v4 and the typography plugin.

The site is deployed to GitHub Pages via a GitHub Actions workflow — push to `main` and it builds automatically.

## Get involved

Workgraph is MIT-licensed and open source. If task coordination for humans and AI agents sounds interesting to you:

- Check out the [manual](/workgraph-manual.html) for a full walkthrough
- Read about [organizational patterns](/organizational-patterns.html) for the theory behind the design
- Visit the [GitHub repo](https://github.com/graphwork/workgraph) to browse the code

We're excited to share more here soon.
