# Structure

## Intros and Narrative Flow

- **Rich and Custom Introductions**:
  - **Length**: 180 - 220 words.
  - **Content**: Include stats if possible, but **avoid generic mobile statistics** or overused hooks.
  - **Customization**: Understand the article deeply to create a custom intro. Look for stats or hooks that are **exclusive** to the article's specific topic.
  - **Avoid**: Repetitive introductions about general mobile app usage.
  - **Word Count Verification**:
    - **REQUIRED**: Use the `tools/word_counter.py` script to verify the exact word count of the introduction.
    - **Method**: Save the introduction text to a temporary markdown file and run: `python tools/word_counter.py temp_intro.md`.
    - If the word count is below 180 words, add content to reach the minimum requirement.
    - If the word count is above 220 words, trim content to meet the maximum requirement.
    - Continue rewriting and verifying until the introduction falls within the 180-220 word range.
    - Make sure to delete the temporary intro file once you have verified that the word count requirements are satisfied.
- **Ending the Introduction**:
  - Include a **soft CTA** (e.g., "in this guide...", "in this post, we will tackle...").
  - **Uniqueness**: Never default to a single approach for the last line. The agent must come up with a unique transition/CTA for each article.
- Standard section flow:
  1. State the problem or tension.
  2. Explain why it matters for the reader.
  3. Show how the solution works, with specifics.
  4. End with a clear takeaway or recommended action.

## Headings and Subheadings

- Make subheads meaningful on their own:
  - Bad: "Refund Policy Guidelines."
  - Good: "Refunds Are Protection."
- Treat subheads like mini takeaways:
  - A reader should be able to skim headings and understand the main argument.
  - Keep paragraphs short and punchy, but still connected to the next paragraph.
- **Heading Hierarchy**:
  - **No H2 to H3 jumps**: Do not go straight from an H2 to an H3.
  - **Introductory Text**: Always include some text (e.g., a paragraph) beneath an H2 before starting an H3 subsection.

## Paragraphs, Spacing, Lists, and Emphasis

### Paragraphs and Flow

Use paragraph form for narrative flow, explanations, and connecting ideas. Paragraphs feel conversational and keep the reader moving through the story.

- Keep paragraphs short: roughly 2–4 lines.
- Use transitions and connectors to maintain narrative momentum.

### Lists and Bullet Points

**CRITICAL: Bullet points are MANDATORY for certain content types. Use them explicitly and generously.**

#### When Bullet Points Are REQUIRED

Default to bullet points whenever you are listing or describing:

1. **Features or capabilities** (platform features, tool capabilities, app functionalities)
   - Example: Instead of "Klaviyo offers segmentation, automation, A/B testing, and revenue attribution" → Use bullets
   
2. **Benefits or advantages** (why something matters, what you gain)
   - Example: Instead of "Apps drive retention, increase AOV, and improve LTV" → Use bullets

3. **Steps or processes** (how to do something, sequential actions)
   - Example: Any "how to" content or numbered workflows

4. **Comparison points** (when contrasting two or more options)
   - Example: "Choose X if:" sections MUST use bullets

5. **Sets of related items** (integrations, tools, platforms, examples)
   - Example: Instead of "It integrates with Shopify, WooCommerce, and BigCommerce" → Use bullets if listing 3+ items

6. **Technical specifications** (pricing tiers, plan details, limits)
   - Example: Free plan details, pricing breakdowns

7. **Multiple attributes or characteristics** (when describing something with 3+ traits)
   - Example: Instead of "The platform is affordable, easy to use, and well-supported" → Use bullets

#### Before/After Examples

**❌ WRONG (Dense Prose):**
> Klaviyo's segmentation engine lets you build audiences with surgical precision. You can target customers based on browsing behavior, purchase frequency, cart value, location, engagement history, and dozens of other attributes.

**✅ CORRECT (Scannable Bullets):**
> Klaviyo's segmentation is surgical. Target customers by:
> - Browsing behavior
> - Purchase frequency
> - Cart value
> - Location and demographics
> - Engagement history
> - Dozens of other custom attributes

**❌ WRONG (List in Paragraph):**
> Omnisend includes product pickers that let you add dynamic product recommendations directly into emails. You can insert unique discount codes, countdown timers, and gift boxes without custom coding.

**✅ CORRECT (Feature Bullets):**
> Omnisend includes ecommerce-specific features:
> - Product pickers for dynamic recommendations
> - Unique discount codes (auto-generated)
> - Countdown timers
> - Gift box elements
> - No custom coding required

#### Bullet Point Rules

1. **Use bullets liberally** - When in doubt, use bullets. They improve scannability and rarely hurt readability.

