import streamlit as st
import anthropic

# Page configuration
st.set_page_config(
    page_title="Perfect Gift Finder",
    page_icon="🎁",
    layout="centered"
)

# Custom CSS for elegant burgundy styling
st.markdown("""
<style>
    /* Main background - rich burgundy */
    .stApp {
        background: linear-gradient(145deg, #4a1c2a 0%, #722f37 50%, #4a1c2a 100%);
        background-attachment: fixed;
    }
    
    /* Main container styling */
    .main .block-container {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 24px;
        padding: 2.5rem 3rem;
        margin-top: 2rem;
        margin-bottom: 2rem;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
    }
    
    /* All text white */
    h1, h2, h3, p, span, label, .stMarkdown {
        color: #ffffff !important;
    }
    
    /* Header styling */
    h1 {
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        font-size: 2.5rem !important;
    }
    
    /* Subheaders */
    h3 {
        color: #ffd700 !important;
        font-weight: 600;
        margin-top: 1.5rem;
        border-bottom: 1px solid rgba(255, 215, 0, 0.3);
        padding-bottom: 0.5rem;
    }
    
    /* Intro text */
    .intro-text {
        text-align: center;
        color: rgba(255, 255, 255, 0.85) !important;
        font-size: 1.15rem;
        margin-bottom: 2rem;
        font-style: italic;
    }
    
    /* Input field styling */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: rgba(255, 255, 255, 0.95) !important;
        border: 2px solid rgba(255, 215, 0, 0.3) !important;
        border-radius: 12px !important;
        padding: 0.75rem !important;
        font-size: 0.95rem !important;
        color: #2d2d2d !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #ffd700 !important;
        box-shadow: 0 0 0 3px rgba(255, 215, 0, 0.2) !important;
    }
    
    /* Select box styling */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.95) !important;
        border-radius: 12px !important;
        border: 2px solid rgba(255, 215, 0, 0.3) !important;
    }
    
    .stSelectbox > div > div > div {
        color: #2d2d2d !important;
    }
    
    /* Slider styling */
    .stSlider > div > div > div > div {
        background: #ffd700 !important;
    }
    
    .stSlider > div > div > div > div > div {
        background: #ffd700 !important;
    }
    
    /* Button styling */
    .stFormSubmitButton > button {
        background: linear-gradient(90deg, #ffd700, #ffb347) !important;
        color: #4a1c2a !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 1rem 2rem !important;
        font-size: 1.15rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px !important;
        transition: all 0.3s ease !important;
        margin-top: 1.5rem !important;
        box-shadow: 0 4px 20px rgba(255, 215, 0, 0.4) !important;
    }
    
    .stFormSubmitButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 30px rgba(255, 215, 0, 0.5) !important;
    }
    
    /* Divider styling */
    hr {
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, rgba(255, 215, 0, 0.4), transparent) !important;
        margin: 2rem 0 !important;
    }
    
    /* Info box styling */
    .stAlert {
        background: rgba(255, 215, 0, 0.15) !important;
        border: 1px solid rgba(255, 215, 0, 0.3) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
    }
    
    .stAlert > div {
        color: #ffffff !important;
    }
    
    /* Error message styling */
    .stException, .stError {
        background: rgba(255, 100, 100, 0.2) !important;
        border-radius: 12px !important;
    }
    
    /* Caption/footer styling */
    .stCaption, caption {
        text-align: center !important;
        color: rgba(255, 255, 255, 0.6) !important;
    }
    
    /* Placeholder text */
    ::placeholder {
        color: #888888 !important;
        font-style: italic !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #ffd700 !important;
    }
    
    /* Results section styling */
    .element-container {
        color: #ffffff !important;
    }
    
    /* Links */
    a {
        color: #ffd700 !important;
    }
    
    /* Label text */
    .stTextInput > label, .stTextArea > label, .stSelectbox > label {
        color: #ffffff !important;
        font-weight: 500 !important;
    }
    
    /* Multiselect and select labels */
    div[data-baseweb="select"] > div {
        color: #2d2d2d !important;
    }
</style>
""", unsafe_allow_html=True)

# Title and introduction
st.title("🎁 Perfect Gift Finder")
st.markdown('<p class="intro-text">Discover thoughtful, personalized gift ideas that show you truly understand them</p>', unsafe_allow_html=True)

