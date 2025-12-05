# GPT-5.1 Prompt Optimization Summary

## Overview

This document outlines the improvements made to `prompt_gpt5_optimized.txt` based on ground truth translation examples across 7 languages (German, Spanish, Serbian, Slovenian, Italian, Bulgarian, Hungarian).

## Key Ground Truth Patterns Identified

### 1. Idiomatic Adaptation Over Literal Translation

**Pattern:** The best translations adapt concepts idiomatically rather than translating word-for-word.

Example: "No-Bullshit-Casino"
- 🇩🇪 German: "Kein-Bullshit-Casino" (keeps loanword naturally)
- 🇪🇸 Spanish: "Casino sin rodeos" (idiom: no beating around the bush)
- 🇮🇹 Italian: "Casino senza fregature" (without scams/rip-offs)
- 🇭🇺 Hungarian: "Kaszinó kamu nélkül" (without fake stuff)

**Implementation:** Added explicit guidance to "prioritize idiomatic naturalness over literal accuracy" with these examples in the `<marketing_headlines>` section.

### 2. Ultra-Concise UI Text

**Pattern:** UI elements use the shortest natural form, often single words.

Examples:
- "All" → "Alle" (DE), "Todos" (ES), "Tutti" (IT), "Sve" (SR), "Vse" (SL), "Mind" (HU)
- "Games" → "Spiele" (DE), "Juegos" (ES), "Igre" (SR), "Giochi" (IT)

**Implementation:** Enhanced `<ui_elements>` section with explicit "think mobile-first" guidance and multiple single-word examples.

### 3. Strategic Use of Loanwords

**Pattern:** English loanwords are kept when they're natural in the target language.

Examples preserved across languages:
- "Cashy" (brand name)
- "VIP Club" (kept in English everywhere)
- "Cash" (kept in German: "Cash-Gewinne")
- "Slots" (kept in most languages)
- "Blog" (kept everywhere)

**Implementation:** Added nuanced guidance in `<igaming_terms>` about when to keep English terms vs. translate.

### 4. Natural Compound Formation

**Pattern:** German-style compounds should follow natural target language patterns.

Examples:
- "Kein-Bullshit-Casino" (German compound with hyphens)
- "Willkommensbonus" (closed compound, no hyphens)

**Implementation:** Added examples showing proper compound formation in `<brand_voice>` section.

### 5. Locale-Appropriate Number Formatting

**Pattern:** Currency amounts adapt to local conventions while keeping currency symbols.

Examples:
- "$200.000 garantiert" (DE - period for thousands)
- "$200.000 garantizados" (ES - period for thousands)
- "$200 000 garantált" (HU - space for thousands)

**Implementation:** Enhanced `<number_formatting>` section with specific locale examples.

### 6. Consistent Casual Tone

**Pattern:** All translations use informal address forms consistently (except legal text).

Indicators:
- German: "Schnapp dir" (du-form), "Versuch's" (casual contraction)
- Spanish: "Regístrate" (tú-form)
- Italian: "Registrati" (tu-form)

**Implementation:** Made formality requirement more prominent in `<critical_rules>` and added explicit examples throughout.

## Optimizations for GPT-5.1 Capabilities

### 1. Enhanced Few-Shot Learning

**What:** Added `<few_shot_examples>` section with 4 concrete translation examples from ground truth.

**Why:** GPT-5.1 has stronger pattern recognition. Providing high-quality examples helps the model internalize the desired style and approach.

**Result:** Model can now reference specific approved translations when making similar decisions.

### 2. Hierarchical Content Type Guidance

**What:** Expanded content type sections with specific strategies and multiple examples for each type.

**Why:** GPT-5.1 can better understand and apply context-specific rules when they're clearly organized by content type.

**Structure:**
```
<ui_elements> → Strategy: Think mobile-first
<marketing_headlines> → Strategy: Ask would a local copywriter write this?
<value_propositions> → Strategy: Be specific and credible
<error_messages> → Strategy: Write like helping a friend
<legal_text> → Strategy: Translate as if lawyers will review
```

### 3. Meta-Cognitive Prompting

**What:** Added strategic questions throughout (e.g., "would a local copywriter write it this way?")

**Why:** GPT-5.1's improved reasoning benefits from prompts that encourage self-reflection on translation quality.

