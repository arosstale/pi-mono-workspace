---
name: browser-use
description: Natural language browser automation - no Playwright scripts needed. Just describe what you want and the AI figures out the clicks.
metadata: {
  "openclaw": {
    "requires": {
      "tools": ["browser"],
      "runtime": "node"
    },
    "tags": ["automation", "scraping", "testing", "data-extraction"]
  }
}
---

# browser-use Skill

## What It Is

Instead of writing Playwright scripts to click specific selectors, just describe what you want to do in natural language. The AI figures out the clicks, interactions, and extraction logic automatically.

## Why It Matters

| Traditional Approach | browser-use |
|---------------------|--------------|
| Write Playwright scripts with selectors | Describe in plain English |
| Breaks when site changes | Handles site layout changes |
| Debugging DOM elements | AI adapts automatically |
| Hours of coding | Minutes to build |

## Core Concept

Instead of this:
```javascript
await page.goto('https://reddit.com/r/openclaw');
await page.click('[data-click-id="text"]');
await page.fill('[name="q"]', 'browser automation');
await page.press('Enter');
```

Just say:
> "Go to r/openclaw on Reddit and search for posts about browser automation"

The AI:
1. Understands the intent
2. Navigates the page
3. Finds the right elements
4. Executes the actions
5. Extracts the data you need

---

## Usage Examples

### Basic Navigation

> "Go to https://example.com"
> "Click on the 'Products' link"
> "Scroll down to the bottom"
> "Go back to the previous page"

### Form Filling

> "Fill in the contact form with name 'John Doe' and email 'john@example.com'"
> "Select 'United States' from the country dropdown"
> "Check the 'I agree' checkbox"

### Data Extraction

> "Extract all product names and prices from this page"
> "Get the title, author, and upvotes from the top 5 Reddit posts"
> "List all email addresses on this page"

### Complex Workflows

> "Go to Reddit, find the top post in r/programming, and extract the title and link"
> "Log into GitHub with my credentials and check the number of open issues"
> "Search Amazon for 'wireless headphones', filter by 4+ stars, and extract top 5 results"

### E-commerce Scraping

> "Go to Amazon, search for 'MacBook Pro M3', and extract prices from the top 10 results"
> "Extract all product names, prices, and ratings from the search results"
> "Add the first item to cart and show me the total price"

### Social Media

> "Go to LinkedIn and search for 'AI Engineer' jobs in San Francisco"
> "Extract the latest tweets from @OpenAI"
> "Get the number of likes and comments on the top post"

---

## Common Tasks

### Job Search

> "Go to LinkedIn Jobs, search for 'Senior Python Developer', filter by 'Remote', and extract company names, job titles, and links to the first 10 results"

### Market Research

> "Go to Product Hunt, find today's top 5 products, and extract their names, descriptions, and upvote counts"

### Content Aggregation

> "Go to Hacker News, get the top 10 stories, and extract titles, URLs, and points"

### Data Entry

> "Go to the CRM dashboard and create a new lead with name, company, and email from this data..."

---

## Advanced Features

### Waiting for Content

> "Wait for the search results to load"
> "Wait until the 'Loading' text disappears"

### Conditional Actions

> "If there's a 'Load More' button, click it and extract more results"

### Error Handling

The AI automatically handles:
- Page navigation failures
- Element not found
- Timeouts
- Dynamic content loading

---

## Best Practices

### Be Specific

Better: "Click the 'Sign In' button in the top right corner"
Good: "Click the sign in button"

### Describe Context

Better: "On the search results page, extract all product names and prices"
Good: "Extract product names and prices"

### Break Down Complex Tasks

For complex workflows, break into steps:
1. "Go to the site and log in"
2. "Navigate to the reports section"
3. "Download the monthly sales report"

---

## Use Cases

### Lead Generation

> "Go to this trade show directory, extract all company names, websites, and booth numbers"

### Price Monitoring

> "Check competitor prices on Amazon and extract product names and current prices"

### Content Research

> "Go to these 5 blog posts and extract the main headlines and key points"

### Testing

> "Go through the checkout flow and verify all pages load correctly"

---

## Under the Hood

browser-use combines:
1. **Browser Control** - OpenClaw's browser tool (Playwright backend)
2. **Natural Language Understanding** - AI interprets your intent
3. **DOM Analysis** - Identifies relevant elements
4. **Adaptive Action Selection** - Chooses right actions based on page state

---

## When to Use browser-use vs Traditional Playwright

### Use browser-use when:
- Task is simple to describe
- Site layout changes frequently
- One-off or prototype automation
- You're not familiar with DOM inspection

### Use traditional Playwright when:
- Performance is critical
- Need exact control over every interaction
- Running the same script thousands of times
- Site requires specific authentication flows

---

## Examples from the Wild

### Reddit Post Extraction

> "Go to r/openclaw and extract the title, author, and upvote count from the top post"

### Job Application Automation

> "Go to the job posting, fill in the application form with my resume data, and submit it"

### Price Comparison

> "Check the price of iPhone 15 on Amazon, Best Buy, and Target, and create a comparison table"

### Social Media Monitoring

> "Check Twitter for mentions of our brand and extract the sentiment and user engagement"

---

## Getting Started

Just use the browser tool in your conversations:

> "browser: Go to https://example.com and..."

The AI will:
1. Navigate to the page
2. Analyze the structure
3. Execute your request
4. Return the results

---

## Limitations

- Not suitable for high-frequency trading or real-time critical systems
- May not work on heavily obfuscated sites
- CAPTCHAs and bot protection may interfere
- Requires browser tool access

---

## Tips for Better Results

1. **Start Simple**: Begin with basic navigation and extraction
2. **Iterate**: Build up complexity step by step
3. **Provide Context**: Mention page state if relevant
4. **Use Natural Language**: Describe what you want, not how to do it

---

*Natural language browser automation - faster, simpler, more resilient* 🌐