# FINAL SYSTEM PROMPT - V4 (Smarter Inference + Production Ready)
SYSTEM_PROMPT = """You are a thoughtful friend with a gift for understanding people—even from limited information. You're the person everyone asks for gift advice because you just "get it." You notice the little things, read between the lines, and make connections others miss.

## Your Superpower: Reading Between the Lines

Most people struggle to describe someone perfectly. That's okay. Your job is to take whatever they give you and build a richer picture by asking yourself:

**"What else is probably true about this person?"**

Use these inference techniques:

**1. Lifestyle Implications**
- "Busy working mom" → Probably values anything that saves time, rarely treats herself, appreciates practical luxury
- "College student" → Likely budget-conscious themselves, values experiences, might be in a small living space
- "Recent retiree" → Has more free time, possibly exploring new hobbies, might value experiences over things
- "Works in finance" → Likely appreciates quality, may have traditional tastes, probably owns the basics already

**2. Personality Depth**
- "Introverted" → Probably enjoys solo activities, thoughtful gifts over flashy ones, quality time at home
- "Always busy" → Might secretly crave relaxation, probably doesn't shop for themselves, appreciates convenience
- "Very organized" → Likely appreciates aesthetic consistency, hates clutter, values function and form
- "Adventurous" → Open to trying new things, might prefer experiences, probably doesn't want another "thing"

**3. Interest Expansion**
- "Loves cooking" → Might also appreciate: food photography, kitchen aesthetics, cookbooks as reading material, specialty ingredients, dining experiences
- "Into fitness" → Might also value: recovery/self-care, nutrition, athleisure they can wear casually, wellness experiences
- "Enjoys reading" → Consider: cozy accessories, bookish aesthetics, author events, reading-adjacent hobbies like journaling or tea

**4. Relationship Context**
- "Don't know them well" → Safer to go experiential or consumable; avoid permanent decor or highly personal items
- "Very close" → Can take more risks, inside jokes work, sentimental value matters more
- "Professional relationship" → Keep it appropriate but not generic; thoughtful beats expensive

**5. Occasion Intuition**
- Birthday → Celebrate who they are as a person
- Thank you → Match the gesture to what they did for you
- Housewarming → Practical but elevated; things they won't buy themselves
- Sympathy → Comfort and ease; nothing that requires effort from them

## How to Handle Sparse Information

When details are limited, don't just give generic gifts. Instead:

1. **Make educated guesses** based on demographics, relationship type, and occasion
2. **Lean into universal truths**: Most people appreciate quality over quantity, experiences over clutter, feeling understood over being impressed
3. **Offer range**: Include safer options alongside more personalized guesses
4. **Flag your reasoning**: "Based on her being a new mom, she might appreciate..." shows your thinking

## Core Philosophy

**Build a complete person from fragments.** A few details can paint a whole picture if you think about what they imply.

**Simple and thoughtful beats complicated and impressive.** "Knicks game tickets" > "personalized data visualization of team statistics."

**Budget doesn't equal thoughtfulness.** A $25 gift with real thought behind it beats a $200 generic gift.

**Respect the avoid list religiously.** If they say no candles, don't suggest candles.

## Strict Rules

**NEVER exceed the maximum budget.** If max is $75, nothing above $75.

**Spread prices across the full range.** Include options at the low, middle, and high end.

**Follow the selected gift style.** If they chose "Practical," every gift should be practical.

**No banned clichés** unless specifically relevant:
- Custom star maps (overdone)
- Generic scented candles
- Generic gift cards
- "Personalized" mugs/keychains
- Catch-all subscription boxes

## Response Structure

### 🎯 Gift Profile

4-5 sentences that show you truly understand this person—including insights you've inferred from what was shared. This should feel like, "Wow, you really get them" even if the input was sparse. Show your reasoning: "Based on X, they probably also value Y..."

---

### Top 5 Gift Ideas

**1. [Specific Gift Name]** — $XX

[1-2 sentences: What exactly is this? Be specific—brands, products, details.]

*Why they'd love it:* [Connect to both stated AND inferred traits. Show your reasoning.]

*Where to find it:* [1-2 specific stores or websites]

---

### 🎲 Wild Card

Something genuinely unexpected and specific to THIS person. Not a care package. Not a subscription box. Think: "What would make them say 'I never would have thought of that, but it's so me'?"

Base this on an inference—something you picked up on that maybe even the gift-giver didn't fully articulate.

---

### 💡 Gift-Giving Tips for This Person

2-3 specific tips about presentation, timing, or gestures based on their personality—including traits you've inferred. Make it personal and actionable.

---

## Quality Checklist

1. **Sound human.** Write like a thoughtful friend, not an AI.
2. **Show your reasoning.** "Since she's a busy mom, she probably..." builds trust.
3. **Infer deeper.** Go beyond what's written to what's implied.
4. **Pass the "would they use this?" test.**
5. **Stay in budget.** Never exceed the maximum.
6. **Be specific.** "Leuchtturm1917 notebook" not "a nice journal."
7. **Match the gift style.** If they selected one, follow it.
8. **Respect the avoid list.** Never suggest items they ruled out."""


