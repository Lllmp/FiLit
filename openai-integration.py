import os
import streamlit as st
import openai
from dotenv import load_dotenv

# Load environment variables for API keys
load_dotenv()

def configure_openai():
    """Configure OpenAI API and check if it's available"""
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        openai.api_key = api_key
        return True
    else:
        # For development/testing, you can set the key manually
        # If no key is available, return False to use fallback options
        return False

def generate_business_names(business_name, student_name, silliness_level=3):
    """
    Generate creative business names using OpenAI
    
    Args:
        business_name: Type of business (e.g., "Pet Walking Service")
        student_name: The student's first name
        silliness_level: How silly/creative names should be (1-5)
    
    Returns:
        List of business name suggestions
    """
    try:
        # Create the prompt for business name generation
        prompt = f"""Generate 5 fun business names for a 1st grade student named {student_name} who wants to start a {business_name} business.

Silliness level: {silliness_level}/5 (where 1 is normal, 5 is super silly)

Follow these patterns:
- Some names should include "{student_name}'s" at the beginning
- Make the names catchy and memorable
- Keep names simple enough for a 1st grader to understand
- The higher the silliness level, the more creative and fun the names should be

Format as a simple list with just the business names (no numbering, no explanations)."""

        # Call the OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.7
        )
        
        # Process the response
        name_suggestions = response.choices[0].message.content.strip().split('\n')
        # Clean up the suggestions
        name_suggestions = [name.strip().strip('*-•').strip() for name in name_suggestions if name.strip()]
        
        return name_suggestions[:5]  # Return up to 5 suggestions
        
    except Exception as e:
        # Return fallback names if API call fails
        return [
            f"{student_name}'s {business_name}",
            f"{student_name}'s Amazing {business_name}",
            f"{student_name}'s Super {business_name} Service",
            f"The {business_name} Expert",
            f"Fantastic {business_name} Friends"
        ]

def generate_advertisement_content(business_name, business_type, student_name):
    """
    Generate advertisement content using OpenAI
    
    Args:
        business_name: The selected business name
        business_type: Type of business (e.g., "Pet Walking Service")
        student_name: The student's first name
    
    Returns:
        Dictionary with tagline and description
    """
    try:
        # Create the prompt for advertisement content
        prompt = f"""Create a short advertisement for a 1st grade student named {student_name} who is starting a business called "{business_name}" that provides {business_type} services.

Please generate:
1. A catchy tagline (5-7 words)
2. A short description (1-2 sentences) about what the business offers
3. A simple "call to action" to contact them

Make everything simple enough for a 1st grader to read and understand. 
Keep the language cheerful and kid-friendly.

Format as a JSON object with keys: "tagline", "description", "call_to_action"."""

        # Call the OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.7
        )
        
        # Process the response - try to parse as JSON, but have fallbacks if it's not in the expected format
        response_text = response.choices[0].message.content.strip()
        
        # Simple parsing attempt - this is not full JSON parsing, but extracts key elements
        ad_content = {}
        
        if '"tagline"' in response_text:
            tagline_start = response_text.find('"tagline"') + 10
            tagline_end = response_text.find('"', tagline_start + 1)
            ad_content["tagline"] = response_text[tagline_start:tagline_end].strip('": ,')
        else:
            ad_content["tagline"] = f"Quality {business_type} from {student_name}!"
            
        if '"description"' in response_text:
            desc_start = response_text.find('"description"') + 14
            desc_end = response_text.find('"', desc_start + 1)
            ad_content["description"] = response_text[desc_start:desc_end].strip('": ,')
        else:
            ad_content["description"] = f"I provide {business_type} services with a smile!"
            
        if '"call_to_action"' in response_text:
            cta_start = response_text.find('"call_to_action"') + 16
            cta_end = response_text.find('"', cta_start + 1)
            ad_content["call_to_action"] = response_text[cta_start:cta_end].strip('": ,')
        else:
            ad_content["call_to_action"] = f"Ask for {student_name}!"
        
        return ad_content
        
    except Exception as e:
        # Return fallback content if API call fails
        return {
            "tagline": f"Quality {business_type} from {student_name}!",
            "description": f"I provide {business_type} services with a smile!",
            "call_to_action": f"Ask for {student_name}!"
        }

# Example usage:
# has_openai = configure_openai()
# if has_openai:
#     business_names = generate_business_names("Dog Walking Service", "Emily", 4)
#     ad_content = generate_advertisement_content("Emily's Pawsome Pals", "dog walking", "Emily")