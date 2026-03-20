PROTOTYPES = {
    "family": [
        "I talked with my mother and father about home problems.",
        "My family situation made me feel emotional.",
        "I spent time with my parents, siblings, or relatives.",
        "There was tension or support inside my family.",
        "I had concerns about my child, parent, or family responsibilities."
    ],
    "health": [
        "I felt sick, tired, stressed, or physically unwell.",
        "I exercised, rested, or focused on my health.",
        "I had body pain, illness, sleep problems, or recovery concerns.",
        "I thought about my mental health and physical wellbeing.",
        "I tried to take care of my body and mind."
    ],
    "money": [
        "I worried about money, savings, bills, or expenses.",
        "I thought about salary, debt, or financial planning.",
        "I needed to manage my budget and spending.",
        "There was pressure related to income or cost of living.",
        "I was concerned about my financial future."
    ],
    "work_study": [
        "I was busy with work, study, deadlines, or responsibilities.",
        "I had tasks, meetings, assignments, or exams to finish.",
        "I felt pressure from my job or school work.",
        "I wanted to improve my performance at work or in class.",
        "My productivity and career goals were on my mind."
    ],
    "relationship": [
        "I thought about my boyfriend, girlfriend, partner, or romantic relationship.",
        "There was conflict, distance, or closeness in my relationship.",
        "I felt hurt, loved, or uncertain about someone I love.",
        "My romantic life affected my emotions.",
        "I wanted understanding and connection with my partner."
    ],
    "personal_growth": [
        "I reflected on self-improvement and personal growth.",
        "I wanted to become stronger, wiser, and more confident.",
        "I learned something meaningful about myself.",
        "I tried to heal, grow, and understand my emotions.",
        "I worked on my habits, mindset, and inner development."
    ],
    "social": [
        "I spent time with friends or people around me.",
        "I felt connected or disconnected from others.",
        "There were social situations that affected me emotionally.",
        "I thought about friendship, communication, and belonging.",
        "My interaction with other people influenced my day."
    ]
}

KEYWORDS = {
    "family": {
        "strong": {
            "mother", "father", "mom", "mum", "dad", "parent", "parents",
            "sister", "brother", "siblings", "family", "relative", "relatives",
            "child", "children", "son", "daughter", "home"
        },
        "weak": {
            "house", "support", "care", "responsibility", "marriage", "family issue"
        }
    },
    "health": {
        "strong": {
            "health", "sick", "ill", "pain", "body", "exercise", "sleep",
            "tired", "stress", "stressed", "anxiety", "depression", "medicine",
            "hospital", "doctor", "therapy", "rest"
        },
        "weak": {
            "walk", "gym", "eat", "food", "wellness", "healing", "mental", "physical"
        }
    },
    "money": {
        "strong": {
            "money", "salary", "income", "debt", "bill", "bills", "expense",
            "expenses", "budget", "rent", "loan", "financial", "cash", "savings"
        },
        "weak": {
            "cost", "price", "buy", "bought", "payment", "paid", "finance"
        }
    },
    "work_study": {
        "strong": {
            "work", "job", "office", "boss", "project", "deadline", "meeting",
            "assignment", "study", "school", "class", "exam", "teacher", "student"
        },
        "weak": {
            "task", "career", "learn", "learning", "presentation", "training", "performance"
        }
    },
    "relationship": {
        "strong": {
            "boyfriend", "girlfriend", "partner", "husband", "wife", "lover",
            "relationship", "love", "breakup", "broke up", "romantic"
        },
        "weak": {
            "heart", "close", "distance", "attachment", "together", "separate"
        }
    },
    "personal_growth": {
        "strong": {
            "growth", "improve", "improvement", "healing", "heal", "self",
            "mindset", "confidence", "purpose", "goal", "reflection", "reflected"
        },
        "weak": {
            "learned", "realized", "realised", "change", "habit", "discipline", "inner"
        }
    },
    "social": {
        "strong": {
            "friend", "friends", "people", "social", "community", "team", "group"
        },
        "weak": {
            "talked", "conversation", "chat", "connection", "belonging", "others"
        }
    }
}

DEFAULT_TOP_K = 3
DEFAULT_ALPHA = 0.65  # semantic weight
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
MODEL_STORE_DIRNAME = "model_store"
PROTOTYPE_CACHE_FILENAME = "prototype_embeddings.pkl"