# Create the input form
with st.form("gift_form"):
    
    # === SECTION 1: The Basics ===
    st.markdown("### 👤 The Basics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        recipient = st.text_input(
            "Who is this gift for?",
            placeholder="e.g., My sister Emma, My boss Michael"
        )
        
        age = st.text_input(
            "Their age",
            placeholder="e.g., 28, mid-40s, early 70s"
        )
        
        relationship = st.selectbox(
            "Your relationship",
            ["Select...", "Partner / Spouse", "Parent", "Sibling", "Best friend", 
             "Close friend", "Friend", "Child", "Grandparent", "In-laws",
             "Extended family", "Coworker", "Boss / Manager", "Mentor / Teacher",
             "Client", "Acquaintance", "New relationship", "Other"]
        )
    
    with col2:
        occasion = st.selectbox(
            "Occasion",
            ["Select...", "Birthday", "Christmas", "Hanukkah", "Anniversary",
             "Valentine's Day", "Mother's Day", "Father's Day", "Graduation",
             "Wedding gift", "Engagement", "Baby shower", "Housewarming",
             "Retirement", "Promotion / New job", "Thank you", "Apology",
             "Get well soon", "Sympathy", "Just because", "Other"]
        )
        
        budget_min, budget_max = st.select_slider(
            "Budget range",
            options=[0, 25, 50, 75, 100, 150, 200, 300, 400, 500, 750, 1000, 1500, 2000],
            value=(50, 150),
            format_func=lambda x: f"${x}" if x < 2000 else "$2000+"
        )
        
        how_well = st.selectbox(
            "How well do you know them?",
            ["Select...", 
             "Inside and out — we're extremely close",
             "Very well — we have a strong relationship", 
             "Pretty well — we spend regular time together",
             "Moderately — friendly but not super close",
             "Somewhat — still getting to know them",
             "Not well — more of an acquaintance"]
        )
    
    st.divider()
    
    # === SECTION 2: Who They Are ===
    st.markdown("### ✨ Who They Are")
    
    personality = st.text_area(
        "Describe their personality",
        placeholder="What are they like? Introverted/extroverted? Practical or whimsical? Minimalist or collector? What makes them unique? How would their friends describe them?",
        height=100
    )
    
    col3, col4 = st.columns(2)
    
    with col3:
        interests = st.text_area(
            "Interests & hobbies",
            placeholder="What do they love doing? What do they talk about with excitement? What are they passionate about?",
            height=120
        )
    
    with col4:
        lifestyle = st.text_area(
            "Lifestyle & situation",
            placeholder="What's their daily life like? Job situation? Living space? Do they travel? Have kids? Any recent life changes?",
            height=120
        )
    
    values = st.text_area(
        "What matters most to them?",
        placeholder="What do they value? Family? Career? Creativity? Adventure? Health? Sustainability? Learning? What principles guide their life?",
        height=80
    )
    
    st.divider()
    
    # === SECTION 3: Gift Intelligence ===
    st.markdown("### 🧠 Gift Intelligence")
    
    col5, col6 = st.columns(2)
    
    with col5:
        love_language = st.selectbox(
            "How do they feel most appreciated?",
            ["I'm not sure",
             "Thoughtful gifts — they treasure meaningful presents",
             "Quality time — experiences together mean the most",
             "Words — heartfelt notes and verbal appreciation",
             "Acts of service — doing things to help them",
             "Physical affection — they're warm and huggy"]
        )
    
    with col6:
        gift_style = st.selectbox(
            "What type of gift usually resonates?",
            ["I'm not sure",
             "Practical — things they'll actually use daily",
             "Experiential — activities, classes, events, trips",
             "Sentimental — personal, meaningful, memory-based",
             "Luxurious — quality items they wouldn't buy themselves",
             "Creative — unique, artistic, one-of-a-kind",
             "Self-care — relaxation, wellness, pampering",
             "Learning — books, courses, skill-building",
             "Tech — gadgets and electronics"]
        )
    
    previous_hits = st.text_area(
        "🎯 Gifts they've LOVED (from you or others)",
        placeholder="What gifts made them light up? What do they still use or talk about? Understanding past wins helps me find similar successes.",
        height=80
    )
    
    previous_misses = st.text_area(
        "❌ Gifts that missed the mark",
        placeholder="What gifts got a polite smile but gathered dust? What clearly wasn't their taste? This helps me avoid similar mistakes.",
        height=80
    )
    
    st.divider()
    
    # === SECTION 4: Extra Intel ===
    st.markdown("### 💡 Extra Intel")
    
    mentioned_wants = st.text_area(
        "Things they've mentioned wanting",
        placeholder="Any hints they've dropped? Something they pointed at in a store? A hobby they want to try? Something broken they need to replace?",
        height=80
    )
    
    avoid = st.text_area(
        "What to avoid",
        placeholder="Allergies? Things they hate? Items they have too many of? Sensitive topics? Anything that would definitely miss?",
        height=80
    )
    
    other_context = st.text_area(
        "Anything else I should know?",
        placeholder="Inside jokes? Recent events in their life? Your shared history? Their aesthetic preferences? The more context, the better the recommendations.",
        height=80
    )
    
    st.divider()
    
    # Submit button
    submitted = st.form_submit_button("✨ Find Perfect Gifts", use_container_width=True)

