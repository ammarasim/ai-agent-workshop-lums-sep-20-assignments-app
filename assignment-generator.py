import streamlit as st
import re
import random
from typing import List, Dict, Tuple

class QuizGenerator:
    def __init__(self):
        self.question_starters = [
            "What is", "How does", "Why is", "When did", "Where does",
            "Which", "Who was", "What are the main", "How can", "What would happen if"
        ]
        
        self.essay_prompts = [
            "Analyze the main concepts discussed in the text and explain their significance.",
            "Compare and contrast the key ideas presented and provide your own perspective.",
            "Discuss the implications of the information provided and its real-world applications.",
            "Evaluate the arguments presented and provide supporting evidence for your viewpoint.",
            "Examine the relationship between the different concepts mentioned in the text.",
            "Critically assess the topic and propose potential solutions or improvements.",
            "Explore the historical context and evolution of the subject matter.",
            "Investigate the causes and effects of the phenomena described in the text."
        ]

    def extract_key_phrases(self, text: str) -> Tuple[List[str], List[str]]:
        """Extract key phrases and concepts from the text."""
        # Clean the text
        text = re.sub(r'[^\w\s]', '', text.lower())
        
        # Split into sentences
        sentences = [s.strip() for s in text.split('.') if len(s.strip()) > 10]
        
        # Extract words
        words = text.split()
        
        # Filter out common words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 
            'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those'
        }
        
        # Get important words
        key_words = [word for word in words if len(word) > 4 and word not in stop_words]
        
        # Get unique words and limit to most relevant ones
        unique_words = list(set(key_words))[:10]
        
        return sentences, unique_words

    def generate_assignment_questions(self, text: str, key_words: List[str]) -> List[str]:
        """Generate essay-style assignment questions."""
        assignments = []
        
        # Select random essay prompts
        selected_prompts = random.sample(self.essay_prompts, min(2, len(self.essay_prompts)))
        
        for i, prompt in enumerate(selected_prompts):
            if key_words:
                # Customize prompt with key concepts
                key_concept = random.choice(key_words).title()
                customized_prompt = f"{prompt} Focus particularly on the concept of '{key_concept}' mentioned in the material."
            else:
                customized_prompt = prompt
                
            assignments.append(f"Assignment {i+1}: {customized_prompt}")
        
        return assignments

    def generate_quiz_questions(self, sentences: List[str], key_words: List[str]) -> List[Dict]:
        """Generate multiple choice quiz questions."""
        quiz_questions = []
        
        if not sentences or not key_words:
            # Fallback questions if no content to work with
            return [
                {
                    "question": "Based on the provided text, what is the main topic discussed?",
                    "options": ["Option A", "Option B", "Option C", "Option D"],
                    "correct": 0,
                    "explanation": "This is a general comprehension question."
                }
            ]
        
        # Generate 3 questions
        for i in range(3):
            if i < len(sentences) and key_words:
                sentence = sentences[i]
                key_word = random.choice(key_words)
                
                # Create question based on sentence and key word
                question_starter = random.choice(self.question_starters)
                question = f"{question_starter} {key_word.title()} mentioned in the text?"
                
                # Generate options
                correct_option = f"{key_word.title()} is related to {sentence[:50]}..."
                
                distractors = [
                    "It refers to a completely different concept",
                    "It is not mentioned in the provided text",
                    "It only appears in the conclusion"
                ]
                
                options = [correct_option] + distractors
                random.shuffle(options)
                correct_index = options.index(correct_option)
                
                quiz_questions.append({
                    "question": question,
                    "options": options,
                    "correct": correct_index,
                    "explanation": "The correct answer relates to the context provided in the text."
                })
            else:
                # Fallback question
                quiz_questions.append({
                    "question": f"Question {i+1}: What can be inferred from the given text?",
                    "options": [
                        "The text provides comprehensive information",
                        "The text is completely unrelated to the topic",
                        "The text contains no useful information",
                        "The text is written in a foreign language"
                    ],
                    "correct": 0,
                    "explanation": "This question tests reading comprehension."
                })
        
        return quiz_questions

    def generate_content(self, input_text: str) -> Tuple[List[str], List[Dict]]:
        """Generate both assignments and quiz questions from input text."""
        if not input_text.strip():
            return [], []
        
        sentences, key_words = self.extract_key_phrases(input_text)
        assignments = self.generate_assignment_questions(input_text, key_words)
        quiz_questions = self.generate_quiz_questions(sentences, key_words)
        
        return assignments, quiz_questions

