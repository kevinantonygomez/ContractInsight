# ContractInsight
A Python tool to analyze contract PDFs using OpenAI, generating an HTML report with summaries, data extraction, and risk/deal assessments.

## Features
-   **PDF Analysis:** Reads and extracts text from PDF contracts.
-   **OpenAI Integration:** Uses the OpenAI API to summarize, extract data, assess risk, and evaluate the deal.
-   **HTML Report Generation:** Creates an HTML report with formatted analysis results.
-   **Command-Line Interface:** Easy-to-use command-line interface for specifying input PDF, output filename, OpenAI model, and temperature.
-   **Loading Animation:** Provides a loading animation during analysis.
-   **Model and Temperature Validation:** Validates provided OpenAI model and temperature.
-   **Adaptability** Can easily be plugged in to various applications, including Flask backends, with minimal modifications.

## Prerequisites
-   Python 3.6+
-   OpenAI API key (set as an environment variable `OPENAI_API_KEY`)

## Installation

1.  Clone the repository:

    ```bash
    git clone [[https://github.com/kevinantonygomez/ContractInsight.git](https://github.com/kevinantonygomez/ContractInsight.git)]
    cd ContractInsight
    ```

2.  Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

3.  Set your OpenAI API key as an environment variable:

    ```bash
    export OPENAI_API_KEY="your_openai_api_key" # linux or mac
    # set OPENAI_API_KEY="your_openai_api_key" # windows
    ```

## Usage

```bash
python main.py <filepath> [--output <output_filename>] [--model <model>] [--temperature <temperature>]
```

## Example
A sample input (a lease agreement) and the rendered output can be viewed under "example"
