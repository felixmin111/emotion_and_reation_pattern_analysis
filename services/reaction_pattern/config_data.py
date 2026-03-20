LABEL_TEMPLATES = {

    # ---------------------------
    # LESS HELPFUL PATTERNS
    # ---------------------------

    "avoidance_withdrawal": [
        "I avoided the situation instead of facing it",
        "I stayed away from everyone",
        "I ignored the problem",
        "I ran away from my responsibilities",
        "I isolated myself to escape",
        "I withdrew and did not respond",
        "I avoided dealing with my emotions"
    ],

    "rumination_worry": [
        "I kept overthinking about it",
        "I worried about it all day",
        "I could not stop thinking about the problem",
        "I kept replaying the situation in my mind",
        "I felt anxious and mentally stuck",
        "My thoughts kept looping",
        "I felt constant worry"
    ],

    "emotional_dysregulation": [
        "I yelled at someone",
        "I lost control of my emotions",
        "I shouted in anger",
        "I snapped at someone",
        "I exploded emotionally",
        "I reacted impulsively"
    ],

    "numbing_distraction": [
        "I distracted myself to avoid feeling",
        "I scrolled mindlessly for hours",
        "I binge watched to escape my thoughts",
        "I wasted time online instead of facing it",
        "I used entertainment to numb my feelings",
        "I avoided thinking by using social media"
    ],

    "trauma_rumination": [
        "Past trauma still affects me",
        "Old wounds still hurt today",
        "Childhood rejection still impacts me",
        "I cannot move on from past pain",
        "Memories from the past still trigger me",
        "Unresolved trauma influences my life"
    ],

    # ---------------------------
    # ADAPTIVE / HELPFUL PATTERNS
    # ---------------------------

    "problem_focused_coping": [
        "I made a plan and worked step by step",
        "I took action to solve the issue",
        "I handled the situation calmly",
        "I fixed the problem gradually",
        "I decided what to do and executed it",
        "I approached the challenge systematically",
        "I completed my tasks one by one"
    ],

    "emotion_regulation_mindfulness": [
        "I practiced meditation to calm down",
        "I focused on my breathing",
        "I regulated my emotions mindfully",
        "I accepted my feelings without judgment",
        "I tried to calm myself before reacting",
        "I stayed present and aware",
        "I grounded myself emotionally"
    ],

    "support_seeking": [
        "I talked to someone for support",
        "I shared my feelings with a friend",
        "I asked for help",
        "I reached out to family",
        "I sought advice from someone",
        "I did not handle it alone"
    ],

    "cognitive_reappraisal": [
        "I tried to see the positive side",
        "I reframed the situation differently",
        "I found meaning in the experience",
        "I changed my perspective",
        "I looked for the lesson in it",
        "I transformed negative thoughts into growth"
    ],

    "grief_loss_processing": [
        "I felt deep sadness because someone died",
        "I experienced grief and loss",
        "I mourned the death of someone I love",
        "I felt pain from losing someone",
        "I miss someone who passed away",
        "I am processing loss"
    ],

    "achievement_mastery": [
        "I felt proud of my accomplishment",
        "I completed my work successfully",
        "I achieved my goal",
        "I finished everything I planned",
        "I felt satisfied with my effort",
        "I made progress and felt confident",
        "I worked hard and felt proud"
    ],

    "positive_reflection_meaning": [
        "I reflected positively on my life",
        "I felt grateful for my past",
        "I appreciate my supportive family",
        "I remembered good memories warmly",
        "I found comfort in positive experiences",
        "I felt thankful for my journey",
        "I see meaning in my life story"
    ]
}

REACTION_PATTERNS = {

    # LESS HELPFUL

    "avoidance_withdrawal": {
        "single": [
            "avoid", "ignored", "ignore", "withdraw", "withdrew",
            "escape", "isolated", "isolate", "hide"
        ],
        "phrase": [
            "stayed away",
            "ran away",
            "shut myself off",
            "kept distance",
            "did not face"
        ]
    },

    "rumination_worry": {
        "single": [
            "worry", "worried", "anxious", "anxiety",
            "overthink", "regret"
        ],
        "phrase": [
            "cannot stop thinking",
            "kept thinking",
            "over and over",
            "thinking all day"
        ]
    },

    "emotional_dysregulation": {
        "single": [
            "yell", "shout", "snap", "explode"
        ],
        "phrase": [
            "lost control",
            "lost my temper",
            "raised my voice"
        ]
    },

    "numbing_distraction": {
        "single": [
            "scroll", "doomscroll", "binge"
        ],
        "phrase": [
            "waste time",
            "binge watch",
            "mindlessly scrolling",
            "avoid my feelings"
        ]
    },

    "trauma_rumination": {
        "single": [
            "trauma", "triggered"
        ],
        "phrase": [
            "still affects me",
            "cannot move on",
            "old wound",
            "past still hurts"
        ]
    },

    # HELPFUL

    "problem_focused_coping": {
        "single": [
            "plan", "decide", "solve", "fix", "handle"
        ],
        "phrase": [
            "step by step",
            "made a plan",
            "worked on",
            "took action",
            "finished everything"
        ]
    },

    "emotion_regulation_mindfulness": {
        "single": [
            "meditate", "breathe", "calm", "relax"
        ],
        "phrase": [
            "stay calm",
            "focused on breathing",
            "accepted my feelings",
            "let it go"
        ]
    },

    "support_seeking": {
        "single": [
            "shared", "asked", "talked"
        ],
        "phrase": [
            "asked for help",
            "talked to",
            "reached out",
            "opened up"
        ]
    },

    "cognitive_reappraisal": {
        "single": [
            "learned", "realized"
        ],
        "phrase": [
            "found the good side",
            "changed my perspective",
            "looked differently",
            "found meaning",
            "changed my mindset"
        ]
    },

    "grief_loss_processing": {
        "single": [
            "died", "loss", "miss"
        ],
        "phrase": [
            "passed away",
            "car accident",
            "lost someone"
        ]
    },

    "achievement_mastery": {
        "single": [
            "proud", "achieved", "completed", "finished"
        ],
        "phrase": [
            "felt proud",
            "finished my work",
            "made progress",
            "did it successfully"
        ]
    },

    "positive_reflection_meaning": {
        "single": [
            "grateful", "thankful"
        ],
        "phrase": [
            "supportive family",
            "good childhood",
            "positive memory",
            "feel blessed"
        ]
    }
}

REACTION_PATTERNS["social_comparison_envy"] = {
    "single": [
        "envy", "envious", "jealous", "jealousy",
        "insecure", "resent", "resentful",
        "compare", "comparison", "competitive",
        "bitter", "bitterness"
    ],
    "phrase": [
        "feel jealous",
        "feel envy",
        "instead of proud",
        "why not me",
        "i wish i had",
        "compare myself",
        "compare to my friend",
        "not happy for",
        "green with envy"
    ]
}

LABEL_WEIGHTS = {

    # Less helpful
    "grief_loss_processing": 1.6,
    "trauma_rumination": 1.5,
    "rumination_worry": 1.4,
    "emotional_dysregulation": 1.3,
    "avoidance_withdrawal": 1.2,
    "numbing_distraction": 1.1,

    # Helpful
    "problem_focused_coping": 1.2,
    "cognitive_reappraisal": 1.3,
    "emotion_regulation_mindfulness": 1.2,
    "support_seeking": 1.1,
    "achievement_mastery": 1.2,
    "positive_reflection_meaning": 1.1
}

NEG_WORDS = {"not", "never", "no", "n't"}