def main():
    st.set_page_config(
        page_title="Assignment & Quiz Generator",
        page_icon="📚",
        layout="wide"
    )
    
    st.title("📚 Assignment & Quiz Generator")
    st.markdown("Generate assignments and quiz questions from any text or topic!")
    
    # Initialize the generator
    generator = QuizGenerator()
    
    # Sidebar for instructions
    with st.sidebar:
        st.header("Instructions")
        st.markdown("""
        1. **Input Text**: Paste your document or write about a topic
        2. **Generate**: Click the button to create content
        3. **Review**: Check your assignments and quiz questions
        
        **Tips:**
        - Longer texts produce better questions
        - Include key concepts and definitions
        - Technical topics work well
        """)
    
    # Main input area
    st.header("Input Text or Topic")
    input_text = st.text_area(
        "Enter your document content or topic description:",
        height=200,
        placeholder="Paste your document here or describe a topic you want to create assignments about..."
    )
    
    # Sample text button
    if st.button("Use Sample Text"):
        sample_text = """
        Photosynthesis is the process by which plants convert sunlight, carbon dioxide, and water into glucose and oxygen. 
        This process occurs in the chloroplasts of plant cells and involves two main stages: the light reactions and the Calvin cycle. 
        During light reactions, chlorophyll absorbs sunlight and converts it into chemical energy in the form of ATP and NADPH. 
        The Calvin cycle uses this energy to convert carbon dioxide into glucose. Photosynthesis is essential for life on Earth 
        as it produces oxygen and serves as the foundation of most food chains. Factors affecting photosynthesis include light intensity, 
        carbon dioxide concentration, and temperature. Understanding photosynthesis is crucial for agriculture and environmental science.
        """
        st.text_area("Sample text loaded:", value=sample_text, height=150, disabled=True)
        input_text = sample_text
    
    # Generate button
    if st.button("🎯 Generate Assignments & Quiz", type="primary"):
        if input_text.strip():
            with st.spinner("Generating content..."):
                assignments, quiz_questions = generator.generate_content(input_text)
            
            # Display results
            col1, col2 = st.columns(2)
            
            with col1:
                st.header("📝 Assignment Questions")
                if assignments:
                    for i, assignment in enumerate(assignments):
                        st.subheader(f"Assignment {i+1}")
                        st.write(assignment.replace(f"Assignment {i+1}: ", ""))
                        st.markdown("---")
                else:
                    st.warning("No assignments generated. Try providing more detailed text.")
            
            with col2:
                st.header("❓ Quiz Questions")
                if quiz_questions:
                    for i, q in enumerate(quiz_questions):
                        st.subheader(f"Question {i+1}")
                        st.write(q["question"])
                        
                        # Display options
                        for j, option in enumerate(q["options"]):
                            if j == q["correct"]:
                                st.success(f"{chr(65+j)}. {option} ✓")
                            else:
                                st.write(f"{chr(65+j)}. {option}")
                        
                        st.info(f"**Explanation:** {q['explanation']}")
                        st.markdown("---")
                else:
                    st.warning("No quiz questions generated. Try providing more detailed text.")
        else:
            st.error("Please enter some text to generate assignments and quiz questions.")
    
    # Footer
    st.markdown("---")
    st.markdown("*Generated content is based on simple text analysis. Review and modify as needed for your specific requirements.*")

if __name__ == "__main__":
    main()
