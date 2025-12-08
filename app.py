import streamlit as st
import json
import re
from pathlib import Path
import anthropic
from openai import OpenAI
import google.generativeai as genai
from typing import Dict, Any, Optional

# Reference translations for evaluation
REFERENCE_TRANSLATIONS = {
    "French": {
        "hero_headline": "ZERO PIPEAU CASINO",
        "hero_subheadline": "Que des gains en cash"
    },
    "Spanish": {
        "hero_headline": "CASINO SIN RODEOS",
        "hero_subheadline": "Solo premios en cash"
    },
    "Italian": {
        "hero_headline": "ZERO FUFFA CASINÒ",
        "hero_subheadline": "Solo premi in cash"
    },
    "German": {
        "hero_headline": "CASINO OHNE TRICKS",
        "hero_subheadline": "Nur Cash-Gewinne"
    },
    "Russian": {
        "hero_headline": "КАЗИНО БЕЗ ФОКУСОВ",
        "hero_subheadline": "Только денежные призы"
    },
    "Japanese": {
        "hero_headline": "透明性の高いカジノ",
        "hero_subheadline": "現金賞品のみ"
    },
    "Indonesian": {
        "hero_headline": "KASINO JUJUR TERBUKA",
        "hero_subheadline": "HANYA HADIAH TUNAI"
    },
    "Simplified Chinese": {
        "hero_headline": "无废话娱乐场",
        "hero_subheadline": "纯粹现金奖励"
    },
    "Traditional Chinese": {
        "hero_headline": "無廢話娛樂場",
        "hero_subheadline": "純粹現金獎勵"
    },
    "Korean": {
        "hero_headline": "투명한 카지노",
        "hero_subheadline": "오직 현금상금"
    },
    "Portuguese (Portugal)": {
        "hero_headline": "CASINO A SÉRIO",
        "hero_subheadline": "Prémios em dinheiro"
    },
    "Portuguese (Brazil)": {
        "hero_headline": "CASSINO NA VEIA",
        "hero_subheadline": "Prêmios em dinheiro"
    },
    "Turkish": {
        "hero_headline": "DOLANSIZ CASINO",
        "hero_subheadline": "Sadece nakit ödüller"
    },
    "Hindi": {
        "hero_headline": "साफ़ सुथरा कैसिनो",
        "hero_subheadline": "सिर्फ नकद इनाम"
    },
    "Vietnamese": {
        "hero_headline": "SÒNG BẠC KHÔNG XẠO",
        "hero_subheadline": "Chỉ thưởng tiền mặt thật"
    },
    "Arabic (Peninsular)": {
        "hero_headline": "كازينو بلا تعقيد",
        "hero_subheadline": "مكافآت نقدية بس"
    }
}

# Page configuration
st.set_page_config(
    page_title="Translation Prompt Tester",
    page_icon="🌐",
    layout="wide"
)

# Initialize API clients
@st.cache_resource
def get_anthropic_client():
    """Initialize Anthropic client with API key from secrets"""
    try:
        return anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
    except Exception as e:
        st.error(f"Failed to initialize Anthropic client: {e}")
        return None

@st.cache_resource
def get_openai_client():
    """Initialize OpenAI client with API key from secrets"""
    try:
        return OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    except Exception as e:
        st.error(f"Failed to initialize OpenAI client: {e}")
        return None

@st.cache_resource
def get_gemini_client():
    """Initialize Gemini client with API key from secrets"""
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        return genai.GenerativeModel("gemini-3-pro-preview")
    except Exception as e:
        st.error(f"Failed to initialize Gemini client: {e}")
        return None

