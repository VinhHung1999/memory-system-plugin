# BFM Benchmark Methodology

## How to Run a BFM-Style Benchmark

BFM benchmarks are task-based, not feature-based. The goal is to compare how competing products handle the same user need — not to count features or measure design aesthetics.

## Step 1: Define the Task Basket

A task basket is 15-30 specific tasks that represent the core user needs in the category. Each task must be:
- **Specific**: "Send £100 to an overseas payee for the first time" not "make a payment"
- **Reproducible**: any tester can perform the same task without ambiguity
- **User-goal-oriented**: describes what the user wants to accomplish, not what UI to interact with

**BFM Example (PS5 vs Xbox):**
> "A basket of 30 common tasks across 3 categories with recorded datapoints"

The 30-task basket covered 3 categories of console UX: setup and account creation, core gaming tasks, and media/streaming tasks. Each task was scored independently.

**BFM Example (Opening 12 Bank Accounts):**
The study opened accounts at 12 UK banks using the same personal details and device. Each account opening was scored on: time to complete, number of steps, information required, and first-session experience quality.

## Step 2: Define the Scoring Dimensions

For each task, score on 3-5 specific dimensions — not overall impression. Example dimensions:
- **Steps to complete**: how many taps/clicks from starting state to task completion
- **Information required**: how much the user must provide (vs. what the app could infer)
- **Error recovery**: what happens when something goes wrong mid-task
- **Time to completion**: wall-clock seconds from task start to task end

The dimensions should be objective enough that two different testers score the same task the same way.

## Step 3: Run the Same Task on All Products

Same device, same network, same starting state. If one product requires login, all products are tested logged in. If one product is tested fresh install, all products are tested fresh install.

**Key discipline:** Do not add new tasks to "show off" a product's best feature. The task basket is fixed before testing begins.

## Step 4: Find the Outlier

The goal of a benchmark is not to produce an average — it is to find the outlier in each dimension. The outlier is the insight:
- Which product completes this task in the fewest steps?
- Which product has the worst error recovery on this task?
- Where does the best product diverge from the industry norm?

**BFM framing:** "One product always does something meaningfully better or worse. That's the insight."

## Step 5: Distinguish Norm from Best

A finding like "all 6 banks require the user to re-enter payee details on each international payment" is a norm finding — the industry standard is bad. A finding like "Monzo's notification format is 3x more readable than the industry average" is a best-in-class finding.

Both are valuable. The norm finding identifies an industry-wide opportunity. The best-in-class finding identifies the target to aim for.

## Common Benchmarking Mistakes

**Mistake 1: Feature counting**
Counting how many features a product has produces a list, not an insight. A product with 20 features may deliver a worse core task experience than a product with 10.

**Mistake 2: Using power user tasks**
Benchmarking on advanced tasks (export to CSV, configure API keys) tells you about the experience for 5% of users. Benchmark on the tasks that 80% of users need.

**Mistake 3: Snapshot bias**
A benchmark is a snapshot. Products are updated weekly. Publish with a date; revisit annually.

**Mistake 4: Not scoring failure states**
How a product handles errors is as important as how it handles success. A benchmark that only tests the happy path misses half the experience.

## BFM Evidence

### Opening 12 Bank Accounts — methodology as the finding
The act of opening 12 accounts with identical details at 12 different banks revealed: account opening time ranged from 3 minutes (Monzo) to 45+ minutes (legacy banks); information required varied from email + ID photo to in-person branch visit; and first-session experience quality — what happens in the first 5 minutes after account opening — varied from personalised onboarding to a blank account with no guidance.

The methodology itself is the point: doing the same thing 12 times in a row makes the differences impossible to rationalise as "just different choices" — they become visible quality gaps.

### Maps — preference vs. usage benchmark
> "Google Maps vs Apple Maps preference data and usage comparison"

The maps benchmark reveals a consistent pattern: user preference (which app they prefer) does not always match usage frequency (which app they actually use). This gap — between stated preference and actual behaviour — is only visible through a task-based benchmark, not a survey.
