import os
from dotenv import find_dotenv, load_dotenv
import google.generativeai as genai

load_dotenv(find_dotenv())

API_KEY = os.environ['GEMINI_API_KEY']
genai.configure(api_key=API_KEY)

def summarize(text: str) -> str:
    """
    Summarizes the given text using Google's Gemini model.

    Args:
        text (str): The text content to summarize.

    Returns:
        str: The summarized text.

    Raises:
        Exception: If there's an error in generating the summary.
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""Provide a concise summary of the following text. 
        Capture the key points while significantly reducing the length.
        
        Text to summarize: {text}
        
        Respond with ONLY the summary, no explanations or additional commentary."""
        
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.1,
                "max_output_tokens": 150,
            }
        )
        
        summary = response.text.strip()
        
        # Remove quotes if they're present in the response
        if summary.startswith('"') and summary.endswith('"'):
            summary = summary[1:-1]
        
        return summary
    
    except Exception as e:
        raise Exception(f"Error in summarizing text: {str(e)}")
