# JSON-LD Schema Templates

Copy-paste structured data markup for common page types. Paste inside `<script type="application/ld+json">` in `<head>`.

## Product (for e-commerce product pages)

```json
{
  "@context": "https://schema.org/",
  "@type": "Product",
  "name": "Red Terracotta Cactus Pot",
  "image": "https://example.com/red-cactus-pot.jpg",
  "description": "Handmade terracotta pot perfect for small cacti and succulents.",
  "sku": "PCTO-RED-4IN",
  "brand": {"@type": "Brand", "name": "PlantCo"},
  "offers": {
    "@type": "Offer",
    "url": "https://example.com/products/red-cactus-pot",
    "priceCurrency": "USD",
    "price": "14.99",
    "availability": "https://schema.org/InStock"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.6",
    "reviewCount": "128"
  }
}
```

## Article (for blog posts, news)

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "How to Repot a Cactus Without Getting Stabbed",
  "image": ["https://example.com/repot-cactus-hero.jpg"],
  "datePublished": "2026-03-01T08:00:00+00:00",
  "dateModified": "2026-04-14T10:00:00+00:00",
  "author": {"@type": "Person", "name": "Jane Doe"},
  "publisher": {
    "@type": "Organization",
    "name": "PlantCo",
    "logo": {"@type": "ImageObject", "url": "https://example.com/logo.png"}
  }
}
```

## FAQPage (for pages with Q&A sections)

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "How often should I water a cactus?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Water once every 2-3 weeks in summer, once a month in winter. Always let soil dry completely between waterings."
      }
    },
    {
      "@type": "Question",
      "name": "Can cacti survive indoors?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes, most cacti thrive indoors with bright indirect light. Place near a south-facing window for best results."
      }
    }
  ]
}
```

## Recipe

```json
{
  "@context": "https://schema.org/",
  "@type": "Recipe",
  "name": "Classic Chocolate Chip Cookies",
  "image": "https://example.com/cookies.jpg",
  "author": {"@type": "Person", "name": "Jane Doe"},
  "datePublished": "2026-01-15",
  "recipeYield": "24 cookies",
  "prepTime": "PT15M",
  "cookTime": "PT12M",
  "totalTime": "PT27M",
  "recipeIngredient": [
    "2 cups flour",
    "1 cup butter",
    "1 cup chocolate chips"
  ],
  "recipeInstructions": [
    {"@type": "HowToStep", "text": "Preheat oven to 375°F."},
    {"@type": "HowToStep", "text": "Cream butter and sugar until fluffy."}
  ]
}
```

## Organization (for homepages, about pages)

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "PlantCo",
  "url": "https://example.com",
  "logo": "https://example.com/logo.png",
  "sameAs": [
    "https://facebook.com/plantco",
    "https://instagram.com/plantco",
    "https://twitter.com/plantco"
  ],
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "+1-555-0100",
    "contactType": "Customer Service"
  }
}
```

## LocalBusiness (for brick-and-mortar)

```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "PlantCo Downtown Shop",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "123 Main St",
    "addressLocality": "Portland",
    "addressRegion": "OR",
    "postalCode": "97204",
    "addressCountry": "US"
  },
  "geo": {"@type": "GeoCoordinates", "latitude": 45.515, "longitude": -122.679},
  "openingHours": "Mo-Sa 09:00-18:00",
  "telephone": "+1-555-0100"
}
```

## Validation

Before going live, validate any JSON-LD with:
- https://search.google.com/test/rich-results (Google's official tool)
- https://validator.schema.org (Schema.org's validator)

Both will flag syntax errors and missing required properties.
