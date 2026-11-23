
"""
PassiveRoast 💀
Because not every thought deserves to be sent.

An MCP server that detects passive-aggressive messages
and translates corporate drama into human language.
"""

import re
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("PassiveRoast")

# Passive-aggressive phrase database
PHRASES = {
    "obviously": ("You're making this sound obvious.", 2),
    "as i already said": ("I'm getting tired of repeating myself.", 3),
    "as mentioned before": ("We've discussed this already.", 2),
    "per my last email": ("Please read my previous email.", 3),
    "with all due respect": ("I strongly disagree with you.", 3),
    "interesting choice": ("I probably wouldn't have chosen that.", 2),
    "no offense": ("Something potentially offensive is coming.", 2),
    "just saying": ("I want to criticize this without owning it.", 2),
    "if you say so": ("I don't agree, but I'm done arguing.", 3),
    "whatever": ("I have officially given up.", 3),
    "fine": ("This might not actually be fine.", 2),
    "sure...": ("My enthusiasm is currently missing.", 2),
    "thanks in advance": ("I'm expecting you to do this.", 1),
    "asap": ("I would like this done immediately.", 1),
    "noted": ("I acknowledge your message, emotionally unavailable edition.", 2),
    "no worries": ("There may, in fact, be worries.", 1),
    "just following up": ("I'm wondering why you haven't replied.", 1),
    "like i said": ("Please listen this time.", 2),
    "i'm not angry": ("There is a possibility of anger.", 2),
    "per usual": ("This is apparently a recurring problem.", 2),
}

# Professional alternatives
REPLACEMENTS = {
    "as i already said": "As a reminder",
    "as mentioned before": "To clarify",
    "per my last email": "Following up on my previous message",
    "with all due respect": "I see this differently",
    "no offense": "I want to be honest",
    "just saying": "One thing to consider",
    "if you say so": "Understood",
    "whatever": "Let's move forward",
    "like i said": "To reiterate",
    "obviously": "Clearly",
    "noted": "Thanks for letting me know",
    "just following up": "I wanted to check in",
    "fine": "That works for me",
}


def analyze_message(message: str):
    """Analyze a message and calculate its drama score."""

    lower = message.lower()
    found = []
    score = 0

    for phrase, (meaning, weight) in PHRASES.items():
        if phrase in lower:
            found.append({
                "phrase": phrase,
                "translation": meaning,
                "weight": weight
            })
            score += weight

    # Additional drama signals
    if "!!!" in message:
        score += 1

    if re.search(r"\b[A-Z]{4,}\b", message):
        score += 1

    if message.count("?") >= 3:
        score += 1

    return min(score, 10), found


def professional_rewrite(message: str):
    """Replace suspicious phrases with more professional alternatives."""

    result = message

    for phrase, replacement in REPLACEMENTS.items():
        result = re.sub(
            re.escape(phrase),
            replacement,
            result,
            flags=re.IGNORECASE
        )

    result = re.sub(r"!{2,}", ".", result)
    result = re.sub(r"\?{3,}", "?", result)

    return result.strip()


def get_verdict(score: int):
    """Return a funny verdict based on the drama score."""

    if score == 0:
        return (
            "ANGEL MODE 😇",
            "No obvious passive-aggressive signals. Suspiciously wholesome."
        )

    elif score <= 3:
        return (
            "SLIGHTLY SPICY 🌶️",
            "A little attitude. Nothing a diplomatic rewrite can't fix."
        )

    elif score <= 6:
        return (
            "CORPORATE WARFARE 🥷",
            "This message has a LinkedIn smile and a hidden agenda."
        )

    else:
        return (
            "EMOTIONAL DAMAGE 💀",
            "Someone needs a coffee break before pressing Send."
        )


@mcp.tool()
def vibe_check(message: str) -> str:
    """
    Analyze a message for passive-aggressive language.

    Returns:
    - Drama score
    - Funny verdict
    - Detected phrases
    - Professional rewrite
    """

    if not message or not message.strip():
        return "💀 Empty message. Even the drama is missing."

    if len(message) > 5000:
        return "Please keep your message under 5000 characters."

    score, found = analyze_message(message)
    verdict, roast = get_verdict(score)

    output = [
        "💀 PASSIVEROAST",
        "=" * 35,
        f"DRAMA SCORE: {score}/10",
        f"VERDICT: {verdict}",
        f"ROAST: {roast}",
        "",
        "🔍 DETECTED PHRASES:"
    ]

    if found:
        for item in found:
            output.append(
                f"• '{item['phrase']}' → {item['translation']}"
            )
    else:
        output.append("• Nothing suspicious detected.")

    output.extend([
        "",
        "✨ PROFESSIONAL VERSION:",
        professional_rewrite(message),
        "",
        "🧠 FINAL ADVICE:",
        "Read your message one more time before sending.",
        "Remember: screenshots are forever. 💀"
    ])

    return "\n".join(output)


@mcp.tool()
def generate_reply(situation: str, tone: str = "polite") -> str:
    """
    Help the user write a reply to an awkward situation.

    Available tones:
    polite, funny, direct, professional, savage
    """

    if not situation or not situation.strip():
        return "Please describe the situation first."

    if len(situation) > 3000:
        return "Please keep the situation under 3000 characters."

    allowed_tones = [
        "polite",
        "funny",
        "direct",
        "professional",
        "savage"
    ]

    tone = tone.lower().strip()

    if tone not in allowed_tones:
        return (
            "Invalid tone. Choose from: "
            + ", ".join(allowed_tones)
        )

    return (
        "Help the user respond to this situation:\n\n"
        f"{situation}\n\n"
        f"Requested tone: {tone}\n\n"
        "Write a natural, context-aware reply. "
        "Keep it appropriate and avoid unnecessary hostility."
    )


if __name__ == "__main__":
    mcp.run()
