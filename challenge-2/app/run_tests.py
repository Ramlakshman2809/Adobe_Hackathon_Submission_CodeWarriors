import os
import json
from document_processor import DocumentProcessor  # Changed from prg to document_processor

TEST_CASES = [
    {
        "name": "Academic Research",
        "input_subdir": "academic_research",
        "persona": "PhD Researcher in Computational Biology",
        "job": "Prepare a comprehensive literature review focusing on methodologies, datasets, and performance benchmarks"
    }
    # Uncomment other test cases when ready
    # {
    #     "name": "Business Analysis",
    #     "input_subdir": "business_analysis",
    #     "persona": "Investment Analyst",
    #     "job": "Analyze revenue trends, R&D investments, and market positioning strategies"
    # },
    # {
    #     "name": "Educational Content",
    #     "input_subdir": "educational_content",
    #     "persona": "Undergraduate Chemistry Student",
    #     "job": "Identify key concepts and mechanisms for exam preparation on reaction kinetics"
    # }
]

def run_test_case(test_case, base_input_dir="input"):
    print(f"\n{'='*50}")
    print(f"Running Test Case: {test_case['name']}")
    print(f"Persona: {test_case['persona']}")
    print(f"Job: {test_case['job']}")
    
    # Set input directory path - using relative path
    input_dir = os.path.join(base_input_dir, test_case["input_subdir"])
    
    if not os.path.exists(input_dir):
        print(f"Warning: Input directory {input_dir} not found. Skipping test case.")
        print(f"Current working directory: {os.getcwd()}")
        print(f"Please ensure you have an '{input_dir}' directory with PDF files.")
        return
    
    # Count PDF files in input directory
    pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.pdf')]
    print(f"Found {len(pdf_files)} PDF files in {input_dir}")
    
    if not pdf_files:
        print("No PDF files found in the directory. Skipping test case.")
        return
    
    # Process documents
    processor = DocumentProcessor(input_dir=input_dir)
    result = processor.process_documents(
        persona=test_case["persona"],
        job=test_case["job"]
    )
    
    # Save results
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"result_{test_case['name'].lower().replace(' ', '_')}.json")
    
    with open(output_file, "w") as f:
        json.dump(result, f, indent=2)
    
    print(f"\nResults saved to {output_file}")
    print(f"{'='*50}\n")

def main():
    print("Starting test cases...")
    
    for test_case in TEST_CASES:
        try:
            run_test_case(test_case)
        except Exception as e:
            print(f"Error running test case {test_case['name']}: {str(e)}")
    
    print("All test cases completed!")

if __name__ == "__main__":
    main()