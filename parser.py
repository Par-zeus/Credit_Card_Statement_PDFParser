"""
Credit Card Statement Parser
Supports 5 major credit card issuers:
1. American Express
2. Chase
3. Citibank
4. HDFC Bank
5. ICICI Bank
"""

import re
import pdfplumber
from datetime import datetime
from typing import Dict, Optional, List
import PyPDF2


class CreditCardParser:
    """Main parser class for credit card statements"""
    
    # Supported issuers
    SUPPORTED_ISSUERS = [
        "American Express",
        "Chase",
        "Citibank", 
        "HDFC Bank",
        "ICICI Bank"
    ]
    
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.text_content = ""
        self.issuer = None
        
    def extract_text(self) -> str:
        """Extract text from PDF using pdfplumber"""
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
                self.text_content = text
                return text
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
    
    def identify_issuer(self) -> str:
        """Identify the credit card issuer from the statement"""
        text_lower = self.text_content.lower()
        
        # Check for issuer patterns
        if "american express" in text_lower or "amex" in text_lower:
            self.issuer = "American Express"
        elif "chase" in text_lower and ("credit card" in text_lower or "visa" in text_lower or "mastercard" in text_lower):
            self.issuer = "Chase"
        elif "citibank" in text_lower or "citi" in text_lower:
            self.issuer = "Citibank"
        elif "hdfc" in text_lower:
            self.issuer = "HDFC Bank"
        elif "icici" in text_lower:
            self.issuer = "ICICI Bank"
        else:
            self.issuer = "Unknown"
            
        return self.issuer
    
    def extract_card_last_four(self) -> Optional[str]:
        """Extract last 4 digits of card number"""
        patterns = [
            r'(?:card|account)[\s#:]*(?:ending|number)?[\s#:]*[xX*]{4,12}(\d{4})',
            r'[xX*]{4,12}[\s-]?(\d{4})',
            r'(\d{4})[\s]*(?:card|account)',
            r'account[\s]+number[\s:]*[xX*]+(\d{4})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, self.text_content, re.IGNORECASE)
            if match:
                return match.group(1)
        return None
    
    def extract_billing_cycle(self) -> Optional[Dict[str, str]]:
        """Extract billing cycle dates"""
        # Common patterns for billing cycle
        patterns = [
            r'(?:billing|statement)[\s]+(?:period|cycle|date)[\s:]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})[\s]*(?:to|-|through)[\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
            r'statement[\s]+from[\s:]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})[\s]*(?:to|-|through)[\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
            r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})[\s]*(?:to|-|through)[\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, self.text_content, re.IGNORECASE)
            if match:
                return {
                    "start_date": match.group(1),
                    "end_date": match.group(2)
                }
        return None
    
    def extract_payment_due_date(self) -> Optional[str]:
        """Extract payment due date"""
        patterns = [
            r'(?:payment|pay)[\s]+due[\s]+(?:date|by)[\s:]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
            r'due[\s]+date[\s:]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
            r'please[\s]+pay[\s]+by[\s:]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, self.text_content, re.IGNORECASE)
            if match:
                return match.group(1)
        return None
    
    def extract_total_amount_due(self) -> Optional[str]:
        """Extract total amount due"""
        patterns = [
            r'(?:total|new|amount)[\s]+(?:balance|due|amount due)[\s:]*(?:Rs\.?|INR|USD|\$)?[\s]*([0-9,]+\.?\d*)',
            r'(?:amount|payment)[\s]+due[\s:]*(?:Rs\.?|INR|USD|\$)?[\s]*([0-9,]+\.?\d*)',
            r'(?:minimum|total)[\s]+(?:payment|amount)[\s]+due[\s:]*(?:Rs\.?|INR|USD|\$)?[\s]*([0-9,]+\.?\d*)',
            r'new[\s]+balance[\s:]*(?:Rs\.?|INR|USD|\$)?[\s]*([0-9,]+\.?\d*)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, self.text_content, re.IGNORECASE)
            if match:
                amount = match.group(1).replace(',', '')
                return amount
        return None
    
    def extract_transactions(self) -> List[Dict]:
        """Extract transaction details (sample transactions)"""
        transactions = []
        
        # Pattern for transaction lines
        # Date | Description | Amount
        pattern = r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})[\s]+([A-Za-z\s\*&\-\.]+?)[\s]+(?:Rs\.?|INR|USD|\$)?[\s]*([0-9,]+\.?\d{2})'
        
        matches = re.finditer(pattern, self.text_content, re.MULTILINE)
        
        for match in matches:
            transaction = {
                "date": match.group(1),
                "description": match.group(2).strip(),
                "amount": match.group(3).replace(',', '')
            }
            transactions.append(transaction)
            
            # Limit to first 10 transactions for display
            if len(transactions) >= 10:
                break
        
        return transactions
    
    def parse(self) -> Dict:
        """Main parsing method - extracts all 5 data points"""
        # Extract text
        self.extract_text()
        
        # Identify issuer
        issuer = self.identify_issuer()
        
        # Extract 5 key data points
        result = {
            "issuer": issuer,
            "card_last_four": self.extract_card_last_four(),
            "billing_cycle": self.extract_billing_cycle(),
            "payment_due_date": self.extract_payment_due_date(),
            "total_amount_due": self.extract_total_amount_due(),
            "transactions": self.extract_transactions()
        }
        
        return result


def parse_statement(pdf_path: str) -> Dict:
    """Convenience function to parse a credit card statement"""
    parser = CreditCardParser(pdf_path)
    return parser.parse()
