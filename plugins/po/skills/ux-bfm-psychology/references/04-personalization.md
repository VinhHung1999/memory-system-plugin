# Personalization

## Core Principle
Real personalization changes the outcome for the user. Cosmetic personalization — using a name, showing a greeting — changes only the surface and rarely influences behaviour. The difference is whether the user's input actually filtered or reordered what they see. When genuine personalization is technically limited, the experience of being considered carefully matters as much as the accuracy of the result.

## Diagnostic Questions
- Does the user's input actually change what they see, or is it collected and ignored?
- Is the recommended result believable as personalised — or does it look like the most expensive or most popular option by default?
- If the user's explicit preference (size, gender, goal) is ignored in recommendations, does the recommendation surface feel trustworthy?

## Design Checklist
- If you ask for a preference, use it — recommendations that ignore explicit input destroy trust faster than no recommendation at all
- When the algorithm has limited personalisation power, use animation and process to sell the *experience* of being considered
- Show the user their input is doing something — cycle through options visually before settling on a result
- Frame each feature or recommendation through the lens of the user's stated goal, not as a generic feature
- "Good afternoon, [name]" is not personalisation — collect data only if you will actually use it in the experience

## Anti-Pattern
**What goes wrong:** A personalisation quiz asks for multiple user preferences, then the recommendation engine returns the same result regardless of what the user selected — typically the bestseller or highest-margin item.
**Why it happens:** Engineering constraints mean the quiz data is not wired to the recommendation logic, or the product catalog is too small to differentiate. The quiz is added as a UX layer without backend integration.
**BFM Example:** Nike — the "Top Picks for You" section recommended pink baby Jordans to a male user who had explicitly favourited a men's running top. The Running Shoe Finder quiz included questions ("How far will you race?") that had no impact on the outcome according to the API response. The algorithm was not using the answers.

## BFM Evidence
### Nike — cosmetic personalisation is the easy, ineffective thing
> "This type of personalisation is so common that most people just assume it must work. So then, why do people obsess about this? Because it's easy. This isn't how you craft personalised experiences."

### Nike — explicit input ignored in recommendations
> "I added a men's running top to my favourites. And what do they suggest to me? A pair of pink baby Jordans."

### Nike — the quiz may be showmanship
> "I wanted to see if this was technically doing anything. Or if it was all showmanship. The truth is; some of the questions make no difference. i.e., they may ask how far you're running in a race — despite that question having no impact on the outcome."

### Nike — the animation sells the illusion of consideration
> "These animations are psychologically very important. They demonstrate the effort required to filter through a broad range of options. The key is that you need to sell the illusion of the personalisation. Regardless of what technically happens, the experience sells you on the idea that this is personalised to you."

### Monzo Perks — features without personal context feel irrelevant
> "Assume that the user doesn't perceive any of these perks as solving an immediate or acute problem. And, they might not even stumble across these features naturally in the app."

### Monzo Perks — goals collected, then ignored
> "The user then literally selects what they want to happen. And Monzo takes this absolutely invaluable context... and does basically nothing with it."

## What Good Looks Like
Nike's Running Shoe Finder — even if the backend is limited, the animation of dozens of shoes being sorted, then two halves closing in on a single result, then a beautiful transition to a comparison screen makes the user feel that something rigorous just happened on their behalf. The *experience* of personalisation is delivered even when the data pipeline isn't perfect.

## Red Flags
- [ ] Personalisation data (name, preferences, goals) is collected but not reflected in the content shown
- [ ] The primary recommendation is the same for all users regardless of quiz input
- [ ] Recommendations contradict the user's explicit stated preference (gender, size, goal)
- [ ] Features are introduced with generic copy rather than reframed for the user's selected goal
- [ ] No animation, progress indicator, or process ritual separates "input" from "result"
