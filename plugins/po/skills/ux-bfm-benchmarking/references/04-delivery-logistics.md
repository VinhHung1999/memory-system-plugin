# Delivery & Logistics Benchmarking

## Core Principle
Parcel delivery apps are used at moments of specific anxiety: "where is my package, and when exactly will it arrive?" The quality of the delivery UX is almost entirely determined by how well it answers these two questions — not by the richness of the feature set. BFM's parcel study (UX of Parcels) benchmarks UPS, FedEx, Royal Mail, and DPD across the core delivery tracking experience.

## Key Benchmarks

### Tracking Status Language
The task: understand what "In Transit" or "Out for Delivery" means for the user's specific situation.

**Best practice:** Time-specific language ("arriving between 14:00 and 16:00") rather than status language ("Out for Delivery"). The delivery window tells the user whether to wait or go about their day. The status label tells them nothing actionable.

**BFM observation (UX of Parcels):**
> "Shipping cost confusion, delivery uncertainty, poor error handling, multi-carrier fragmentation"

The fragmentation problem: a user who shops on Amazon, eBay, ASOS, and a small brand may track through Amazon Logistics, Royal Mail, DPD, and Evri — four different tracking interfaces. No industry-standard tracking experience exists.

### Delivery Notification Timing
When should a user receive a delivery notification?

Best practice sequence:
1. "Your parcel is out for delivery today" — morning of delivery
2. "Your driver is 3 stops away" — day of delivery, ~30-60 mins before
3. "Your parcel has been delivered" — at delivery, with photo

**Common failure:** Single notification at dispatch ("your parcel has been shipped") with no follow-up until delivered — sometimes days later. The user has no information during the interval.

### Failed Delivery Recovery
The moment a delivery is missed is the highest-anxiety moment in the parcel tracking experience. The quality of the recovery UX determines whether the user trusts the carrier for future deliveries.

Best practice: automated rescheduling link in the failed delivery notification, with 3 available windows clearly shown.

Failure mode: "Your parcel is at the depot. Contact your local depot." with no link, phone number, or rescheduling option.

### Multi-Carrier Problem
> "Multi-carrier fragmentation" — BFM's UX of Parcels study identifies that no single tracking experience handles parcels from multiple carriers. The user must manage tracking across multiple apps, emails, and SMS threads.

The opportunity: a unified parcel tracking layer (which Apple Maps, Google, and some email clients partially provide) that extracts tracking numbers from email and surfaces them in one interface.

## BFM Evidence

### UX of Parcels — core failure categories
> "Key findings: Shipping cost confusion, delivery uncertainty, poor error handling, multi-carrier fragmentation"

1. **Shipping cost confusion**: free shipping offers with thresholds obscure the real cost of shipping until checkout
2. **Delivery uncertainty**: tracking status is status-based ("processing") not time-based ("arriving Tuesday 14:00-16:00")
3. **Poor error handling**: failed delivery recovery requires manual contact rather than automated rescheduling
4. **Multi-carrier fragmentation**: no unified tracking experience across carriers

## What Good Looks Like
A carrier tracking experience that provides time-specific delivery windows (not just status labels), proactive same-day notifications with driver proximity updates, automated rescheduling on failed delivery, and — ideally — integration with the user's email or calendar so tracking numbers are automatically surfaced without requiring the user to actively check.

## Red Flags
- [ ] Tracking status uses labels ("Out for Delivery") not time windows ("Arriving 14:00-16:00")
- [ ] No same-day delivery notification with driver proximity
- [ ] Failed delivery recovery requires phone call or manual rescheduling
- [ ] Tracking link requires creating an account or installing an app
- [ ] Tracking updates are email-only, with no push notification option