def load_prompt_template() -> str:
    """Load the optimized GPT-5.1 prompt template"""
    prompt_path = Path(__file__).parent / "prompt_gpt5_optimized.txt"
    try:
        with open(prompt_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        st.error(f"Prompt template not found at {prompt_path}")
        return ""

def format_prompt(
    template: str,
    target_language: str,
    region_variant: str,
    context_path: str,
    glossary: Dict[str, str],
    json_input: str
) -> str:
    """Format the prompt template with user inputs"""
    glossary_str = json.dumps(glossary) if glossary else "{}"

    return template.replace("${targetLanguage}", target_language) \
                   .replace("${regionVariant}", region_variant) \
                   .replace("${contextPath}", context_path) \
                   .replace("${glossary}", glossary_str) \
                   .replace("${jsonInput}", json_input)

def translate_with_opus(prompt: str, temperature: float = 0.3) -> Optional[str]:
    """Call Claude Opus with the formatted prompt"""
    client = get_anthropic_client()
    if not client:
        return None

    try:
        with st.spinner("Translating with Claude Opus..."):
            message = client.messages.create(
                model="claude-opus-4-5-20251101",
                max_tokens=4000,
                temperature=temperature,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            return message.content[0].text
    except Exception as e:
        st.error(f"Opus translation failed: {e}")
        return None

def translate_with_sonnet(prompt: str, temperature: float = 0.3) -> Optional[str]:
    """Call Claude Sonnet with the formatted prompt"""
    client = get_anthropic_client()
    if not client:
        return None

    try:
        with st.spinner("Translating with Claude Sonnet..."):
            message = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4000,
                temperature=temperature,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            return message.content[0].text
    except Exception as e:
        st.error(f"Sonnet translation failed: {e}")
        return None

def translate_with_gpt(prompt: str, temperature: float = 0.3) -> Optional[str]:
    """Call GPT-5.1 with the formatted prompt"""
    client = get_openai_client()
    if not client:
        return None

    try:
        with st.spinner("Translating with GPT-5.1..."):
            response = client.chat.completions.create(
                model="gpt-5.1-2025-11-13",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=temperature,
                max_completion_tokens=4000,
                top_p=0.9
            )
            return response.choices[0].message.content
    except Exception as e:
        st.error(f"GPT-5.1 translation failed: {e}")
        return None

def translate_with_gemini(prompt: str, temperature: float = 0.3) -> Optional[str]:
    """Call Gemini 3 Pro with the formatted prompt"""
    model = get_gemini_client()
    if not model:
        return None

    try:
        with st.spinner("Translating with Gemini 3 Pro..."):
            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=4000,
                )
            )
            return response.text
    except Exception as e:
        st.error(f"Gemini 3 Pro translation failed: {e}")
        return None

def clean_json_output(text: str) -> str:
    """Clean model output to extract pure JSON"""
    if not text:
        return ""

    # Remove markdown code fences
    text = re.sub(r'^```json\s*\n?', '', text, flags=re.MULTILINE)
    text = re.sub(r'^```\s*\n?', '', text, flags=re.MULTILINE)
    text = re.sub(r'\n?```\s*$', '', text, flags=re.MULTILINE)

    # Try to find JSON object in the text
    # Look for content between first { and last }
    start = text.find('{')
    end = text.rfind('}')

    if start != -1 and end != -1 and end > start:
        text = text[start:end+1]

    return text.strip()

def validate_json(json_str: str) -> tuple[bool, Optional[Dict], str]:
    """Validate JSON string and return parsed object"""
    try:
        # Clean the JSON string first
        cleaned = clean_json_output(json_str)
        parsed = json.loads(cleaned)
        return True, parsed, ""
    except json.JSONDecodeError as e:
        return False, None, f"Invalid JSON: {e}"

