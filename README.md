# Translation Prompt Testing Suite

Automated testing framework for evaluating translation prompt performance with GPT-5.1.

## Files Overview

- `prompt_optimized.txt` - Optimized translation prompt structured for GPT-5.1 comprehension
- `test_translation.py` - Python script to test translations and grade results
- `test_cases.json` - Comprehensive test cases covering different content types
- `prompt.txt` - Your original prompt (preserved for reference)
- `reasoning.txt` - Initial rationale and notes

## Setup

### Prerequisites

```bash
pip install openai
```

### API Key Configuration

Set your OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY='your-api-key-here'
```

### Model Configuration

**IMPORTANT:** Update the model name in `test_translation.py` when GPT-5.1 is available.

Current line 129:
```python
tester = TranslationTester(api_key, model="gpt-4")  # Update to "gpt-5.1"
```

## Running Tests

Execute the test suite:

```bash
python test_translation.py
```

This will:
1. Load all test cases from `test_cases.json`
2. For each test case:
   - Generate the prompt with test-specific variables
   - Call OpenAI API
   - Grade the translation output
   - Display detailed results
3. Print a summary of all test results

## Grading Rubric

The automated grading system evaluates translations on a 100-point scale:

| Check | Points | Description |
|-------|--------|-------------|
| Valid JSON | 15 | Output must be parseable JSON |
| Keys Unchanged | 15 | All keys must remain identical |
| Placeholders Preserved | 15 | {placeholders} must be exact |
| HTML Tags Preserved | 15 | All `<tags>` must be unchanged |
| "Cashy" Unchanged | 10 | Brand name must never be translated |
| String Count Matches | 10 | Same number of string values |
| Glossary Compliance | 10 | Must use required translations |
| No Extra Text | 5 | Output should be only JSON |
| Length Constraints | 5 | UI text within ±20% of source |

**Passing Grade:** 90+ points (A), 70-89 points (B), <70 needs improvement

## Test Cases

The suite includes 8 comprehensive test cases:

1. **German UI Text** - Dashboard elements with placeholders
2. **German Marketing** - Hero section with persuasive copy
3. **German Error Messages** - User-facing error handling
4. **German Legal** - Terms and conditions (formal)
5. **Spanish Mixed Content** - HTML tags and links
6. **German iGaming Terms** - Slot mechanics terminology
7. **French Complex Flow** - Multi-step UI wizard
8. **Italian Short UI** - Buttons and action labels

## Adding Custom Test Cases

Edit `test_cases.json` to add new test scenarios:

```json
{
  "name": "Test Case Name",
  "target_language": "German",
  "region_variant": "Germany (DE)",
  "context_path": "components/example/path",
  "glossary": {
    "Source Term": "Required Translation"
  },
  "json_input": {
    "key": "value to translate"
  }
}
```

## Prompt Optimization

### Key Improvements in `prompt_optimized.txt`

1. **XML Structure** - Uses semantic tags for clear section boundaries
2. **Critical Rules First** - Most important rules at the top
3. **Repeated Emphasis** - Critical rules stated upfront and at the end
4. **Inline Examples** - Examples immediately follow related rules
5. **Concise Language** - Token-efficient phrasing
6. **Explicit Verification** - Checklist format for self-QA
7. **Clear Output Format** - Unambiguous formatting requirements

### Why This Structure Works for LLMs

- **Semantic boundaries:** XML tags are clearer than visual separators
- **Primacy/recency effects:** Critical rules at start and end
- **Contextual examples:** Examples near rules improve learning
- **Reduced "lost in middle":** Shorter focused sections
- **Explicit instructions:** Removes ambiguity in requirements

## Interpreting Results

### Example Output

```
RESULTS: German UI Text with Placeholders
Score: 95/100 (95.0%)

Detailed Checks:
  ✓ PASS | valid_json
  ✓ PASS | keys_unchanged
  ✓ PASS | placeholders_preserved
  ✓ PASS | html_tags_preserved
  ✓ PASS | cashy_unchanged
  ✓ PASS | string_count_matches
  ✓ PASS | glossary_compliance
  ✗ FAIL | no_extra_text
          Response contained markdown code fences
  ✓ PASS | length_constraints
```

### Common Issues

**Markdown Code Fences:**
- Model adds ` ```json ` around output
- Still parseable but violates "no extra text" rule
- May need additional prompt emphasis

**Length Violations:**
- Translation significantly longer/shorter than source
- Common with German (longer) or Italian (shorter)
- Check if translation is too literal vs. natural

**Glossary Misses:**
- Model didn't use required translation
- May need glossary format adjustment
- Consider adding examples of glossary usage

## Modifying the Prompt

To test prompt variations:

1. Create a copy: `cp prompt_optimized.txt prompt_v2.txt`
2. Make your changes to the new file
3. Update script to use new prompt:
   ```python
   tester = TranslationTester(api_key, model="gpt-4",
                             prompt_template_path="prompt_v2.txt")
   ```
4. Run tests and compare scores

## Advanced Usage

### Testing Individual Cases

Modify `main()` in `test_translation.py`:

```python
# Test only specific cases
test_cases = [tc for tc in test_cases if 'German' in tc.name]
```

### Saving Results

Add result logging:

```python
with open('test_results.json', 'w') as f:
    json.dump(results, f, indent=2)
```

### Batch Testing

Test multiple prompt versions:

```python
prompts = ['prompt_optimized.txt', 'prompt_v2.txt', 'prompt_v3.txt']
for prompt_file in prompts:
    tester = TranslationTester(api_key, model="gpt-4",
                               prompt_template_path=prompt_file)
    # Run tests...
```

## Best Practices

1. **Establish Baseline:** Run tests with current prompt before modifications
2. **Single Variable:** Change one aspect at a time
3. **Multiple Runs:** Run 3+ times to account for model variance
4. **Real Data:** Add test cases from actual production content
5. **Edge Cases:** Test with very short/long text, special characters, etc.

## Troubleshooting

**API Errors:**
- Check `OPENAI_API_KEY` is set correctly
- Verify API quota and rate limits
- Check model name is correct for GPT-5.1

**Import Errors:**
- Install openai: `pip install openai`
- Check Python version: 3.7+ required

**JSON Parsing Fails:**
- Model may be returning invalid JSON
- Check if model is following output format instructions
- May need stronger emphasis on JSON validity

## Next Steps

1. **Run baseline tests** with both prompts (original and optimized)
2. **Compare scores** to identify improvements
3. **Analyze failures** to understand edge cases
4. **Iterate prompt** based on consistent failure patterns
5. **A/B test** different prompt variations
6. **Validate with humans** - automated grading catches technical issues, but tone/naturalness needs human review

## Human Review Checklist

For translations that score >90, manually verify:

- [ ] Sounds natural to native speaker
- [ ] Matches Cashy brand voice (direct, no BS)
- [ ] Appropriate formality level
- [ ] Culturally appropriate
- [ ] No awkward phrasing
- [ ] Maintains intended meaning

## Contact & Support

For issues or questions about this testing suite, refer to the Cashy translation documentation or reach out to the localization team.
