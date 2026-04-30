# Notification Fatigue

## Core Principle
Every non-urgent notification trains users to ignore all notifications. Over-notification is a form of accidental churn — users don't delete the app, they mute it, and a muted app is functionally churned. The inverse is also true: apps that earn notification trust (by sending only genuinely time-sensitive alerts) retain the ability to re-engage users at critical moments.

## Diagnostic Questions
- What percentage of your push notifications are genuinely time-sensitive vs. informational?
- Do users' notification open rates decrease month-over-month?
- Is there a correlation between notification volume and app mute/uninstall rates?
- Are you using notification-style UI elements (red badges, banners) for non-urgent content within the app?

## Design Checklist
- Reserve push notifications for genuinely time-sensitive events only (price drops, deadlines, social responses)
- Treat in-app notification banners with the same discipline as push notifications — overuse kills trust
- Milestone notifications ("you've reached 50% of your goal!") should feel earned, not automated-spam
- Give users fine-grained notification controls — not just on/off, but by category
- Audit your notification taxonomy: what is genuinely urgent vs. what is promotional noise dressed as urgency?

## Anti-Pattern
**What goes wrong:** Engagement team adds more notification types to boost DAU. Open rates rise briefly, then fall below baseline as users start muting or ignoring all alerts. A valuable time-sensitive notification (flash sale, expiring offer) gets ignored because users have trained themselves not to open this app's notifications.
**Why it happens:** Short-term DAU metrics improve with more notifications. The downstream effect (mute rate, notification opt-out, reduced trust) is harder to attribute and often measured separately.
**BFM Example (LinkedIn):** LinkedIn uses urgent-looking in-app banners (the diamond icon array) for content that is almost never urgent — privacy settings changes, generic recommendations. Users learn to dismiss them reflexively, which means the same visual treatment fails when used for actually important alerts.

## BFM Evidence

### LinkedIn — non-urgent notifications trained to be ignored
> "Annoyingly, LinkedIn use notifications like this all the time. And they're almost never urgent."

The context: LinkedIn fires prominent blue notification banners (the same visual style used for genuine alerts) for things like "You can control who can see your profile fields." These are informational, not time-sensitive.

### LinkedIn — milestone notifications do work, but only when genuinely earned
> "These milestones encourage habit-forming behaviour. (i.e., they reduce churn)."

The contrast: a notification that fires when a user reaches their profile completion milestone is meaningful — it's tied to something the user did. A notification about a settings reorganisation is not.

### LinkedIn — notification fatigue compounds through volume
> "Oh, they obviously, throw in a notification for good measure."

The observation: LinkedIn treats notifications as a default tool for any communication, regardless of urgency. The cumulative effect is users who skim or ignore every notification from the app.

## What Good Looks Like
An app that notifies only when the user would genuinely want to know right now. Price drop on a tracked flight. A friend replied to your post. Your streak is at risk. These earn notification opens. The app that sends "10 people viewed your profile this week" 52 weeks a year eventually gets muted.

## Red Flags
- [ ] Using notification-style UI (badges, banners) for content that is not time-sensitive
- [ ] All notification categories are on by default with no easy way to tune by type
- [ ] Notification volume has increased quarter-over-quarter to boost DAU
- [ ] The same visual treatment is used for urgent and non-urgent alerts
- [ ] No measurement of notification mute rate or opt-out rate as a leading churn indicator