def compile_all_results_for_copy(all_results: Dict[str, Any], json_parsed: Dict) -> str:
    """Compile all translation results into a copyable format"""
    output_lines = []
    output_lines.append("=" * 80)
    output_lines.append("TRANSLATION RESULTS - SELECTED LANGUAGES")
    output_lines.append("=" * 80)
    output_lines.append("")

    for language in all_results.keys():
        result_data = all_results.get(language)
        if not result_data or not result_data.get("valid"):
            continue

        result_parsed = result_data["parsed"]

        output_lines.append(f"\n{'='*80}")
        output_lines.append(f"LANGUAGE: {language}")
        output_lines.append(f"{'='*80}\n")

        # Show hero_headline comparison
        if "hero_headline" in result_parsed:
            output_lines.append("HERO HEADLINE:")
            output_lines.append(f"  Translation: {result_parsed['hero_headline']}")
            output_lines.append(f"  Char count:  {len(result_parsed['hero_headline'])} / 20")
            if language in REFERENCE_TRANSLATIONS and "hero_headline" in REFERENCE_TRANSLATIONS[language]:
                ref = REFERENCE_TRANSLATIONS[language]["hero_headline"]
                match_status = "✅ MATCH" if result_parsed['hero_headline'] == ref else "❌ NO MATCH"
                output_lines.append(f"  Reference:   {ref}")
                output_lines.append(f"  Status:      {match_status}")
            output_lines.append("")

        # Show hero_subheadline comparison
        if "hero_subheadline" in result_parsed:
            output_lines.append("HERO SUBHEADLINE:")
            output_lines.append(f"  Translation: {result_parsed['hero_subheadline']}")
            output_lines.append(f"  Char count:  {len(result_parsed['hero_subheadline'])} / 24")
            if language in REFERENCE_TRANSLATIONS and "hero_subheadline" in REFERENCE_TRANSLATIONS[language]:
                ref = REFERENCE_TRANSLATIONS[language]["hero_subheadline"]
                match_status = "✅ MATCH" if result_parsed['hero_subheadline'] == ref else "❌ NO MATCH"
                output_lines.append(f"  Reference:   {ref}")
                output_lines.append(f"  Status:      {match_status}")
            output_lines.append("")

        # Show other fields
        output_lines.append("OTHER FIELDS:")
        for key, value in result_parsed.items():
            if key not in ["hero_headline", "hero_subheadline"]:
                output_lines.append(f"  {key}: {value}")
        output_lines.append("")

    output_lines.append("=" * 80)
    output_lines.append("END OF RESULTS")
    output_lines.append("=" * 80)

    return "\n".join(output_lines)

def evaluate_against_reference(translation: Dict[str, Any], target_language: str) -> Dict[str, Any]:
    """Evaluate translation against reference translations"""
    # Check if we have reference translations for this language
    if target_language not in REFERENCE_TRANSLATIONS:
        return {"has_reference": False}

    reference = REFERENCE_TRANSLATIONS[target_language]
    results = {"has_reference": True, "matches": []}

    # Check hero_headline
    if "hero_headline" in translation and "hero_headline" in reference:
        actual = translation["hero_headline"].strip()
        expected = reference["hero_headline"]
        matches = actual == expected
        results["matches"].append({
            "field": "hero_headline",
            "expected": expected,
            "actual": actual,
            "matches": matches,
            "char_count": len(actual)
        })

    # Check hero_subheadline
    if "hero_subheadline" in translation and "hero_subheadline" in reference:
        actual = translation["hero_subheadline"].strip()
        expected = reference["hero_subheadline"]
        matches = actual == expected
        results["matches"].append({
            "field": "hero_subheadline",
            "expected": expected,
            "actual": actual,
            "matches": matches,
            "char_count": len(actual)
        })

    return results