# Process the form when submitted
if submitted:
    # Validation
    missing_fields = []
    if not recipient:
        missing_fields.append("recipient")
    if relationship == "Select...":
        missing_fields.append("relationship")
    if occasion == "Select...":
        missing_fields.append("occasion")
    if not personality:
        missing_fields.append("personality")
    if not interests:
        missing_fields.append("interests")
    
    if missing_fields:
        st.error(f"Please fill in these required fields: {', '.join(missing_fields)}")
    else:
        # Build comprehensive user message
        budget_str = f"${budget_min} - ${budget_max}" if budget_max < 2000 else f"${budget_min} - $2000+"
        
        # Build gift style instruction
        gift_style_instruction = ""
        if gift_style != "I'm not sure":
            style_name = gift_style.split(" — ")[0]
            gift_style_instruction = f"\n\n**IMPORTANT: The user specifically requested {style_name} gifts. ALL 5 suggestions must fit this category.**"
        
        # Determine information completeness
        fields_filled = sum([
            bool(personality),
            bool(interests),
            bool(lifestyle),
            bool(values),
            love_language != "I'm not sure",
            gift_style != "I'm not sure",
            bool(previous_hits),
            bool(previous_misses),
            bool(mentioned_wants),
            bool(other_context)
        ])
        
        if fields_filled <= 3:
            info_note = "\n\n**Note:** Limited information was provided. Please use your inference skills to build a fuller picture of this person based on their age, relationship, occasion, and the details given. Make educated guesses and show your reasoning."
        elif fields_filled <= 6:
            info_note = "\n\n**Note:** Moderate information was provided. Fill in gaps by inferring related traits and preferences based on what's been shared."
        else:
            info_note = ""
        
        user_message = f"""Find the perfect gift based on this information:

## Basic Details
- **Recipient**: {recipient}
- **Age**: {age if age else "Not specified"}
- **Relationship**: {relationship}
- **Occasion**: {occasion}
- **Budget**: {budget_str}
  - ⚠️ STRICT MAXIMUM: ${budget_max}. Do not suggest anything above this price.
  - Include variety across the full range (low, middle, and high end).
- **How well I know them**: {how_well}

## Their Personality & Identity
{personality if personality else "Not specified — please infer from other details"}

## Interests & Hobbies
{interests if interests else "Not specified — please infer from other details"}

## Lifestyle & Current Situation
{lifestyle if lifestyle else "Not specified — please infer from relationship, age, and other context"}

## What They Value Most
{values if values else "Not specified — please infer from personality and interests"}

## Gift-Giving Insights
- **How they feel appreciated**: {love_language}
- **Gift style that resonates**: {gift_style}{gift_style_instruction}
- **Past gift wins**: {previous_hits if previous_hits else "None shared"}
- **Past gift misses**: {previous_misses if previous_misses else "None shared"}

## IMPORTANT — Things to Avoid
{avoid if avoid else "Nothing specific mentioned"}
{"⚠️ Do NOT suggest any items listed above. Read carefully and respect these restrictions." if avoid else ""}

## Additional Context
- **Things they've mentioned wanting**: {mentioned_wants if mentioned_wants else "Nothing specific"}
- **Other context**: {other_context if other_context else "None"}{info_note}

Remember:
1. Build a complete picture of this person—infer deeper traits from what's given
2. Stay at or BELOW the ${budget_max} maximum budget
3. Suggest gifts across the full price range
4. Follow the selected gift style if one was chosen
5. Never suggest items from the "avoid" list
6. Show your reasoning in the Gift Profile—explain what you inferred and why
7. Make the Wild Card specific to THIS person based on something you picked up on"""

        # Call the API
        with st.spinner("🎁 Finding perfect gift ideas..."):
            try:
                client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
                
                message = client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=3000,
                    system=SYSTEM_PROMPT,
                    messages=[
                        {"role": "user", "content": user_message}
                    ]
                )
                
                # Display results
                st.divider()
                st.markdown("## 🎁 Your Personalized Recommendations")
                st.markdown(message.content[0].text)
                
                # Price disclaimer
                st.divider()
                st.info("**💡 Pricing Note:** All prices are estimates. Please verify current prices before purchasing.")
                
            except Exception as e:
                st.error(f"Something went wrong: {str(e)}")
                st.markdown("Please check your API key in Streamlit secrets and try again.")

# Footer
st.divider()
st.caption("Built for Professor Hindman's AI Revolution course at GWU | Powered by Claude AI")
