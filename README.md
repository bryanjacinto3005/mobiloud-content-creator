# MobiLoud Blog Content Workspace

A specialized repository for planning, researching, and producing high-quality, SEO-optimized blog content for MobiLoud. This workspace is designed to be used by both AI agents and human writers to generate publication-ready technical articles with minimal friction.

## Purpose

The goal of this repository is to centralize the brand voice, messaging guidelines, and operational tools required to create content that sounds like MobiLoud. It bridges the gap between raw AI capabilities and the specific nuances of our brand, ensuring every piece of content remains consistent, accurate, and valuable to our audience of founders and ecommerce leaders.

## Repository Structure

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

This repository is designed for an **AI-first workflow**. The `agents/mobiloud_blog_writer.md` file contains a sophisticated prompt that drives the entire content creation process from end to end.

### How to Use

1.  **Provide Input**: Open your IDE or chat interface and instruct the AI (e.g., "Write a comparison article for MobiLoud vs Shopney").
2.  **Autonomous Execution**: The agent will automatically:
    -   **Research**: Run `tools/dataforseo_client.py` to generate a keyword brief and analyze competitors.
    -   **Plan**: Select the correct **Playbook** (e.g., `playbooks/comparison_article_with_mobiloud.md`) and **Structure** (e.g., `structures/blogpost_structure.md`).
    -   **Draft**: Write the full article using `context/` for voice/tone and `directories/` for internal links.
    -   **Verify**: Self-correct using `tools/word_counter.py` and strict quality checklists.
3.  **Review**: The agent stops only when it has a publication-ready Markdown file in the `outputs/` folder for you to review.
4.  **Cleanup**: Temporary files are stored in `temp_files/` during the process and are purged upon completion. Strategic artifacts like SEO briefs are preserved.

### For Developers

-   **Agents**: Update `agents/mobiloud_blog_writer.md` to refine the AI's behavior or add new steps to the workflow.
-   **Tools**: Enhance `tools/` scripts to provide better data or more robust validation logic.
-   **Context**: Keep `directories/` updated as new content is published to the main site.

## Contributing

-   **Content Updates**: When publishing new articles, please update `directories/blog_link_directory.md` so the AI can link to them in future posts.
-   **Rule Changes**: If brand messaging changes, update `context/mobiloud_brand_bible.md` or `context/master_writing_guidelines.md` first.

---
*Internal use only.*
