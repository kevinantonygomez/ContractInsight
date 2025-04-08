import argparse  
import threading 
import os        
from utils import read_pdf, loading_animation, generate_html # Custom utility functions
from openai_utils import summarize_and_highlight, extract_data, assess_risk, assess_deal, check_args_validity # OpenAI API related functions

def main(filepath, output_filename, model, temperature):
    """Main function to analyze the contract."""
    pdf_text = read_pdf(filepath) # Reads the PDF content
    if pdf_text.get('error'): # Checks if there was an error reading the PDF
        return pdf_text

    analysis_events = [('Summarizing and highlighting', summarize_and_highlight), # List of analysis tasks
                       ('Extracting data', extract_data),
                       ('Assessing risk', assess_risk),
                       ('Assessing deal', assess_deal)]
    responses = {} # Dictionary to store analysis responses

    for event_name, event_func in analysis_events:
        try:
            stop_event = threading.Event() # Event to signal loading animation to stop
            loading_thread = threading.Thread(target=loading_animation, args=(event_name, stop_event,)) # Create loading animation thread
            loading_thread.start() # Start loading animation
            responses[event_name] = event_func(pdf_text['text'], model, temperature) # Execute analysis function and store response
        finally:
            stop_event.set()  # Signal the loading animation thread to stop
            loading_thread.join()  # Wait for the loading animation thread to finish.

    results_html_path = f"{output_filename}.html" # Create HTML output filename
    generate_html(results_html_path, responses) # Generate HTML report
    print(f"Results saved to: {results_html_path}") # Print output file path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze a contract PDF.") # Create argument parser
    parser.add_argument("filepath", type=str, help="Path to the contract PDF file.") # required 'filepath' argument
    parser.add_argument("--output", type=str, default=None, help="Output filename (without extension). Defaults to input filename.") # optional 'output' argument
    parser.add_argument("--model", type=str, default="gpt-4o", help="OpenAI model to use. Defaults to gpt-4o") # optional 'model' argument
    parser.add_argument("--temperature", type=float, default=0.5,  help="Output randomness (between 0 and 2). Higher values make the output more random. Defaults to 0.5") # optional 'temperature' argument

    args = parser.parse_args() # Parse command-line arguments

    if not check_args_validity(args.model, args.temperature): # Check if the args are valid
        exit(1) # Exit if the model is invalid.

    output_filename = args.output if args.output else os.path.splitext(os.path.basename(args.filepath))[0] # Determine output filename
    main(args.filepath, output_filename, args.model, args.temperature) # Execute main function with provided arguments