def main():
    st.title("🌐 Translation Prompt Tester")
    st.markdown("Test translation prompts with Claude Opus and GPT-5.1")

    # Load default prompt template
    default_prompt = load_prompt_template()
    if not default_prompt:
        default_prompt = ""

    # Create two columns for input and output
    col1, col2 = st.columns([1, 1])

    with col1:
        st.header("Input Configuration")

        # Model selection
        model_choice = st.selectbox(
            "Select Translation Model",
            ["Claude Opus 4.5", "Claude Sonnet 4.5", "GPT-5.1", "Gemini 3 Pro"],
            help="Choose which AI model to use for translation"
        )

        # Temperature slider
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.3,
            step=0.1,
            help="Lower values = more consistent, Higher values = more creative"
        )

        # Prompt editor
        st.subheader("Translation Prompt")
        with st.expander("✏️ Edit Prompt Template", expanded=False):
            st.markdown("**Variables:** `${targetLanguage}`, `${regionVariant}`, `${contextPath}`, `${glossary}`, `${jsonInput}`")
            prompt_template = st.text_area(
                "Prompt Template",
                value=default_prompt,
                height=400,
                help="Edit the prompt template. Use variables like ${targetLanguage}, ${jsonInput}, etc.",
                label_visibility="collapsed"
            )

        # Target language configuration
        st.subheader("Language Settings")

        # Language selection
        all_languages = list(REFERENCE_TRANSLATIONS.keys())

        col_a, col_b = st.columns([3, 1])
        with col_a:
            selected_languages = st.multiselect(
                "Select languages to translate",
                options=all_languages,
                default=all_languages,
                help="Choose which languages to translate. Select multiple or all."
            )
        with col_b:
            st.write("")  # Spacing
            st.write("")  # Spacing
            if st.button("Select All", use_container_width=True):
                selected_languages = all_languages
                st.rerun()

        if not selected_languages:
            st.warning("⚠️ Please select at least one language to translate")
        else:
            st.info(f"📋 Will translate to {len(selected_languages)} language(s): {', '.join(selected_languages)}")

        # JSON input to translate
        st.subheader("JSON to Translate")
        json_input = st.text_area(
            "Input JSON",
            value="""{
  "hero_headline": "ZERO BS CASINO",
  "hero_subheadline": "CASH REWARDS ONLY",
  "hero_bullet_no_wagering": "No wagering requirements",
  "hero_bullet_fast_payouts": "Super fast payouts",
  "hero_bullet_no_limits": "No limits on wins & withdrawals",
  "hero_cta_signup": "Sign up"
}""",
            height=300,
            help="The JSON object to translate"
        )

        # Validate input JSON
        json_valid, json_parsed, json_error = validate_json(json_input)
        if not json_valid:
            st.error(json_error)

        # Translate button
        translate_button = st.button(
            "🚀 Translate",
            type="primary",
            disabled=not json_valid or not selected_languages,
            use_container_width=True
        )

    with col2:
        st.header("Translation Results")

        if translate_button:
            # Translate selected languages
            all_results = {}

            with st.spinner(f"Translating to {len(selected_languages)} language(s)..."):
                for language in selected_languages:
                    # Format the prompt
                    formatted_prompt = format_prompt(
                        template=prompt_template,
                        target_language=language,
                        region_variant=language,
                        context_path="translation",
                        glossary={},
                        json_input=json_input
                    )

                    # Call appropriate model
                    if model_choice == "Claude Opus 4.5":
                        result = translate_with_opus(formatted_prompt, temperature)
                    elif model_choice == "Claude Sonnet 4.5":
                        result = translate_with_sonnet(formatted_prompt, temperature)
                    elif model_choice == "GPT-5.1":
                        result = translate_with_gpt(formatted_prompt, temperature)
                    else:  # Gemini 3 Pro
                        result = translate_with_gemini(formatted_prompt, temperature)

                    # Store result
                    if result:
                        result_valid, result_parsed, result_error = validate_json(result)
                        all_results[language] = {
                            "valid": result_valid,
                            "parsed": result_parsed,
                            "error": result_error,
                            "raw": result
                        }
                    else:
                        all_results[language] = {
                            "valid": False,
                            "parsed": None,
                            "error": "Translation failed",
                            "raw": None
                        }

            # Add copy button for all results
            st.subheader("📋 Copy All Results")
            # Filter compile function to only show selected languages
            filtered_results = {lang: all_results[lang] for lang in selected_languages if lang in all_results}
            compiled_results = compile_all_results_for_copy(filtered_results, json_parsed)

            with st.expander("View/Copy All Translation Results", expanded=False):
                st.code(compiled_results, language="text")
                st.info("💡 Tip: Click the copy button in the top-right corner of the code block above to copy all results")

            # Display results in tabs
            tabs = st.tabs(selected_languages)

            for idx, language in enumerate(selected_languages):
                with tabs[idx]:
                    result_data = all_results.get(language)

                    if not result_data:
                        st.error("No result for this language")
                        continue

                    if result_data["valid"]:
                        result_parsed = result_data["parsed"]

                        # Show formatted JSON
                        st.code(json.dumps(result_parsed, indent=2, ensure_ascii=False), language="json")

                        # Validation checks
                        st.subheader("🔍 Validation Checks")

                        checks = []

                        # Check 1: Same keys
                        input_keys = set(json_parsed.keys())
                        output_keys = set(result_parsed.keys())
                        keys_match = input_keys == output_keys
                        checks.append(("Same keys", keys_match))

                        # Check 2: Cashy preserved
                        result_str = json.dumps(result_parsed)
                        cashy_preserved = "Cashy" in result_str or "cashy" not in result_str.lower()
                        checks.append(("Brand name 'Cashy' preserved", cashy_preserved))

                        # Check 3: Placeholders
                        input_values = ' '.join(str(v) for v in json_parsed.values())
                        output_values = ' '.join(str(v) for v in result_parsed.values())
                        input_placeholders = set(re.findall(r'\{[a-zA-Z_][a-zA-Z0-9_]*\}', input_values))
                        output_placeholders = set(re.findall(r'\{[a-zA-Z_][a-zA-Z0-9_]*\}', output_values))
                        placeholders_preserved = input_placeholders == output_placeholders or len(input_placeholders) == 0
                        checks.append(("Placeholders preserved", placeholders_preserved))

                        # Display checks
                        for check_name, passed in checks:
                            if passed:
                                st.success(f"✅ {check_name}")
                            else:
                                st.error(f"❌ {check_name}")

                        # Reference translation evaluation
                        eval_results = evaluate_against_reference(result_parsed, language)

                        if eval_results["has_reference"]:
                            st.subheader("📚 Reference Match Evaluation")

                            for match_info in eval_results["matches"]:
                                field = match_info["field"]
                                expected = match_info["expected"]
                                actual = match_info["actual"]
                                matches = match_info["matches"]
                                char_count = match_info["char_count"]

                                # Determine character limit
                                if field == "hero_headline":
                                    char_limit = 20
                                elif field == "hero_subheadline":
                                    char_limit = 24
                                else:
                                    char_limit = None

                                within_limit = char_count <= char_limit if char_limit else True

                                # Display match status
                                if matches and within_limit:
                                    st.success(f"✅ **{field}**: Perfect match! ({char_count}/{char_limit} chars)")
                                elif matches and not within_limit:
                                    st.warning(f"⚠️ **{field}**: Matches but exceeds limit ({char_count}/{char_limit} chars)")
                                else:
                                    # Show comparison
                                    c1, c2 = st.columns(2)
                                    with c1:
                                        status_icon = "✅" if within_limit else "⚠️"
                                        st.error(f"❌ **{field}** ({char_count}/{char_limit} chars {status_icon})")
                                        st.text("Expected:")
                                        st.code(expected, language="text")
                                    with c2:
                                        st.text("Got:")
                                        st.code(actual, language="text")

                    else:
                        st.error(f"⚠️ Invalid JSON output")
                        st.code(result_data.get("raw", ""), language="text")
                        st.error(result_data.get("error", "Unknown error"))

        else:
            st.info("👈 Select languages, configure settings, and click 'Translate' to see results")

    # Sidebar with information
    with st.sidebar:
        st.header("ℹ️ About")
        st.markdown("""
        This tool allows you to test translation prompts using:
        - **Claude Opus 4.5**: Anthropic's most capable model
        - **Claude Sonnet 4.5**: Anthropic's balanced model (faster, cost-effective)
        - **GPT-5.1**: OpenAI's latest model
        - **Gemini 3 Pro**: Google's newest preview model

        ### How to use:
        1. Select your translation model
        2. (Optional) Edit the prompt template
        3. Configure target language
        4. Paste your JSON input
        5. Click **Translate**

        ### Tips:
        - Edit the prompt to test different approaches
        - Lower temperature (0.2-0.4) for consistent translations
        - Higher temperature (0.5-0.8) for creative marketing copy
        - Always validate JSON output before use
        """)

if __name__ == "__main__":
    main()
