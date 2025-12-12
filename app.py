import streamlit as st
import anthropic

# Page configuration
st.set_page_config(
    page_title="Perfect Gift Finder",
    page_icon="🎁",
    layout="centered"
)

# Custom CSS for sophisticated styling
st.markdown("""
<style>
    /* Main background and font */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }
    
    /* Main container styling */
    .main .block-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 2rem 3rem;
        margin-top: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    }
    
    /* Header styling */
    h1 {
        color: #2d3748;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    /* Subheader styling */
    h2, h3 {
        color: #4a5568;
        font-weight: 600;
        margin-top: 1.5rem;
    }
    
    /* Section headers with icons */
    .section-header {
        background: linear-gradient(90deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 1.3rem;
        font-weight: 600;
        margin: 1.5rem 0 1rem 0;
    }
    
    /* Input field styling */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border: 2px solid #e2e8f0;
        border-radius: 10px;
        padding: 0.75rem;
        font-size: 0.95rem;
        transition: border-color 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Select box styling */
    .stSelectbox > div > div {
        border-radius: 10px;
    }
    
    /* Button styling */
    .stFormSubmitButton > button {
        background: linear-gradient(90deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.875rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        margin-top: 1rem;
    }
    
    .stFormSubmitButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
    }
    
    /* Divider styling */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #e2e8f0, transparent);
        margin: 1.5rem 0;
    }
    
    /* Results container */
    .results-container {
        background: #f8fafc;
        border-radius: 15px;
        padding: 1.5rem;
        margin-top: 1rem;
        border: 1px solid #e2e8f0;
    }
    
    /* Info box styling */
    .stAlert {
        border-radius: 12px;
    }
    
    /* Caption/footer styling */
    .stCaption {
        text-align: center;
        color: #718096;
    }
    
    /* Placeholder text */
    ::placeholder {
        color: #a0aec0;
        font-style: italic;
    }
    
    /* Slider styling */
    .stSlider > div > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Intro text */
    .intro-text {
        text-align: center;
        color: #718096;
        font-size: 1.1rem;
        margin-bottom: 1.5rem;
    }
    
    /* Form section backgrounds */
    .form-section {
        background: #f8fafc;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Title and introduction
st.title("🎁 Perfect Gift Finder")
st.markdown('<p class="intro-text">Discover thoughtful, personalized gift ideas that show you truly understand them</p>', unsafe_allow_html=True)

# The enhanced system prompt
SYSTEM_PROMPT = """You are an elite gift consultant with deep expertise in finding meaningful, personalized gifts. Your recommendations consistently surprise and delight recipients because you understand people on a deeper level.

## Your Approach

Before recommending gifts, you conduct a thorough psychological and lifestyle analysis. You don't suggest generic options—you find gifts that make people feel truly *seen*.

## Analysis Framework

When reviewing the information provided, consider:

**Identity & Values**: What defines this person? What do they care about deeply? What brings them joy and meaning?

**Lifestyle Fit**: What would seamlessly integrate into their daily life? What would they actually use vs. what would collect dust?

**Emotional Resonance**: Based on the relationship and occasion, what would create a genuine emotional moment?

**The "They Get Me" Factor**: What gift would make them think "Wow, they really understand who I am"?

**Aspiration & Growth**: Is there something that aligns with who they're becoming, not just who they are?

## Response Structure

### 🎯 Gift Profile

Write 4-5 sentences analyzing this person as a gift recipient. What type of gifts resonate with them? What's the key insight that should drive your recommendations? What emotional tone should the gift strike?

---

### Top Recommendations

For each of your 5 gift recommendations, use this exact format:

**1. [Specific Gift Name]**

[2-3 sentences explaining exactly what this gift is. Be specific—include brands, types, variations where relevant. Paint a picture of the actual item.]

*Why this is perfect for them:*
[2-3 sentences connecting this gift to specific details about who they are. Reference their personality, interests, or situation directly. Make it clear this isn't a generic suggestion.]

*Budget & Sourcing:*
• Estimated cost: $XX - $XX
• Where to look: [2-3 specific retailer suggestions]
• Pro tip: [One helpful buying tip if applicable]

---

[Repeat for gifts 2-5, with decreasing rank priority]

---

### 🎲 Wild Card

**[Unexpected Gift Idea]**

[Description and reasoning for a creative, outside-the-box option that might be unexpectedly perfect.]

---

### 💡 Gift-Giving Tips for This Person

End with 2-3 personalized tips about HOW to give this person a gift (presentation, timing, accompanying gestures) based on their personality.

## Quality Standards

1. **Specificity**: Never say "a nice book" — say "The Thursday Murder Club by Richard Osman" or "a first-edition of their favorite childhood book"

2. **Personalization**: Every recommendation must reference at least one specific detail from the input

3. **Price Honesty**: Give realistic ranges. Acknowledge that prices vary and should be verified

4. **Avoid Clichés**: No generic candles, gift cards, or wine unless the profile specifically indicates they'd love these

5. **Consider the Relationship**: A gift from a spouse should feel different than one from a coworker

6. **Balance**: Mix of price points within budget, mix of practical and emotional

## Tone

Warm, confident, and genuinely enthusiastic—like a friend with impeccable taste who's excited to help you nail this gift."""


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
• **Recipient**: {recipient}
• **Age**: {age if age else "Not specified"}
• **Relationship**: {relationship}
• **Occasion**: {occasion}
• **Budget**: {budget_str}
• **How well I know them**: {how_well}

## Their Personality & Identity
{personality}

## Interests & Hobbies
{interests}

## Lifestyle & Current Situation
{lifestyle if lifestyle else "Not specified"}

## What They Value Most
{values if values else "Not specified"}

## Gift-Giving Insights
• **How they feel appreciated**: {love_language}
• **Gift style that resonates**: {gift_style}
• **Past gift wins**: {previous_hits if previous_hits else "None shared"}
• **Past gift misses**: {previous_misses if previous_misses else "None shared"}

## Additional Context
• **Things they've mentioned wanting**: {mentioned_wants if mentioned_wants else "Nothing specific"}
• **Things to avoid**: {avoid if avoid else "Nothing specific"}
• **Other context**: {other_context if other_context else "None"}

Please analyze this person thoroughly and provide your best gift recommendations."""

        # Call the API
        with st.spinner("🎁 Analyzing their personality and curating perfect matches..."):
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
                st.info("**💡 Pricing Note:** All prices are estimates based on typical retail ranges. Prices vary by retailer, location, and time—please verify before purchasing.")
                
            except Exception as e:
                st.error(f"Something went wrong: {str(e)}")
                st.markdown("Please check your API key in Streamlit secrets and try again.")

# Footer
st.divider()
st.caption("Built for Professor Hindman's AI Revolution course at GWU | Powered by Claude AI")
