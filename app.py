"""
Streamlit App for Credit Card Statement Parser
Professional UI for demonstrating PDF parsing capabilities
"""

import streamlit as st
import pandas as pd
from parser import parse_statement
import os
from datetime import datetime
import tempfile

# Page configuration
st.set_page_config(
    page_title="Credit Card Statement Parser",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stAlert {
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    h1 {
        color: #1f77b4;
    }
    .dataframe {
        font-size: 14px;
    }
    </style>
""", unsafe_allow_html=True)


def main():
    # Header
    st.title("💳 Credit Card Statement Parser")
    st.markdown("### Extract key insights from credit card statements with AI-powered parsing")
    
    # Sidebar
    with st.sidebar:
        st.header("📋 About")
        st.markdown("""
        This parser extracts **5 key data points** from credit card statements:
        
        1. **Card Issuer** - Identifies the bank/provider
        2. **Card Last 4 Digits** - Card identification
        3. **Billing Cycle** - Statement period
        4. **Payment Due Date** - When payment is due
        5. **Total Amount Due** - Outstanding balance
        """)
        
        st.header("🏦 Supported Issuers")
        issuers = [
            "American Express",
            "Chase",
            "Citibank",
            "HDFC Bank",
            "ICICI Bank"
        ]
        for issuer in issuers:
            st.markdown(f"✓ {issuer}")
        
        st.markdown("---")
        st.markdown("**Built with:** Streamlit, PyPDF2, pdfplumber")
        st.markdown("**Version:** 1.0.0")
    
    # Main content
    st.markdown("---")
    
    # File upload
    st.subheader("📄 Upload Credit Card Statement")
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=['pdf'],
        help="Upload your credit card statement in PDF format"
    )
    
    if uploaded_file is not None:
        # Display file info
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"📁 **File Name:** {uploaded_file.name}")
        with col2:
            file_size = len(uploaded_file.getvalue()) / 1024
            st.info(f"📊 **File Size:** {file_size:.2f} KB")
        
        # Parse button
        if st.button("🔍 Parse Statement", type="primary", use_container_width=True):
            with st.spinner("Parsing your statement... Please wait."):
                try:
                    # Save uploaded file temporarily
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_path = tmp_file.name
                    
                    # Parse the statement
                    result = parse_statement(tmp_path)
                    
                    # Clean up temp file
                    os.unlink(tmp_path)
                    
                    # Display results
                    st.success("✅ Statement parsed successfully!")
                    st.markdown("---")
                    
                    # Display 5 key data points
                    st.subheader("📊 Extracted Data Points")
                    
                    # Create metrics in columns
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric(
                            label="🏦 Card Issuer",
                            value=result.get('issuer', 'Not Found')
                        )
                    
                    with col2:
                        card_last_four = result.get('card_last_four', 'Not Found')
                        st.metric(
                            label="💳 Card Last 4 Digits",
                            value=f"****{card_last_four}" if card_last_four != 'Not Found' else 'Not Found'
                        )
                    
                    with col3:
                        total_due = result.get('total_amount_due', 'Not Found')
                        st.metric(
                            label="💰 Total Amount Due",
                            value=f"₹{total_due}" if total_due != 'Not Found' else 'Not Found'
                        )
                    
                    # Second row of metrics
                    col4, col5 = st.columns(2)
                    
                    with col4:
                        billing_cycle = result.get('billing_cycle')
                        if billing_cycle:
                            cycle_text = f"{billing_cycle.get('start_date', 'N/A')} to {billing_cycle.get('end_date', 'N/A')}"
                        else:
                            cycle_text = "Not Found"
                        st.metric(
                            label="📅 Billing Cycle",
                            value=cycle_text
                        )
                    
                    with col5:
                        due_date = result.get('payment_due_date', 'Not Found')
                        st.metric(
                            label="⏰ Payment Due Date",
                            value=due_date
                        )
                    
                    st.markdown("---")
                    
                    # Display detailed information in expandable sections
                    with st.expander("📋 Detailed Information", expanded=True):
                        # Create a summary table
                        summary_data = {
                            "Data Point": [
                                "Card Issuer",
                                "Card Last 4 Digits",
                                "Billing Cycle",
                                "Payment Due Date",
                                "Total Amount Due"
                            ],
                            "Value": [
                                result.get('issuer', 'Not Found'),
                                f"****{card_last_four}" if card_last_four != 'Not Found' else 'Not Found',
                                cycle_text,
                                due_date,
                                f"₹{total_due}" if total_due != 'Not Found' else 'Not Found'
                            ]
                        }
                        df_summary = pd.DataFrame(summary_data)
                        st.table(df_summary)
                    
                    # Display transactions if available
                    transactions = result.get('transactions', [])
                    if transactions:
                        with st.expander("💸 Sample Transactions (Top 10)", expanded=False):
                            st.markdown("Below are sample transactions extracted from the statement:")
                            df_transactions = pd.DataFrame(transactions)
                            st.dataframe(
                                df_transactions,
                                use_container_width=True,
                                hide_index=True
                            )
                    
                    # Download results as JSON
                    st.markdown("---")
                    st.subheader("💾 Export Results")
                    
                    import json
                    json_str = json.dumps(result, indent=2)
                    st.download_button(
                        label="📥 Download as JSON",
                        data=json_str,
                        file_name=f"parsed_statement_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json",
                        use_container_width=True
                    )
                    
                except Exception as e:
                    st.error(f"❌ Error parsing statement: {str(e)}")
                    st.markdown("""
                    **Possible reasons:**
                    - PDF format is not supported
                    - Statement is from an unsupported issuer
                    - PDF is encrypted or password protected
                    - PDF text extraction failed
                    """)
    
    else:
        # Display instructions when no file is uploaded
        st.info("👆 Please upload a credit card statement PDF to begin parsing.")
        
        st.markdown("---")
        st.subheader("🎯 How to Use")
        st.markdown("""
        1. **Upload** your credit card statement PDF using the file uploader above
        2. **Click** the "Parse Statement" button to extract data
        3. **Review** the extracted information in the results section
        4. **Download** the results as JSON for further processing
        
        The parser uses advanced pattern matching and text extraction to identify:
        - Card issuer and card details
        - Billing periods and payment deadlines
        - Outstanding balances and transaction history
        """)
        
        st.markdown("---")
        st.subheader("⚠️ Important Notes")
        st.markdown("""
        - Ensure the PDF is **not password protected**
        - The statement should be from one of the **supported issuers**
        - Parsing accuracy depends on **PDF text quality**
        - This tool is for **demonstration purposes** only
        """)


if __name__ == "__main__":
    main()
