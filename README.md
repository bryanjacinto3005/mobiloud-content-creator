# MobiLoud Blog Content Workspace

A specialized repository for planning, researching, and producing high-quality, SEO-optimized blog content for MobiLoud. This workspace is designed to be used by both AI agents and human writers to generate publication-ready technical articles with minimal friction.

## Purpose

The goal of this repository is to centralize the brand voice, messaging guidelines, and operational tools required to create content that sounds like MobiLoud. It bridges the gap between raw AI capabilities and the specific nuances of our brand, ensuring every piece of content remains consistent, accurate, and valuable to our audience of founders and ecommerce leaders.

## Repository Structure

-   `agents/`: **AI Instructions.** Contains the master prompt (`blog_writer_agent.md`) that drives the AI content creation workflow.
-   `context/`: **Brand Source of Truth.** Core documentation on MobiLoud's value props, voice, style, and messaging.
-   `directories/`: **Link Indexes.** Canonical lists of internal links (blogs, use cases, docs) to ensure accurate cross-linking.
-   `playbooks/`: **Content Templates.** specialized instructions for specific article types (e.g., Comparison Articles).
-   `tools/`: **Utility Scripts.** Python tools for SEO research (`dataforseo_client.py`) and quality checks (`word_counter.py`).
-   `seo_briefs/`: **Research Artifacts.** JSON and Markdown briefs generated during the SEO research phase.
-   `outputs/`: **Drafts.** The destination folder for all generated content. |

## Key Features

-   **Context-Aware**: The `context/` folder ensures that all content adheres to MobiLoud's specific definitions of "native apps," "no-code," and "retention."
-   **Automated Research**: The `tools/dataforseo_client.py` script provides real-time keyword data and competitive intelligence.
-   **Strict verification**: The `tools/word_counter.py` tool enforces word count limits to match Google Docs standards.
-   **Structured Workflows**: `playbooks/` guide the creation of complex article types like "Alternative" comparisons, ensuring fairness and depth.

## Getting Started

### Prerequisites

-   Python 3.x
-   pip (Python package installer)

### Setup

1.  Clone the repository.
2.  Install any required dependencies for the tools (e.g., `requests` for the SEO client):
    ```bash
    pip install requests
    ```
3.  Ensure your `.env` file is configured with necessary API keys (if applicable for `dataforseo_client.py`).

## Workflow

## Workflow

This repository is designed for an **AI-first workflow**. The `agents/blog_writer_agent.md` file contains a sophisticated prompt that drives the entire content creation process from end to end.

### How to Use

1.  **Provide Input**: Open your IDE or chat interface and instruct the AI (e.g., "Write a comparison article for MobiLoud vs Shopney").
2.  **Autonomous Execution**: The agent will automatically:
    -   **Research**: Run `tools/dataforseo_client.py` to generate a keyword brief and analyze competitors.
    -   **Plan**: Select the correct **Playbook** (e.g., `playbooks/comparison_article_with_mobiloud.md`) and draft an outline.
    -   **Draft**: Write the full article using `context/` for voice/tone and `directories/` for internal links.
    -   **Verify**: Self-correct using `tools/word_counter.py` and strict quality checklists.
3.  **Review**: The agent stops only when it has a publication-ready Markdown file in the `outputs/` folder for you to review.

### For Developers

-   **Agents**: Update `agents/blog_writer_agent.md` to refine the AI's behavior or add new steps to the workflow.
-   **Tools**: Enhance `tools/` scripts to provide better data or more robust validation logic.
-   **Context**: Keep `directories/` updated as new content is published to the main site.

## Contributing

-   **Content Updates**: When publishing new articles, please update `directories/blog_link_directory.md` so the AI can link to them in future posts.
-   **Rule Changes**: If brand messaging changes, update `context/messaging.md` and `context/brand.md` first.

---
*Internal use only.*