**Examples added:**
- "Would this fit in a small button?" (UI text)
- "Would a local copywriter write it this way?" (Marketing)
- "Write like you're helping a friend troubleshoot" (Errors)

### 4. Explicit Pattern Recognition

**What:** Added "Notice patterns:" section after few-shot examples highlighting key takeaways.

**Why:** Helps GPT-5.1 extract generalizable rules from specific examples.

**Patterns highlighted:**
- Idiomatic adaptation approach
- Ultra-concise UI text principles
- Natural compound noun formation
- Strategic loanword usage
- Locale-specific number formatting

### 5. Enhanced Role Definition

**What:** Changed from generic "localization linguist" to "senior localization linguist specializing in online casino brands" with "native-level fluency" and "deep cultural understanding."

**Why:** GPT-5.1 responds better to specific, authoritative role definitions that set expertise expectations.

### 6. Stronger Quality Verification

**What:** Expanded `<quality_checklist>` into three categories: Technical, Language, Cultural.

**Why:** GPT-5.1 can perform more sophisticated self-checking when given a structured verification framework.

**Categories:**
- Technical validation (placeholders, JSON, keys)
- Language quality (naturalness, idioms, tone)
- Cultural appropriateness (conventions, terminology)

### 7. Negative Examples in Output Format

**What:** Added explicit "Example of INCORRECT output" showing markdown fences and explanatory text.

**Why:** GPT-5.1 learns effectively from negative examples of what NOT to do.

### 8. Reinforced Critical Rules

**What:** Moved formality requirement (informal address) into `<critical_rules>` and added final verification step.

**Why:** Ensures consistency is treated as non-negotiable, not just guidance.

## Structural Improvements

### 1. Progressive Disclosure of Information

**Before:** All guidance mixed together
**After:** Information flows from general → specific → examples

Flow:
1. Role and task definition
2. Critical rules (non-negotiable)
3. Brand voice (general principles)
4. Content type guidelines (specific contexts)
5. Technical requirements (implementation details)
6. Few-shot examples (concrete references)
7. Quality checklist (verification)
8. Output instructions (format)

### 2. Richer Example Density

**Quantitative improvement:**
- Original prompt: ~8 translation examples
- Optimized v1: ~12 translation examples
- GPT-5.1 version: ~25+ translation examples across 7 languages

**Coverage:**
- Added examples for 7 different languages
- Added examples for all major content types
- Added examples of both good and bad translations
- Added examples of edge cases (compounds, loanwords)

### 3. Context-Specific Strategies

**New feature:** Each content type section now includes a "Strategy:" statement with actionable guidance.

**Benefit:** Provides decision-making framework, not just rules to follow.

Examples:
- UI: "Think mobile-first — would this fit in a small button?"
- Marketing: "Ask yourself — would a local copywriter write it this way?"
- Errors: "Write like you're helping a friend troubleshoot"
- Legal: "Translate as if this text will be reviewed by lawyers"

## Expected Improvements

### Quantitative

1. **Translation naturalness**: 15-25% improvement in human ratings of "sounds like a native wrote this"
2. **Length compliance**: 90%+ adherence to ±20% UI text length constraint
3. **Consistency**: Lower variance across multiple runs for same input
4. **Idiomatic expression usage**: Higher rate of culturally appropriate phrases vs. literal translations

### Qualitative

1. **Better concept adaptation**: More "Casino sin rodeos" translations, fewer literal "No-Bullshit-Casino" attempts
2. **Improved conciseness**: UI text will be tighter and more scannable
3. **Natural compounds**: Better handling of language-specific word formation
4. **Appropriate formality**: Consistent informal tone except in legal contexts
5. **Strategic loanword usage**: Better judgment on when to keep English terms

## Testing Recommendations

### 1. A/B Comparison Test

Run same inputs through both prompts:
- `prompt_optimized.txt` (baseline)
- `prompt_gpt5_optimized.txt` (new version)

Compare on:
- JSON validity (should be 100% both)
- Placeholder/HTML preservation (should be 100% both)
- Translation naturalness (expect improvement)
- Idiomatic usage (expect improvement)
- Length compliance (expect improvement)
- Tone consistency (expect improvement)

### 2. Native Speaker Blind Review

Present translations to native speakers without indicating which prompt generated them:
- Which sounds more natural?
- Which would you expect to see in a real casino app?
- Which has better tone consistency?
- Which has more appropriate formality?

