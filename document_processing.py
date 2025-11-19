"""
Advanced Document Processing
============================
Enhanced document processing for contracts, leases, and structured documents.
Demonstrates document processing using LLMs.
"""

import os
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path
import pandas as pd
import json
from datetime import datetime

# Document processing libraries
try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False

try:
    import pytesseract
    from PIL import Image
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False

try:
    from unstructured.partition.auto import partition
    UNSTRUCTURED_AVAILABLE = True
except ImportError:
    UNSTRUCTURED_AVAILABLE = False

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AdvancedDocumentProcessor:
    """
    Advanced Document Processing for Contracts and Structured Documents
    
    Features:
    - OCR for scanned documents
    - Table extraction
    - Structured data extraction
    - Contract/lease parsing
    """
    
    def __init__(self):
        logger.info("Advanced Document Processor initialized")
    
    def extract_tables_from_pdf(self, pdf_path: str) -> List[Dict[str, Any]]:
        """Extract tables from PDF using pdfplumber"""
        if not PDFPLUMBER_AVAILABLE:
            logger.warning("pdfplumber not available, install with: pip install pdfplumber")
            return []
        
        tables = []
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    page_tables = page.extract_tables()
                    for table_num, table in enumerate(page_tables):
                        # Convert to DataFrame
                        if table:
                            df = pd.DataFrame(table[1:], columns=table[0])
                            tables.append({
                                'page': page_num + 1,
                                'table_number': table_num + 1,
                                'data': df.to_dict('records'),
                                'dataframe': df
                            })
            
            logger.info(f"Extracted {len(tables)} tables from {pdf_path}")
            return tables
            
        except Exception as e:
            logger.error(f"Error extracting tables: {e}")
            return []
    
    def extract_text_with_ocr(self, image_path: str) -> Dict[str, Any]:
        """Extract text from scanned document using OCR"""
        if not OCR_AVAILABLE:
            logger.warning("OCR not available, install with: pip install pytesseract pillow")
            return {"text": "", "error": "OCR not available"}
        
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image)
            
            # Get detailed OCR data
            ocr_data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
            
            return {
                "text": text,
                "confidence_scores": [int(conf) for conf in ocr_data.get('conf', []) if conf != '-1'],
                "word_count": len(text.split()),
                "char_count": len(text)
            }
            
        except Exception as e:
            logger.error(f"Error in OCR: {e}")
            return {"text": "", "error": str(e)}
    
    def extract_structured_data(
        self,
        document_path: str,
        document_type: str = "contract",
        extraction_schema: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Extract structured data from documents using LLM
        
        Common fields for contracts/leases:
        - parties, dates, amounts, terms, conditions
        """
        try:
            # Load document
            if document_path.endswith('.pdf'):
                loader = PyPDFLoader(document_path)
            else:
                loader = TextLoader(document_path)
            
            docs = loader.load()
            full_text = "\n\n".join([doc.page_content for doc in docs])
            
            # Default extraction schema for contracts
            if not extraction_schema:
                extraction_schema = {
                    "parties": "List all parties involved in the contract",
                    "effective_date": "Contract effective/start date",
                    "expiration_date": "Contract expiration/end date",
                    "total_value": "Total contract value or amount",
                    "payment_terms": "Payment terms and schedule",
                    "key_terms": "Key terms and conditions",
                    "termination_clause": "Termination conditions"
                }
            
            # Create extraction prompt
            extraction_prompt = f"""
            Extract structured information from the following {document_type} document.
            
            Extract the following fields:
            {json.dumps(extraction_schema, indent=2)}
            
            Document text:
            {full_text[:5000]}  # Limit to avoid token limits
            
            Return the extracted information as JSON.
            """
            
            # In production, this would use an LLM to extract structured data
            # For now, return a template structure
            extracted_data = {
                "document_type": document_type,
                "extraction_timestamp": datetime.utcnow().isoformat(),
                "fields": {key: None for key in extraction_schema.keys()},
                "raw_text_length": len(full_text),
                "extraction_schema": extraction_schema
            }
            
            logger.info(f"Structured data extraction completed for {document_type}")
            return extracted_data
            
        except Exception as e:
            logger.error(f"Error extracting structured data: {e}")
            return {"error": str(e)}
    
    def process_contract_document(
        self,
        document_path: str,
        extract_tables: bool = True,
        use_ocr: bool = False
    ) -> Dict[str, Any]:
        """
        Comprehensive contract document processing
        
        Returns:
            Dictionary with text, tables, structured data, metadata
        """
        result = {
            "document_path": document_path,
            "processing_timestamp": datetime.utcnow().isoformat(),
            "text": "",
            "tables": [],
            "structured_data": {},
            "metadata": {}
        }
        
        try:
            # Extract text
            if use_ocr and document_path.endswith(('.png', '.jpg', '.jpeg', '.tiff')):
                ocr_result = self.extract_text_with_ocr(document_path)
                result["text"] = ocr_result.get("text", "")
                result["metadata"]["ocr_used"] = True
                result["metadata"]["ocr_confidence"] = (
                    sum(ocr_result.get("confidence_scores", [])) / 
                    len(ocr_result.get("confidence_scores", [])) 
                    if ocr_result.get("confidence_scores") else 0
                )
            else:
                loader = PyPDFLoader(document_path) if document_path.endswith('.pdf') else TextLoader(document_path)
                docs = loader.load()
                result["text"] = "\n\n".join([doc.page_content for doc in docs])
                result["metadata"]["ocr_used"] = False
            
            # Extract tables
            if extract_tables and document_path.endswith('.pdf'):
                result["tables"] = self.extract_tables_from_pdf(document_path)
            
            # Extract structured data
            result["structured_data"] = self.extract_structured_data(
                document_path,
                document_type="contract"
            )
            
            # Add metadata
            result["metadata"]["file_size"] = os.path.getsize(document_path)
            result["metadata"]["file_type"] = Path(document_path).suffix
            result["metadata"]["word_count"] = len(result["text"].split())
            result["metadata"]["table_count"] = len(result["tables"])
            
            logger.info(f"Contract processing completed: {len(result['text'])} chars, {len(result['tables'])} tables")
            return result
            
        except Exception as e:
            logger.error(f"Error processing contract: {e}")
            result["error"] = str(e)
            return result
    
    def extract_lease_terms(self, lease_document_path: str) -> Dict[str, Any]:
        """Extract lease-specific terms"""
        contract_data = self.process_contract_document(lease_document_path)
        
        # Lease-specific extraction schema
        lease_schema = {
            "lessor": "Property owner/landlord",
            "lessee": "Tenant/renter",
            "property_address": "Leased property address",
            "lease_start_date": "Lease start date",
            "lease_end_date": "Lease end date",
            "monthly_rent": "Monthly rent amount",
            "security_deposit": "Security deposit amount",
            "renewal_options": "Renewal and extension options",
            "maintenance_responsibilities": "Who is responsible for maintenance"
        }
        
        lease_data = self.extract_structured_data(
            lease_document_path,
            document_type="lease",
            extraction_schema=lease_schema
        )
        
        return {
            "lease_terms": lease_data,
            "full_document": contract_data
        }

