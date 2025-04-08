import re
from pypdf import PdfReader
import time
import sys

def loading_animation(event_name, stop_event):
    """Displays a loading animation."""
    chars = ["\\", "|", "/", "-"]
    i = 0
    while not stop_event.is_set():
        sys.stdout.write(f"\r{event_name} {chars[i % len(chars)]}")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.flush()
    sys.stdout.write(f"\r{event_name} ✅\n")
    sys.stdout.flush()


def read_pdf(filepath):
    """Reads text from a PDF file."""
    text = ""
    try:
        reader = PdfReader(filepath)
        number_of_pages = len(reader.pages)
        for page_num in range(number_of_pages):
            text += reader.pages[page_num].extract_text()
    except FileNotFoundError:
        print(f"Pdf not found")
        return {"error": "Pdf not found"}
    except Exception as e:
        print(f"An error occurred while reading pdf: {e}")
        return {"error": e}
    return {'text': text}


def replace_with_markdown(text):
    """
    Replaces markdown strings with (str).

    Args:
        text (str): The input text.

    Returns:
        str: The modified text.
    """
    def replace_bold(match):
        return f"<strong>{match.group(1)}</strong>"

    def replace_h3(match):
        return f"<h3>{match.group(1)}</h3>"

    def replace_h2(match):
        return f"<h2>{match.group(1)}</h2>"
    
    def replace_h1(match):
        return f"<h1>{match.group(1)}</h1>"

    text = re.sub(r'\*\*(.*?)\*\*', replace_bold, text)
    text = re.sub(r'### (.*?)(?:\n|$)', replace_h3, text)
    text = re.sub(r'## (.*?)(?:\n|$)', replace_h2, text)
    text = re.sub(r'# (.*?)(?:\n|$)', replace_h1, text)
    text = text.replace("\n", "<br>")
    return text

def generate_html(results_html_path, responses):
    """Generates an HTML file with the analysis results, preserving formatting."""
    if "error" in responses:
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head><title>Error</title></head>
        <body><h1>Error</h1><p>{responses["error"]}</p></body>
        </html>
        """
    else:
        summarize_response = replace_with_markdown(responses['Summarizing and highlighting'].output[0].content[0].text)
        extract_response = replace_with_markdown(responses['Extracting data'].output[0].content[0].text)
        risk_response = replace_with_markdown(responses['Assessing risk'].output[0].content[0].text)
        deal_response = replace_with_markdown(responses['Assessing deal'].output[0].content[0].text)

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Contract Analysis Results</title>
            <style>
                body {{
                    font-family: monospace;
                    white-space: pre-wrap;
                    margin: 20px;
                }}
                .section {{
                    border: 1px solid #ddd;
                    padding: 15px;
                    margin-bottom: 20px;
                    border-radius: 5px;
                }}
                .section h2 {{
                    margin-top: 0;
                }}
                strong {{
                    font-weight: bold;
                }}
            </style>
        </head>
        <body>
            <h1>Contract Analysis Results</h1>
            <div class="section">
                <h2>Summarization and Highlights</h2>
                <p>{summarize_response}</p>
            </div>

            """
        if extract_response and extract_response != "no_data":
            html_content += f"""
            <div class="section">
                <h2>Extracted Data</h2>
                <p>{extract_response}</p>
            </div>
            """

        html_content += f"""
            <div class="section">
                <h2>Risk Assessment</h2>
                <p>{risk_response}</p>
            </div>

            <div class="section">
                <h2>Deal Assessment</h2>
                <p>{deal_response}</p>
            </div>

        </body>
        </html>
        """

    with open(results_html_path, "w") as f:
        f.write(html_content)

