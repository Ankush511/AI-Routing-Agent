import os
from dotenv import find_dotenv, load_dotenv
import google.generativeai as genai

load_dotenv(find_dotenv())

API_KEY = os.environ['GEMINI_API_KEY']
genai.configure(api_key=API_KEY)

def funify(text: str) -> str:
    """
    Makes the given text funnier using Google's Gemini model.

    Args:
        text (str): The text content to make funnier.

    Returns:
        str: The funified text.

    Raises:
        Exception: If there's an error in generating the funified text.
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""Make the following text funnier while keeping its core meaning. 
        Be creative but don't make it too silly. Keep it concise.
        
        Text to funify: {text}
        
        Respond with ONLY the funified text, no explanations or additional commentary."""
        
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 150,
            }
        )
        
        funified_text = response.text.strip()
        
        # Remove quotes if they're present in the response
        if funified_text.startswith('"') and funified_text.endswith('"'):
            funified_text = funified_text[1:-1]
        
        return funified_text
    
    except Exception as e:
        raise Exception(f"Error in funifying text: {str(e)}")