### 3. Edge Case Testing

Test with challenging inputs:
- Very short UI text (1-2 words)
- Complex marketing headlines requiring cultural adaptation
- Mixed content with placeholders + HTML
- Long text blocks with multiple sentences
- Technical gaming terminology
- Legal disclaimers requiring formal tone

### 4. Cross-Language Consistency

Test same English input across multiple target languages:
- Do all maintain casual tone?
- Do all preserve brand name?
- Do all use appropriate loanwords?
- Do all adapt idioms appropriately?

## Usage with GPT-5.1 API

### Recommended Settings

```python
response = openai.ChatCompletion.create(
    model="gpt-5.1",  # or latest available model
    messages=[
        {
            "role": "system",
            "content": prompt_template.format(
                targetLanguage="German",
                regionVariant="Germany (DE)",
                contextPath="components/hero",
                glossary='{"Welcome Bonus": "Willkommensbonus"}',
                jsonInput=json.dumps(input_data)
            )
        }
    ],
    temperature=0.3,  # Lower for consistency
    max_tokens=4000,  # Adjust based on input size
    top_p=0.9,
    frequency_penalty=0.0,
    presence_penalty=0.0
)
```

### Parameter Rationale

- **temperature=0.3**: Lower temperature for more consistent, predictable translations. Still allows some creativity for idiomatic adaptation.
- **top_p=0.9**: Slightly restrict token sampling to avoid unexpected word choices while maintaining naturalness.
- **frequency_penalty=0.0**: No penalty needed; we want consistent terminology.
- **presence_penalty=0.0**: No penalty needed; we want natural repetition of common words.

### Template Variables

Ensure these are populated for each call:

- `${targetLanguage}`: Full language name (e.g., "German", "Spanish")
- `${regionVariant}`: Regional variant (e.g., "Germany (DE)", "Spain (ES)")
- `${contextPath}`: UI location (e.g., "components/hero", "pages/legal/terms")
- `${glossary}`: JSON object of required term translations (can be empty: `{}`)
- `${jsonInput}`: The actual JSON to translate

## Migration from Previous Version

### Breaking Changes

None — the new prompt is backward compatible.

### Recommended Approach

1. **Parallel testing**: Run both prompts for 1-2 weeks
2. **Compare outputs**: Use automated metrics + human review
3. **Gradual rollout**: Start with non-critical content
4. **Monitor quality**: Track user feedback and error rates
5. **Full migration**: Once confident in quality improvements

### Rollback Plan

If issues arise:
1. Keep `prompt_optimized.txt` as backup
2. Switch back by changing template file reference
3. Document any failure patterns for future improvement

## Future Optimization Opportunities

### 1. Language-Specific Prompts

Consider creating specialized versions for languages with unique challenges:
- **German**: Compound noun formation rules
- **Spanish**: Regional variants (ES vs LATAM)
- **Serbian/Croatian/Bosnian**: Language variants
- **Chinese**: Character limits for UI text

### 2. Dynamic Glossary Integration

Implement system to auto-populate glossary from:
- Previously approved translations
- Brand terminology database
- Industry standard term dictionaries

### 3. Context-Aware Length Optimization

Add more sophisticated length handling:
- Button text: max 15 characters
- Menu items: max 20 characters
- Headlines: max 60 characters
- Body text: no strict limit

### 4. Automated Quality Scoring

Implement post-processing validation:
- JSON structure verification
- Placeholder integrity check
- HTML tag validation
- Length ratio analysis
- Brand name preservation check
- Automated tone analysis

### 5. Feedback Loop Integration

Create system to:
- Collect user corrections
- Identify common error patterns
- Auto-update prompt with new examples
- Track quality metrics over time

## Conclusion

The GPT-5.1 optimized prompt represents a significant evolution by:

1. **Learning from ground truth**: Incorporating 7 languages of proven high-quality translations
2. **Leveraging GPT-5.1 capabilities**: Few-shot learning, meta-cognitive prompting, enhanced reasoning
3. **Providing concrete patterns**: More examples, clearer strategies, explicit decision frameworks
4. **Maintaining backward compatibility**: No breaking changes to structure or output format

Expected result: More natural, culturally appropriate translations that sound like they were written by native speakers, not translated by machines.
