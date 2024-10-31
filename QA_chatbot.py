from transformers import pipeline

# Load the question-answering pipeline from Hugging Face
qa_pipeline = pipeline("question-answering")

def ask_question(question, context):
    # Check for empty question or context
    if not question:
        raise ValueError("The 'question' parameter cannot be empty.")
    if not context:
        raise ValueError("The 'context' parameter cannot be empty.")
    
    # Execute the QA pipeline
    try:
        result = qa_pipeline(question=question, context=context)
        answer = result["answer"]
        return answer
    except Exception as e:
        print(f"Error in qa_pipeline: {e}")
        return "An error occurred while processing the question."
