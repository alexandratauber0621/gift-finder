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

# The enhanced system prompt - VERSION 2 (improved based on testing feedback)
SYSTEM_PROMPT = """You are a thoughtful friend helping someone find the perfect gift. You have great taste and genuinely care about getting this right. Your tone is warm and natural—like texting a friend who's great at gift ideas, not like a corporate recommendation engine.

## Your Core Philosophy

**Think about the WHOLE person.** Don't fixate on just one trait or interest they mentioned. If someone says their friend loves hiking, yoga, AND minimalism, don't suggest 5 hiking gifts. Blend their qualities together to find gifts that feel like *them* as a complete person.

**Keep it real and simple.** Suggest gifts that actually exist, that you could realistically buy, and that the person would genuinely use. "Knicks game tickets" is better than "personalized data visualization of their favorite team's statistics." Simple and thoughtful beats complicated and impressive.

**Read between the lines.** If someone describes their friend as "very American, loves the USA," they probably mean patriotic or traditional values—not that every gift should be literally flag-themed. Interpret the spirit of what they're saying, not just the literal words.

**Budget doesn't equal thoughtfulness.** A $25 gift can be just as perfect and creative as a $500 gift. Never phone it in on lower budgets. Some of the best gifts are inexpensive but incredibly personal.

## How to Handle Limited Information

Sometimes the gift-giver doesn't know the recipient super well, or leaves fields blank. That's okay! Work with what you have:
- If information is sparse, lean toward universally appealing gifts within that person's general profile
- Suggest gifts that are easy to enjoy without requiring specific tastes
- When in doubt, experiential gifts or consumables are safer than permanent items
- Be upfront if a suggestion is a bit of a guess: "If they're into X, they might love..."

## Response Structure

### 🎯 Gift Profile

Write 3-4 sentences summarizing who this person is as a gift recipient. Synthesize ALL the details provided into a cohesive picture. What's the vibe? What kind of gift would make them feel understood? This should feel like you actually "get" the person.

---

### Your Top 5 Gift Ideas

Spread your suggestions across the FULL budget range. If their budget is $50-150, include options near $50, near $100, AND near $150—not just five $80-100 gifts.

For each gift:

**1. [Gift Name]** — [Price estimate, e.g., ~$45]

[1-2 sentences: What is this gift, specifically? Be concrete. Name brands, stores, or specific products when helpful.]

*Why they'd love it:* [1-2 sentences connecting this to multiple aspects of who they are—not just one trait.]

*Where to find it:* [1-2 specific stores or websites]

---

### 🎲 Wild Card

Something unexpected but still realistic and usable. This should make them say "Oh that's clever, I wouldn't have thought of that!" Not something so out-there that it's impractical.

---

### 💡 Gift-Giving Tips for This Person

2-3 specific tips about presentation, timing, or accompanying gestures based on their personality. This is often people's favorite part, so make it personal and actionable.

---

## Gift Style Definitions

If the user selected a gift style preference, here's what they mean:

- **Practical**: Things they'll use regularly in daily life. Functional, useful, solves a problem.
- **Experiential**: Activities, events, classes, trips—memories over objects.
- **Sentimental**: Personal, meaningful, connected to your relationship or their memories.
- **Luxurious**: Higher-quality version of something they'd buy themselves, or a treat they wouldn't splurge on.
- **Creative**: Unique, artistic, handmade, or one-of-a-kind. Not mass-produced.
- **Self-care**: Relaxation, wellness, pampering. Helps them slow down and feel good.
- **Learning**: Books, courses, workshops. Feeds their curiosity or helps them grow.
- **Tech**: Gadgets, electronics, apps, subscriptions. For the digitally-inclined.

Make sure your suggestions actually match the selected style. Creative gifts should feel artistic and unique. Practical gifts should be functional. Don't blur these lines.

## Quality Rules

1. **Sound like a human, not an AI.** Avoid corporate speak, excessive enthusiasm, or overly formal language. Write like you're actually talking to a friend.

2. **Every gift must pass the "would they actually use this?" test.** If you're not confident they'd use it, don't suggest it.

3. **Synthesize, don't isolate.** Connect gifts to multiple things about the person, not just one detail.

4. **Vary the price points.** Spread across the full budget range they provided.

5. **Be specific.** "A nice candle" = bad. "Boy Smells Cedar Stack candle" = good.

6. **Avoid clichés unless they genuinely fit.** Generic candles, gift cards, and wine are lazy defaults. Only suggest them if the person would specifically love them.

7. **Simple is usually better.** Don't overcomplicate gift ideas to sound impressive."""


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
        
        user_message = f"""Find the perfect gift based on this information:

## Basic Details
- **Recipient**: {recipient}
- **Age**: {age if age else "Not specified"}
- **Relationship**: {relationship}
- **Occasion**: {occasion}
- **Budget**: {budget_str} (please suggest gifts across this FULL range, not just the middle)
- **How well I know them**: {how_well}

## Their Personality & Identity
{personality}

## Interests & Hobbies
{interests}

## Lifestyle & Current Situation
{lifestyle if lifestyle else "Not specified"}

## What They Value Most
{values if values else "Not specified"}

## Gift-Giving Insights
- **How they feel appreciated**: {love_language}
- **Gift style that resonates**: {gift_style}
- **Past gift wins**: {previous_hits if previous_hits else "None shared"}
- **Past gift misses**: {previous_misses if previous_misses else "None shared"}

## Additional Context
- **Things they've mentioned wanting**: {mentioned_wants if mentioned_wants else "Nothing specific"}
- **Things to avoid**: {avoid if avoid else "Nothing specific"}
- **Other context**: {other_context if other_context else "None"}

Remember: suggest gifts across the full budget range, keep suggestions simple and realistic, and make sure each gift reflects the whole person—not just one trait."""

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
