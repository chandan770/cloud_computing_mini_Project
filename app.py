
import streamlit as st
import re

# Page configuration
st.set_page_config(
    page_title="Review Sentiment Checker",
    page_icon="🎬",
    layout="centered"
)

# App title
st.title("🎬 Movie Review Sentiment Checker")
st.write("Enter a movie or product review to analyze its sentiment.")

# Sentiment keywords
positive_words = {
    "good", "great", "excellent", "amazing", "awesome",
    "love", "loved", "best", "wonderful", "fantastic",
    "enjoyed", "happy", "perfect", "brilliant", "beautiful"
}

negative_words = {
    "bad", "terrible", "worst", "boring", "awful",
    "hate", "hated", "poor", "disappointing", "waste",
    "horrible", "ugly", "slow", "annoying", "stupid"
}

# Review input
review = st.text_area(
    "Enter your review:",
    placeholder="Example: The movie was amazing and I really enjoyed it.",
    height=150
)

# Analyze button
if st.button("Analyze Sentiment", type="primary"):

    if not review.strip():
        st.warning("Please enter a review first.")

    else:
        # Convert to lowercase and extract words
        words = re.findall(r"\b[a-zA-Z']+\b", review.lower())

        # Count sentiment keywords
        positive_count = sum(word in positive_words for word in words)
        negative_count = sum(word in negative_words for word in words)

        # Handle simple negations
        negations = {"not", "never", "no", "isn't", "wasn't", "don't", "didn't"}
        adjusted_positive = 0
        adjusted_negative = 0

        for i, word in enumerate(words):
            previous_words = words[max(0, i - 3):i]
            negated = any(w in negations for w in previous_words)

            if word in positive_words:
                if negated:
                    adjusted_negative += 1
                else:
                    adjusted_positive += 1

            elif word in negative_words:
                if negated:
                    adjusted_positive += 1
                else:
                    adjusted_negative += 1

        # Determine sentiment
        if adjusted_positive > adjusted_negative:
            sentiment = "POSITIVE 😊"
            st.success(f"Predicted Sentiment: {sentiment}")

        elif adjusted_negative > adjusted_positive:
            sentiment = "NEGATIVE 😞"
            st.error(f"Predicted Sentiment: {sentiment}")

        else:
            sentiment = "NEUTRAL 😐"
            st.info(f"Predicted Sentiment: {sentiment}")

        # Display keyword counts
        col1, col2 = st.columns(2)

        col1.metric("Positive Keywords", adjusted_positive)
        col2.metric("Negative Keywords", adjusted_negative)

        # Display submitted review
        st.subheader("Your Review")
        st.write(review)

# Footer
st.divider()
st.caption("Mini Project | NLP and Cloud Computing")
st.caption("Note: This is a basic keyword-based demonstration, not a trained ML model.")
