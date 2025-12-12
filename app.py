import streamlit as st
import anthropic

# Page configuration
st.set_page_config(
    page_title="Perfect Gift Finder",
    page_icon="🎁",
    layout="centered"
)

# Title and introduction
st.title("🎁 Perfect Gift Finder")
st.markdown("*Find thoughtful, personalized gift ideas in seconds*")
st.divider()

# The system prompt (your refined instructions for Claude)
SYSTEM_PROMPT = """You are a thoughtful, creative gift recommendation assistant. Your goal is to suggest personalized, meaningful gifts that show the giver truly understands the recipient.

## How You Approach Gift Selection

1. **Analyze the recipient**: Consider their personality, interests, lifestyle, and what would genuinely delight them—not just generic options.

2. **Consider the relationship**: A gift for a close friend differs from one for a coworker or distant relative. Match the intimacy level appropriately.

3. **Factor in the occasion**: Birthday gifts feel different from thank-you gifts or holiday presents. The occasion shapes the tone.

4. **Avoid past repeats**: If previous gifts are mentioned, don't suggest the same thing. Instead, build on what worked or try a fresh direction.

5. **Respect the budget**: All suggestions must fall within the stated range. Include a mix across the budget when possible.

## Your Response Format

For each recommendation, provide:
- **Gift idea**: Clear, specific suggestion (not vague categories)
- **Why it fits**: 1-2 sentences connecting the gift to something specific about the recipient
- **Approximate price**: Estimated cost
- **Where to find it**: General sourcing suggestion (e.g., "local bookstores," "Etsy," "Amazon")

Provide 5 gift recommendations, ranked from your top pick to your fifth pick. After your recommendations, include a "Wild Card" option—something unexpected that might be perfect if the giver wants to take a creative risk.

## Your Tone
Warm, helpful, and conversational—like a friend who's great at gift-giving brainstorming with you. Avoid sounding like a generic shopping algorithm."""

# Create the input form
with st.form("gift_form"):
    st.subheader("Tell me about the gift recipient")
    
    col1, col2 = st.columns(2)
    
    with col1:
        recipient = st.text_input(
            "Who is this gift for?",
            placeholder="e.g., My mom, My best friend Jake"
        )
        
        age = st.text_input(
            "Their age (approximate)",
            placeholder="e.g., 35, late 20s, teenager"
        )
        
        relationship = st.selectbox(
            "Your relationship",
            ["Close friend", "Parent", "Sibling", "Partner/Spouse", 
             "Coworker", "Boss", "Acquaintance", "Extended family", "Child", "Other"]
        )
    
    with col2:
        occasion = st.selectbox(
            "What's the occasion?",
            ["Birthday", "Christmas/Holiday", "Thank you", "Anniversary",
             "Graduation", "Wedding", "Baby shower", "Housewarming", 
             "Just because", "Valentine's Day", "Mother's Day", "Father's Day", "Other"]
        )
        
        budget = st.select_slider(
            "Your budget",
            options=["Under $25", "$25-50", "$50-100", "$100-200", "$200-500", "$500+"]
        )
        
        how_well = st.selectbox(
            "How well do you know them?",
            ["Extremely well", "Pretty well", "Somewhat", "Not very well", "Barely know them"]
        )
    
    st.subheader("More about them")
    
    personality = st.text_area(
        "Describe their personality",
        placeholder="e.g., Introverted, loves quiet nights in, very practical, hates clutter...",
        height=80
    )
    
    interests = st.text_area(
        "Their interests and hobbies",
        placeholder="e.g., Cooking, hiking, true crime podcasts, vintage fashion, photography...",
        height=80
    )
    
    lifestyle = st.text_input(
        "Their lifestyle",
        placeholder="e.g., Busy working mom, college student, recent retiree, always traveling..."
    )
    
    st.subheader("Additional context")
    
    previous_gifts = st.text_area(
        "Previous gifts you've given them (to avoid repeats)",
        placeholder="e.g., Last year I gave her a nice candle, year before that a cookbook...",
        height=80
    )
    
    avoid = st.text_input(
        "Anything to avoid?",
        placeholder="e.g., No food (allergies), already has too many books, hates jewelry..."
    )
    
    other_context = st.text_area(
        "Any other helpful context?",
        placeholder="e.g., She mentioned wanting to learn guitar, they just moved to a new apartment...",
        height=80
    )
    
    # Submit button
    submitted = st.form_submit_button("🎁 Find Perfect Gifts", use_container_width=True)

# Process the form when submitted
if submitted:
    # Check that required fields are filled
    if not recipient or not personality or not interests:
        st.error("Please fill in at least the recipient, personality, and interests fields!")
    else:
        # Build the user message from the form inputs
        user_message = f"""Help me find a gift for someone. Here's what I know:

**Recipient**: {recipient}
**Age**: {age if age else "Not specified"}
**Their personality**: {personality}
**Their interests/hobbies**: {interests}
**Their lifestyle**: {lifestyle if lifestyle else "Not specified"}

**Occasion**: {occasion}
**Your relationship**: {relationship}
**How well you know them**: {how_well}

**Budget**: {budget}

**Previous gifts you've given them**: {previous_gifts if previous_gifts else "None mentioned"}

**Things to avoid**: {avoid if avoid else "Nothing specific"}

**Other context**: {other_context if other_context else "None"}"""

        # Call the Anthropic API
        with st.spinner("Finding perfect gift ideas..."):
            try:
                client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
                
                message = client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=1500,
                    system=SYSTEM_PROMPT,
                    messages=[
                        {"role": "user", "content": user_message}
                    ]
                )
                
                # Display the response
                st.divider()
                st.subheader("🎁 Your Personalized Gift Recommendations")
                st.markdown(message.content[0].text)
                
            except Exception as e:
                st.error(f"Something went wrong: {str(e)}")

# Footer
st.divider()
st.caption("Built for Prof. Hindman's AI Revolution course | Powered by Claude")
