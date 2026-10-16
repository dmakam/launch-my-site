# Style cards: let them pick a look by pointing

Most people can't describe a style, but everyone can point at one they like. Style cards are small, real homepage samples that use **their** business name, headline and main button, each in a clearly different style. They pick one (or mix two), and that becomes the starting point for the two design directions.

## When to show them

- **Always** if they answered "no idea" (or didn't answer) to "Any websites you like the look of?"
- **Optionally** alongside their references, to check a direction: "Is it closer to 1 or 3?"
- Not needed if they sent clear references *and* a logo with colours. Build the directions straight from those.

## How to make them

```
python scripts/style_cards.py --name "Maria's Bakery" \
  --tagline "Fresh bread every morning, baked in Oak Park" \
  --cta "Order for pickup" --industry "Bakery · Oak Park" --out style-cards/
```

- `--tagline` is a short headline in their own words from the interview, not a slogan you invented.
- `--cta` is their main button from the interview ("Call 555-0100", "Book a table").
- Default styles: `clean, bold, warm, classic`. Use `--styles` to show 3 if one is clearly wrong for the business.
- Output: `style-cards.png` (the 2×2 sheet to send), one PNG per style, and the HTML files.

Send `style-cards.png` as an image in the chat. Never describe the styles in words only.

## The four styles

| # | Style | Looks like | Often fits |
|---|---|---|---|
| 1 | Clean & bright | White and light blue, rounded buttons, soft glow | Health, home services, professional services, tech |
| 2 | Bold & dark | Dark background, very large type, bright accent button | Trades that want to stand out, gyms, events, auto |
| 3 | Warm & local | Cream and terracotta, friendly serif | Food, bakeries, cafes, florists, family businesses |
| 4 | Classic & formal | Navy and gold, traditional serif | Law, finance, real estate, established firms |

"Often fits" is a hint for which to list first, not a rule. Always show all of them unless one is clearly wrong.

## How to ask

> Here are four quick style samples with your name on them. Which one feels most like your business? You can also mix them, like "the colours of 3 with the big text of 2." Your real words and photos go in later.

## Reading their answer

- **A number:** use it as the base for both directions, and vary one thing between them (light vs dark, or rounded vs sharp).
- **A mix** ("3's colours, 2's headline"): direction A is the literal mix; direction B pushes it one step further.
- **"None of these":** ask what's off in one question ("Too plain? Too dark? Not 'you'?") and render a second set.
- **Personal details count.** "My truck is red", "we wear navy uniforms" are colour specs. Use them.

## Rules

- Samples carry only the business name, their headline and their button. No invented claims, reviews, years in business or licence numbers.
- No stock photos of people in samples. Shapes, gradients and type only.
- If they have a logo, don't put a redrawn version into the samples. Use the plain business name; the real logo goes into the directions.
