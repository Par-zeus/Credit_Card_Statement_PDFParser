"""
Utility functions for Credit Card Statement Parser
"""

import re
from datetime import datetime
from typing import Optional


def format_currency(amount: str, currency: str = "INR") -> str:
    """Format amount with currency symbol"""
    currency_symbols = {
        "INR": "₹",
        "USD": "$",
        "EUR": "€",
        "GBP": "£"
    }
    
    symbol = currency_symbols.get(currency, "₹")
    try:
        formatted_amount = f"{float(amount):,.2f}"
        return f"{symbol}{formatted_amount}"
    except (ValueError, TypeError):
        return f"{symbol}{amount}"


def normalize_date(date_str: str) -> Optional[str]:
    """Normalize date string to standard format"""
    if not date_str:
        return None
    
    # Common date formats
    date_formats = [
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%m/%d/%Y",
        "%m-%d-%Y",
        "%d/%m/%y",
        "%d-%m-%y",
        "%Y-%m-%d"
    ]
    
    for fmt in date_formats:
        try:
            date_obj = datetime.strptime(date_str, fmt)
            return date_obj.strftime("%d/%m/%Y")
        except ValueError:
            continue
    
    return date_str


def clean_amount(amount_str: str) -> Optional[float]:
    """Clean and convert amount string to float"""
    if not amount_str:
        return None
    
    try:
        # Remove currency symbols and commas
        cleaned = re.sub(r'[₹$€£,\s]', '', str(amount_str))
        return float(cleaned)
    except (ValueError, TypeError):
        return None


def mask_card_number(card_number: str) -> str:
    """Mask card number showing only last 4 digits"""
    if not card_number or len(card_number) < 4:
        return "****"
    
    return f"****{card_number[-4:]}"


def validate_pdf_file(file_path: str) -> bool:
    """Validate if file is a valid PDF"""
    import os
    
    if not os.path.exists(file_path):
        return False
    
    if not file_path.lower().endswith('.pdf'):
        return False
    
    # Check file size (max 10MB)
    if os.path.getsize(file_path) > 10 * 1024 * 1024:
        return False
    
    return True


def extract_email(text: str) -> Optional[str]:
    """Extract email address from text"""
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    match = re.search(email_pattern, text)
    return match.group(0) if match else None


def extract_phone(text: str) -> Optional[str]:
    """Extract phone number from text"""
    phone_patterns = [
        r'\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
        r'\d{10}',
        r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}'
    ]
    
    for pattern in phone_patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(0)
    
    return None


def calculate_days_until_due(due_date_str: str) -> Optional[int]:
    """Calculate days until payment due date"""
    try:
        normalized = normalize_date(due_date_str)
        if not normalized:
            return None
        
        due_date = datetime.strptime(normalized, "%d/%m/%Y")
        today = datetime.now()
        delta = (due_date - today).days
        
        return delta
    except (ValueError, TypeError):
        return None


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe saving"""
    # Remove invalid characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Replace spaces with underscores
    sanitized = sanitized.replace(' ', '_')
    return sanitized
