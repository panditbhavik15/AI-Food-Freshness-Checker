"""
Recommendation engine.

Maps freshness classifications to appropriate, carefully worded recommendations.
Includes food-safety disclaimers and visual observation indicators.
"""

from typing import NamedTuple


class FreshnessResult(NamedTuple):
    """Structured freshness analysis output."""
    freshness_class: str
    recommendation: str
    safety_notice: str
    observations: list[str]


# ─────────────────────────────────────────────
# Safety disclaimer — ALWAYS included
# ─────────────────────────────────────────────

SAFETY_NOTICE = (
    "This is a visual AI estimate only. It is not a laboratory food-safety test. "
    "Visual analysis cannot detect bacteria, toxins, or internal spoilage. "
    "Always use your own judgement and follow food-safety guidelines."
)


# ─────────────────────────────────────────────
# Recommendations by freshness class
# ─────────────────────────────────────────────

RECOMMENDATIONS = {
    "FRESH": (
        "No obvious visual spoilage detected. "
        "Store properly to maintain freshness."
    ),
    "AGING": (
        "Visible signs suggest this food may be aging. "
        "Consider using soon and inspect carefully before consumption."
    ),
    "HIGH VISIBLE SPOILAGE RISK": (
        "Visible indicators suggest significant degradation. "
        "Exercise caution and inspect thoroughly. When in doubt, discard."
    ),
}


# ─────────────────────────────────────────────
# Visual observation indicators per food + class
# ─────────────────────────────────────────────

OBSERVATIONS = {
    "apple": {
        "FRESH": [
            "Vibrant, uniform skin color",
            "Firm surface with natural sheen",
            "No visible blemishes or soft spots",
        ],
        "AGING": [
            "Slight dulling of skin color",
            "Minor soft spots detected",
            "Light surface wrinkling beginning",
        ],
        "HIGH VISIBLE SPOILAGE RISK": [
            "Significant brown or dark discoloration",
            "Visible soft or mushy areas",
            "Surface wrinkling and dehydration",
            "Possible mold spots visible",
        ],
    },
    "banana": {
        "FRESH": [
            "Bright yellow color with minimal spots",
            "Firm texture visible",
            "Green tint at stem area (recently ripened)",
        ],
        "AGING": [
            "Increasing brown spots on skin",
            "Darker yellow coloration",
            "Slight softening visible",
        ],
        "HIGH VISIBLE SPOILAGE RISK": [
            "Extensive dark brown or black skin",
            "Visible mushiness or splitting",
            "Possible mold at stem or tips",
            "Strong overall discoloration",
        ],
    },
    "tomato": {
        "FRESH": [
            "Bright, uniform red coloration",
            "Smooth, taut skin surface",
            "Firm appearance without dents",
        ],
        "AGING": [
            "Dark spots beginning to appear",
            "Wrinkled or softening surface",
            "Slight discoloration in areas",
        ],
        "HIGH VISIBLE SPOILAGE RISK": [
            "Significant dark or black spots",
            "Heavy wrinkling and collapse",
            "Visible mold growth",
            "Liquid seepage visible",
        ],
    },
    "potato": {
        "FRESH": [
            "Uniform skin color with no green patches",
            "Firm surface texture",
            "No visible sprouts or eyes growing",
        ],
        "AGING": [
            "Slight sprouting at eye areas",
            "Minor wrinkling of skin",
            "Small green patches appearing",
        ],
        "HIGH VISIBLE SPOILAGE RISK": [
            "Significant green discoloration",
            "Heavy sprouting visible",
            "Soft or mushy areas",
            "Dark spots or possible mold",
        ],
    },
    "orange": {
        "FRESH": [
            "Bright, vibrant orange color",
            "Firm, textured rind",
            "No visible soft spots",
        ],
        "AGING": [
            "Slight dulling of rind color",
            "Minor soft areas developing",
            "Light surface discoloration",
        ],
        "HIGH VISIBLE SPOILAGE RISK": [
            "Significant mold growth visible",
            "Heavy discoloration or darkening",
            "Soft, collapsing areas",
            "Possible white or green mold spots",
        ],
    },
    "carrot": {
        "FRESH": [
            "Bright orange color throughout",
            "Firm, smooth surface",
            "Crisp appearance with no bending",
        ],
        "AGING": [
            "Slight flexibility when bent",
            "Minor surface drying",
            "Slight color fading",
        ],
        "HIGH VISIBLE SPOILAGE RISK": [
            "Significant limpness and bending",
            "Visible sliminess on surface",
            "Dark or black spots",
            "Heavy dehydration and wrinkling",
        ],
    },
    "cucumber": {
        "FRESH": [
            "Bright green, uniform color",
            "Firm texture with slight glossiness",
            "No visible soft spots or yellowing",
        ],
        "AGING": [
            "Yellowing beginning at ends",
            "Slight softening in areas",
            "Minor surface wrinkling",
        ],
        "HIGH VISIBLE SPOILAGE RISK": [
            "Significant yellowing or browning",
            "Visible sliminess on surface",
            "Heavy wrinkling and collapse",
            "Possible mold spots",
        ],
    },
    "strawberry": {
        "FRESH": [
            "Bright red color with vibrant sheen",
            "Firm texture with intact surface",
            "Green, fresh-looking stem and leaves",
        ],
        "AGING": [
            "Darkening of red color",
            "Slight softening",
            "Bruised or dented areas",
            "Stem beginning to brown",
        ],
        "HIGH VISIBLE SPOILAGE RISK": [
            "Visible mold growth (white or gray fuzz)",
            "Significant mushiness",
            "Heavy discoloration or browning",
            "Liquid seepage visible",
        ],
    },
}

# Fallback observations for unknown food categories
FALLBACK_OBSERVATIONS = {
    "FRESH": [
        "No obvious visual signs of degradation",
        "Color appears vibrant and natural",
        "Surface appears firm and intact",
    ],
    "AGING": [
        "Some visual changes detected",
        "Slight discoloration observed",
        "Surface texture changes visible",
    ],
    "HIGH VISIBLE SPOILAGE RISK": [
        "Significant visual degradation detected",
        "Discoloration or dark spots visible",
        "Surface deterioration observed",
    ],
}


def get_recommendation(food_category: str, freshness_class: str) -> FreshnessResult:
    """
    Generate a complete recommendation for a given food and freshness class.

    Args:
        food_category: The identified food (e.g., "tomato")
        freshness_class: One of "FRESH", "AGING", "HIGH VISIBLE SPOILAGE RISK"

    Returns:
        FreshnessResult with recommendation, safety notice, and observations.
    """
    # Get recommendation text
    recommendation = RECOMMENDATIONS.get(
        freshness_class,
        "Unable to generate a specific recommendation. Please inspect the food carefully.",
    )

    # Get observations for the specific food and class
    food_key = food_category.lower().strip()
    food_observations = OBSERVATIONS.get(food_key, FALLBACK_OBSERVATIONS)

    observations = food_observations.get(
        freshness_class, FALLBACK_OBSERVATIONS.get(freshness_class, [])
    )

    return FreshnessResult(
        freshness_class=freshness_class,
        recommendation=recommendation,
        safety_notice=SAFETY_NOTICE,
        observations=observations,
    )