2. **Keep bullet items concise** - Each bullet should be scannable at a glance (5-12 words ideal, max 20).

3. **Parallel structure** - Start bullets with the same grammatical structure (all verbs, all nouns, etc.).

4. **No nested mega-bullets** - Avoid sub-bullets unless absolutely necessary. Keep it simple.

5. **Introduce with context** - Add a short lead-in sentence before bullet lists (e.g., "Klaviyo excels at:").

6. **Balance with prose** - Not EVERY paragraph should be bullets. Use them for lists/features; use prose for narrative, transitions, and explanations.

#### Mandatory Pre-Publish Bullet Point Checklist

Before finalizing any article, scan for these patterns and convert to bullets:

- [ ] Any sentence listing 3+ items with "and" or commas → Convert to bullets
- [ ] Any "Choose X if you..." section → MUST be bullets
- [ ] Any feature description with multiple capabilities → Convert to bullets
- [ ] Any comparison of 3+ attributes → Convert to bullets
- [ ] Any pricing or plan details → Convert to bullets
- [ ] Any paragraph longer than 6 lines that lists things → Break into bullets

**Exception: Key Takeaways** - This section must remain pure paragraph form (no bullets).

### Emphasis

- Use bold sparingly.
- Do not bold every bullet or sentence.
- Reserve bold for key terms, important warnings, or critical takeaways.

## Default Blog Post Structure

Use this as the standard layout for long-form blog articles.

Meta Title: [SEO-optimized meta title]

Meta Description: [SEO-optimized meta description]

URL Slug: [seo-optimized-url-slug]

---

# [Main Article Title]

## Key Takeaways  
[1 short paragraph, max 3 sentences, summarizing the entire article. Light, low-key mention of MobiLoud in context without being pushy, still focused on the overall takeaway of the article. Strictly no bullet points, pure paragraph in the key takeaways section. Keep the heading title as Key Takeaways]

---

## Introduction  
[180 - 210 words. Rich, custom introduction with specific, exclusive stats/hooks (no generic mobile stats). End with a unique soft CTA tailored to the article. Keep the heading title as Introduction]

---

## [H2 Heading 1]  
[Main point or section idea.]

### [H3 Subheading 1]  
[Supporting detail or subtopic.]

### [H3 Subheading 2]  
[Supporting detail or subtopic.]

[Add more H3 sections as needed following the same pattern.]

---

## [H2 Heading 2]  
[Next main point or section idea.]

### [H3 Subheading 1]  
[Supporting detail or subtopic.]

### [H3 Subheading 2]  
[Supporting detail or subtopic.]

[Add more H3 sections as needed following the same pattern.]
---

## [H2 Heading 3]  
[Next main point or section idea.]

### [H3 Subheading 1]  
[Supporting detail or subtopic.]

### [H3 Subheading 2]  
[Supporting detail or subtopic.]

[Add more H3 sections as needed following the same pattern.]

---

[Add more H2 sections and H3 sections as needed following the same pattern.]

## Table Placement

**Tables should appear in the middle or bottom portions of articles, NOT at the very beginning.**

- **Reasoning**: Tables work best after you've established context and narrative flow. Readers need to understand the topic before comparing options or reviewing data.
- **Best Practice**: Place tables after at least 1-2 H2 sections of content that explain the topic, establish the problem, and provide necessary context.
- **Avoid**: Putting tables immediately after the introduction or in the first major section of the article.

When you include a head-to-head comparison table (for example, "Hybrid App vs Website-to-App Service"), add a short, plain-language bridge paragraph immediately before the table that sums up the core difference in one or two sentences. The goal is to make the difference crystal clear for skimmers before they look at rows and columns. Also add a descriptive heading title for the table.

---

## Final Thoughts  
[Summarize the article and close the main discussion.]  
[Start discussing how MobiLoud can help in the context of the article.]  
[End with a clear CTA, such as inviting readers to book a demo or request a preview for Mobiloud's service.]

---

## FAQs  

**FAQ Writing Rules:**
- **Be concise and direct.** Answer exactly what the question asks with minimal words.
- **No walls of text.** Keep answers short - typically 2-4 sentences maximum.
- **Get straight to the point.** Don't add unnecessary context, background, or elaboration.
- **One answer per question.** Don't turn a FAQ into a mini-article.
- Strictly no hyperlinks

### [FAQ 1 Question]  
[FAQ 1 Answer.]

### [FAQ 2 Question]  
[FAQ 2 Answer.]

### [FAQ 3 Question]  
[FAQ 3 Answer.]

### [FAQ 4 Question]  
[FAQ 4 Answer.]

### [FAQ 5 Question]  
[FAQ 5 Answer.]
