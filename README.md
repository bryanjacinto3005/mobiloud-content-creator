# MobiLoud Blog Content Workspace

A specialized repository for planning, researching, and producing high-quality, SEO-optimized blog content for MobiLoud. This workspace is designed to be used by both AI agents and human writers to generate publication-ready technical articles with minimal friction.

## Purpose

The goal of this repository is to centralize the brand voice, messaging guidelines, and operational tools required to create content that sounds like MobiLoud. It bridges the gap between raw AI capabilities and the specific nuances of our brand, ensuring every piece of content remains consistent, accurate, and valuable to our audience of founders and ecommerce leaders.

## Setup Guide

Before you can use the AI agents, you need to configure the local environment with the necessary API keys.

### 1. Installation
1.  **Download** the entire repository folder to your local machine.
2.  **Open** the folder in **Cursor Desktop**.

### 2. Configure Environment Secrets
The tools in this repository require access to the DataForSEO API to perform keyword research.

1.  Locate the `.env.example` file in the root directory.
2.  **Duplicate** this file and rename the copy to `.env` (this file is git-ignored to protect your keys).
3.  Open the new `.env` file. You will see fields for `DATAFORSEO_LOGIN` and `DATAFORSEO_PASSWORD`.

### 3. Get DataForSEO Credentials
1.  Log in to the [DataForSEO Dashboard](https://app.dataforseo.com/dashboard).
2.  Navigate to the API Dashboard or API Credentials section.
3.  Copy your **API Login** and **API Password**.
4.  Paste them into your `.env` file:
    ```bash
    DATAFORSEO_LOGIN=your_login_here
    DATAFORSEO_PASSWORD=your_password_here
    ```
5.  Save the file. You are now ready to run the agents.

## How to Use (Slash Commands)

To generate content, simply use one of the custom slash commands in the chat interface. Each command corresponds to a specific content type and triggers the `mobiloud_blog_writer` agent.

### Available Commands

| Command | Content Type | Description |
| :--- | :--- | :--- |
| `/blogpost` | Standard Blog Post | General-purpose technical or educational articles. |
| `/comparison_general` | Comparison (X vs Y) | Compare two external competitors (e.g., "Shopney vs Tapcart"). |
| `/comparison_mobiloud` | Comparison (MobiLoud vs X) | Compare MobiLoud against a competitor (e.g., "MobiLoud vs GoodBarber"). |
| `/listicle` | Listicle | "Top X" lists (e.g., "7 Best Mobile App Builders"). |
| `/use_case` | Use Case | Specialized articles focusing on specific business scenarios. |

### Usage Format

When running a command, please provide the following inputs:

> **Cmd+K** (or Chat) -> `/command_name`
>
> **Title**: [Proposed Title]
> **Word count**: [Target Word Count]
> **Instructions**: [Any specific focus or requirements]

**Example:**
`/blogpost Title: "How to Reduce Churn" Word count: 1500 Instructions: "Focus on Shopify stores"`

## Repository Structure

-   `.cursor/commands/`: **Slash Commands.** Custom commands to trigger specific content workflows (e.g., `/blogpost`, `/listicle`).
-   `agents/`: **AI Instructions.** Contains the master prompt (`mobiloud_blog_writer.md`) that drives the AI content creation workflow.
-   `context/`: **Brand Source of Truth.** Core documentation on MobiLoud's value props, voice, style, and messaging (e.g., `mobiloud_brand_bible.md`, `master_writing_guidelines.md`).
-   `directories/`: **Link Indexes.** Canonical lists of internal links (blogs, integration pages, use cases) to ensure accurate cross-linking.
-   `playbooks/`: **Content Templates.** Specialized step-by-step instructions for specific article types (e.g., Comparisons, Listicles, Use Cases).
-   `structures/`: **Structural Skeletons.** Reusable markdown outlines for different content formats (e.g., `blogpost_structure.md`, `use_case_structure.md`).
-   `reports_assets/`: **Data Sources.** Primary research and reports (e.g., `ecommerce_mobile_apps_report_2025.md`) used for data-driven claims.
-   `tools/`: **Utility Scripts.** Python tools for SEO research (`dataforseo_client.py`), internal linking (`link_finder.py`), and quality checks (`word_counter.py`).
-   `seo_briefs/`: **Research Artifacts.** JSON and Markdown briefs generated during the SEO research phase.
-   `temp_files/`: **Temporary Workspace.** Holds intermediate files (outlines, research notes) during generation. Automatically purged after task completion.
-   `outputs/`: **Drafts.** The destination folder for all final generated content.

## Key Features

-   **Context-Aware**: The `context/` folder ensures that all content adheres to MobiLoud's specific definitions of "native apps," "no-code," and "retention."
-   **Automated Research**: The `tools/dataforseo_client.py` script provides real-time keyword data and competitive intelligence.
-   **Intelligent Linking**: The `tools/link_finder.py` tool helps identify relevant internal linking opportunities from `directories/`.
-   **Structural Consistency**: `structures/` provide consistent H2/H3 scaffolds for every article type.
-   **Strict Verification**: The `tools/word_counter.py` tool enforces word count limits to match Google Docs standards.

## Workflow

This repository is designed for an **AI-first workflow**, driven by the slash commands listed above.

1.  **Trigger**: User initiates the process using a slash command (e.g., `/blogpost`).
2.  **Autonomous Execution**: The `agents/mobiloud_blog_writer.md` agent executes the following pipeline:
    -   **Research**: Runs `tools/dataforseo_client.py` to generate a keyword brief and analyze competitors.
    -   **Plan**: Selects the correct **Playbook** and **Structure** based on the command used.
    -   **Draft**: Writes the full article using `context/` for voice/tone and `directories/` for internal links.
    -   **Verify**: Self-corrects using `tools/word_counter.py` and strictly follows the quality checklists.
3.  **Review**: The agent stops only when it has a publication-ready Markdown file in the `outputs/` folder.
4.  **Cleanup**: Interim files are purged; strategic artifacts (e.g., SEO briefs) are preserved.

### For Developers

-   **Agents**: Update `agents/mobiloud_blog_writer.md` to refine the AI's behavior or add new steps to the workflow.
-   **Tools**: Enhance `tools/` scripts to provide better data or more robust validation logic.
-   **Context**: Keep `directories/` updated as new content is published to the main site.

## Contributing

-   **Content Updates**: When publishing new articles, please update `directories/blog_link_directory.md` so the AI can link to them in future posts.
-   **Rule Changes**: If brand messaging changes, update `context/mobiloud_brand_bible.md` or `context/master_writing_guidelines.md` first.

---
*Internal use only.*
