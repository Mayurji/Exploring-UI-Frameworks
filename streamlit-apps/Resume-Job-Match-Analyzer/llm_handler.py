import ollama

class LLMHandler:
    def __init__(self, model_name='llama3.2'):
        self.model_name = model_name

    def extract_skills_and_experience(self, text):
        """
        Extract skills and years of experience from the given text using Ollama.
        """
        prompt = f"""
        Extract only the professional skills and the total number of years of experience from the following text.
        Format the output as a concise summary that can be used for semantic matching.
        
        Text:
        {text}
        
        Output format:
        Skills: [List of skills]
        Experience: [Number of years] years
        """
        
        try:
            response = ollama.chat(model=self.model_name, messages=[
                {
                    'role': 'user',
                    'content': prompt,
                },
            ])
            return response['message']['content'].strip()
        except Exception as e:
            return f"Error extracting info: {str(e)}"

    def extract_experience(self, text):
        """
        Extract only the years of experience from the given text using Ollama.
        """
        prompt = f"""
        Extract only the number of years of experience required from the following job description.
        If not explicitly mentioned, estimate based on the role and responsibilities.
        Return only the number or a short range (e.g., "3-5 years").
        
        Job Description:
        {text}
        
        Output:
        """
        
        try:
            response = ollama.chat(model=self.model_name, messages=[
                {
                    'role': 'user',
                    'content': prompt,
                },
            ])
            return response['message']['content'].strip()
        except Exception as e:
            return "N/A"
