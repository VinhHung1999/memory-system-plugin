# One-Thing Focus

## Core Principle
Every product has a single core action that, if the user does it successfully once, dramatically increases their likelihood of returning. All onboarding energy should funnel toward that one thing. Templates, examples, and guided tours that serve multiple purposes simultaneously serve none of them well.

## Diagnostic Questions
- What is the single action that, if a new user completes it in their first session, correlates most strongly with 30-day retention?
- Is the onboarding flow building directly toward that action, or is it teaching users about the product in general?
- Do the templates or sample content provided to new users help them do the one thing, or do they demonstrate the product's breadth?

## Design Checklist
- Identify the core action through retention data and design every onboarding step as a step toward it.
- Remove or defer any feature, tutorial, or prompt that does not contribute to the user completing the core action in the first session.
- Templates given to new users should serve a single purpose: either demonstrate what "good" looks like, or provide a real starting point the user can immediately use.
- Empty states are teaching moments — use them to guide the user toward the core action with a concrete, actionable prompt.
- When a user encounters an edge case (failed scan, search returns no results), turn the failure state into a contextual teaching moment for the core flow.

## Anti-Pattern
**What goes wrong:** A starter template is designed to demonstrate the product's full feature set — it contains instruction cards, example conversations, and upsell cards. It teaches nothing about the user's actual use case and provides no value as a real starting point.
**Why it happens:** Template creation is often done by marketing or product teams who want to showcase capabilities, not by UX teams focused on first-use success.
**BFM Example:** Trello — the default template board mixes instructional cards, fake example conversations, and premium feature upsell cards in the same view. It neither gives the user a clean working environment nor teaches them how to use Trello for their actual project. It serves the company's interest in demonstrating breadth, not the user's interest in getting started.

## BFM Evidence

### Trello — how feature accumulation blurs the one thing
> "As a product builder, you've got an innate desire to promote new features (that you've worked hard on) and to encourage things like referrals. Over time this clouds a team's collective judgement. It makes for a less satisfying experience and creates churn."

### Trello — the template problem: serving two masters
> "Trello attempts to [educate AND provide a starting point] at the same time. Inside the cards themselves are a mixture of instructions, fake conversations and irrelevant activity data. To functionally use the tutorials you need to inherit the cards into a real board. But in doing so, they make the board full of junk and undesirable to clean up."

### Trello — empty search state as a teaching moment
> "Trello pre-populates a search query (that you didn't make), and then predictably fails to find anything. Instead of blocking the user, the right move is to use this distraction as a teaching opportunity — indulge it, then guide them back."

### Trello — zooming in to find the one thing
> "It can help to consider this concept less as a single destination, and more as a direction. Keep zooming until you find it."
*Context: Trello's 'one thing' isn't 'use a kanban board' — it's 'have a task you actually need to do appear on a board you created'.*

### Supermarkets — features and tips can wait
> "Yes, you might have features that you want to talk about. Or tips that you think might help the user. But in this instance, they can wait. Just get them to do the main thing first."

### Supermarkets — contextual teaching beats pre-emptive teaching
> "They'll also tell you what to do if a barcode won't scan. Which should just be explained when it happens."

### Supermarkets — misuse of an empty state as a teaching moment
> "But remember where I am. If I haven't created a shopping list yet, I'm not about to stand here and make one. So why bother telling me where I would find it?"

### Slack — hiding structural decisions to accelerate getting into the product
> "Slack don't want you over-optimising the initial set-up. They want to get you into the product as effortlessly as possible."

## What Good Looks Like
Waitrose's scan-and-go simply opens the camera. No tutorial, no Wi-Fi prompt, no feature tour. The user scans an item, it appears in the basket, and the interface then shows the next logical step. Learning happens through doing the one thing. The only additional information shown is what enables the next step in the same flow — scan, pay, go.

## Red Flags
- [ ] The starter template or example board given to new users contains promotional or upsell content.
- [ ] The onboarding tour visits more than one feature before the user has completed the core action.
- [ ] The empty state shown to a new user describes a feature they cannot use yet (e.g., a shopping list feature shown to someone who is already in the store without a list).
- [ ] Failure or error states during onboarding do not guide the user back to the core action.
- [ ] The onboarding flow teaches how to use the product in general before the user has a specific task in mind.
