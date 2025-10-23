# 💳 Credit Card Statement Parser

A professional PDF parser built with Python and Streamlit that extracts key insights from credit card statements across 5 major issuers.

## 🎯 Project Overview

This project was developed as part of an assignment to demonstrate PDF parsing capabilities. It extracts 5 critical data points from credit card statements and presents them through an intuitive Streamlit interface.

## ✨ Features

### Supported Credit Card Issuers (5)
1. **American Express**
2. **Chase**
3. **Citibank**
4. **HDFC Bank**
5. **ICICI Bank**

### Extracted Data Points (5)
1. **Card Issuer** - Automatically identifies the bank/credit card provider
2. **Card Last 4 Digits** - Extracts the last 4 digits for card identification
3. **Billing Cycle** - Captures the statement period (start and end dates)
4. **Payment Due Date** - Identifies when payment is due
5. **Total Amount Due** - Extracts the outstanding balance

### Additional Features
- **Transaction History** - Extracts sample transactions with dates and amounts
- **Export to JSON** - Download parsed data for further processing
- **Professional UI** - Clean, modern interface built with Streamlit
- **Real-time Parsing** - Instant results upon upload

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Steps

1. **Clone or download this repository**
```bash
cd Credit_card_pdf_parser
```

2. **Create a virtual environment (recommended)**
```bash
python -m venv venv
```

3. **Activate the virtual environment**
```bash
# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

## 🎮 Usage

### Running the Application

1. **Start the Streamlit app**
```bash
streamlit run app.py
```

2. **Access the application**
   - The app will automatically open in your default browser
   - If not, navigate to `http://localhost:8501`

3. **Upload and Parse**
   - Click "Browse files" to upload a credit card statement PDF
   - Click "Parse Statement" to extract data
   - Review the extracted information
   - Download results as JSON if needed

### Using the Parser Programmatically

You can also use the parser module directly in your Python code:

```python
from parser import parse_statement

# Parse a credit card statement
result = parse_statement('path/to/statement.pdf')

# Access extracted data
print(f"Issuer: {result['issuer']}")
print(f"Card Last 4: {result['card_last_four']}")
print(f"Amount Due: {result['total_amount_due']}")
```
<img width="1331" height="611" alt="image" src="https://github.com/user-attachments/assets/a947fafe-89e6-42d4-a499-b2491d33b32c" />
<img width="1329" height="523" alt="image" src="https://github.com/user-attachments/assets/dce1fe28-f2ae-4361-8bb6-1060868a3442" />
<img width="1330" height="556" alt="image" src="https://github.com/user-attachments/assets/561d8f2d-2d67-4051-8b8f-c63f5840bc52" />

## 📂 Project Structure

```
Credit_card_pdf_parser/
│
├── app.py                  # Streamlit web application
├── parser.py               # Core PDF parsing logic
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
└── .gitignore             # Git ignore rules
```

## 🛠️ Technical Implementation

### Architecture
- **Frontend**: Streamlit for interactive UI
- **PDF Processing**: pdfplumber and PyPDF2 for text extraction
- **Pattern Matching**: Regular expressions for data extraction
- **Data Handling**: Pandas for structured data representation

### Key Components

#### 1. PDF Text Extraction
Uses `pdfplumber` for robust text extraction from PDF files with various formats.

#### 2. Issuer Identification
Pattern matching against known issuer identifiers in the statement text.

#### 3. Data Point Extraction
Multiple regex patterns for each data point to handle different statement formats:
- Card numbers with various masking patterns
- Date formats (MM/DD/YYYY, DD-MM-YYYY, etc.)
- Currency amounts with different notations

#### 4. Transaction Parsing
Extracts transaction details including date, description, and amount.

## 📊 Demo & Testing

### Testing with Sample Statements
1. Obtain credit card statement PDFs from supported issuers
2. Ensure PDFs are not password-protected
3. Upload through the Streamlit interface
4. Verify extracted data accuracy

### Expected Output Format
```json
{
  "issuer": "HDFC Bank",
  "card_last_four": "1234",
  "billing_cycle": {
    "start_date": "01/12/2024",
    "end_date": "31/12/2024"
  },
  "payment_due_date": "15/01/2025",
  "total_amount_due": "15000.00",
  "transactions": [
    {
      "date": "05/12/2024",
      "description": "Amazon Purchase",
      "amount": "2500.00"
    }
  ]
}
```

## ⚠️ Limitations & Considerations

- **PDF Format**: Works best with text-based PDFs (not scanned images)
- **Pattern Variations**: Different statement formats may require pattern adjustments
- **Data Quality**: Accuracy depends on PDF text extraction quality
- **Issuer Support**: Limited to 5 configured issuers
- **Language**: Optimized for English statements

## 🔒 Security & Privacy

- All processing is done **locally** on your machine
- No data is sent to external servers
- Temporary files are automatically deleted after parsing
- Recommended for demonstration purposes only

## 🎓 Learning Outcomes

This project demonstrates:
- PDF text extraction and processing
- Pattern matching with regular expressions
- Building interactive web applications with Streamlit
- Handling real-world data parsing challenges
- Professional code organization and documentation

## 🔧 Troubleshooting

### Common Issues

**Error: "ModuleNotFoundError"**
- Ensure all dependencies are installed: `pip install -r requirements.txt`

**Error: "PDF extraction failed"**
- Check if PDF is password-protected
- Verify PDF contains extractable text (not just images)

**"Not Found" for data points**
- Statement format may differ from expected patterns
- Try a statement from a supported issuer

**Streamlit not opening**
- Manually navigate to `http://localhost:8501`
- Check if port 8501 is available

## 📈 Future Enhancements

Potential improvements for production use:
- OCR support for scanned PDFs
- Machine learning for improved extraction accuracy
- Support for more credit card issuers
- Multi-language support
- Batch processing capabilities
- Database integration for historical tracking

## 📝 Assignment Submission

### Deliverables
✅ Functional PDF parser for 5 credit card issuers  
✅ Extraction of 5 key data points  
✅ Professional Streamlit interface  
✅ Clean, documented code  
✅ Comprehensive README  

### Demonstration Points
1. **Functionality**: Upload and parse statements from multiple issuers
2. **Code Quality**: Well-structured, commented, and maintainable
3. **User Experience**: Intuitive interface with clear data presentation
4. **Error Handling**: Graceful handling of edge cases
5. **Documentation**: Complete usage and technical documentation

## 👤 Author

Parth Das - SEM-VIII Project

## 📄 License

This project is created for educational and demonstration purposes.

---

**Built with ❤️ using Python, Streamlit, and modern PDF parsing libraries**
