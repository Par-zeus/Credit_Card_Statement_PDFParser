"""
Configuration file for Credit Card Statement Parser
Contains patterns and settings for different issuers
"""

# Supported credit card issuers
SUPPORTED_ISSUERS = {
    "American Express": {
        "keywords": ["american express", "amex"],
        "card_pattern": r'card[\s]+(?:ending|number)[\s:]*[xX*]{10,12}(\d{4})',
    },
    "Chase": {
        "keywords": ["chase", "chase bank"],
        "card_pattern": r'account[\s]+number[\s:]*[xX*]+(\d{4})',
    },
    "Citibank": {
        "keywords": ["citibank", "citi"],
        "card_pattern": r'card[\s]+number[\s:]*[xX*]+(\d{4})',
    },
    "HDFC Bank": {
        "keywords": ["hdfc", "hdfc bank"],
        "card_pattern": r'card[\s]+no[\s.:]*[xX*]+(\d{4})',
    },
    "ICICI Bank": {
        "keywords": ["icici", "icici bank"],
        "card_pattern": r'card[\s]+number[\s:]*[xX*]+(\d{4})',
    }
}

# Common regex patterns for data extraction
PATTERNS = {
    "card_last_four": [
        r'(?:card|account)[\s#:]*(?:ending|number)?[\s#:]*[xX*]{4,12}(\d{4})',
        r'[xX*]{4,12}[\s-]?(\d{4})',
        r'(\d{4})[\s]*(?:card|account)',
        r'account[\s]+number[\s:]*[xX*]+(\d{4})',
    ],
    "billing_cycle": [
        r'(?:billing|statement)[\s]+(?:period|cycle|date)[\s:]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})[\s]*(?:to|-|through)[\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
        r'statement[\s]+from[\s:]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})[\s]*(?:to|-|through)[\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
    ],
    "due_date": [
        r'(?:payment|pay)[\s]+due[\s]+(?:date|by)[\s:]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
        r'due[\s]+date[\s:]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
        r'please[\s]+pay[\s]+by[\s:]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
    ],
    "total_due": [
        r'(?:total|new|amount)[\s]+(?:balance|due|amount due)[\s:]*(?:Rs\.?|INR|USD|\$)?[\s]*([0-9,]+\.?\d*)',
        r'(?:amount|payment)[\s]+due[\s:]*(?:Rs\.?|INR|USD|\$)?[\s]*([0-9,]+\.?\d*)',
        r'new[\s]+balance[\s:]*(?:Rs\.?|INR|USD|\$)?[\s]*([0-9,]+\.?\d*)',
    ]
}

# Currency symbols
CURRENCY_SYMBOLS = {
    "INR": "₹",
    "USD": "$",
    "EUR": "€",
    "GBP": "£"
}

# App settings
APP_CONFIG = {
    "title": "Credit Card Statement Parser",
    "page_icon": "💳",
    "layout": "wide",
    "max_file_size_mb": 10,
    "allowed_extensions": ["pdf"],
    "max_transactions_display": 10
}
