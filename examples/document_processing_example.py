"""
Document Processing Example
===========================
Demonstrates advanced document processing for contracts and leases.
"""

from document_processing import AdvancedDocumentProcessor
import tempfile
import os

def example_contract_processing():
    """Example of processing contract documents"""
    
    processor = AdvancedDocumentProcessor()
    
    # Example: Process a contract document
    print("📄 Document Processing Example")
    print("=" * 50)
    
    # Create a sample contract text file for demo
    sample_contract = """
    LEASE AGREEMENT
    
    This Lease Agreement ("Agreement") is entered into on January 1, 2024,
    between ABC Properties LLC ("Lessor") and XYZ Corporation ("Lessee").
    
    PROPERTY: 123 Main Street, Atlanta, GA 30309
    
    TERM: The lease term shall commence on January 1, 2024 and expire on
    December 31, 2026, for a total term of 36 months.
    
    RENT: Lessee agrees to pay monthly rent of $5,000.00, due on the first
    of each month. Security deposit of $10,000.00 is required.
    
    RENEWAL: Lessee may renew this lease for an additional 24 months upon
    written notice 90 days prior to expiration.
    
    MAINTENANCE: Lessor is responsible for structural repairs. Lessee is
    responsible for routine maintenance and utilities.
    """
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(sample_contract)
        temp_path = f.name
    
    try:
        # Process the contract
        result = processor.process_contract_document(
            temp_path,
            extract_tables=False,  # No tables in text file
            use_ocr=False
        )
        
        print("\n✅ Processing Results:")
        print(f"Text length: {len(result['text'])} characters")
        print(f"Word count: {result['metadata']['word_count']}")
        print(f"Tables found: {result['metadata']['table_count']}")
        
        print("\n📋 Structured Data Extraction:")
        structured = result['structured_data']
        print(f"Document type: {structured['document_type']}")
        print(f"Extraction schema: {list(structured['extraction_schema'].keys())}")
        
        # Example: Extract lease-specific terms
        print("\n🏢 Lease Terms Extraction:")
        lease_result = processor.extract_lease_terms(temp_path)
        print(f"Lease terms extracted: {len(lease_result['lease_terms']['fields'])} fields")
        
    finally:
        # Cleanup
        if os.path.exists(temp_path):
            os.unlink(temp_path)


def example_table_extraction():
    """Example of extracting tables from PDF"""
    
    processor = AdvancedDocumentProcessor()
    
    print("\n📊 Table Extraction Example")
    print("=" * 50)
    print("To extract tables from PDF:")
    print("""
    tables = processor.extract_tables_from_pdf("lease.pdf")
    
    for table in tables:
        print(f"Table on page {table['page']}:")
        print(table['dataframe'])
    """)


if __name__ == "__main__":
    example_contract_processing()
    example_table_extraction()

