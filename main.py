import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Get the API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY is not set in the environment variables")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Mock data for calculations
user_performance = [0.5, -0.2, 1.0, -0.3, 0.7]
sp500_performance = [0.3, -0.1, 0.8, -0.2, 0.6]

# Function to calculate alpha
def calculate_alpha(user_returns, benchmark_returns):
    user_avg = sum(user_returns) / len(user_returns)
    benchmark_avg = sum(benchmark_returns) / len(benchmark_returns)
    return round(user_avg - benchmark_avg, 2)

# Main logic
def main():
    print("Welcome to Trading Performance Q&A")
    print("Ask questions like: 'What was my alpha last week?' or 'What is my average return?'")
    question = input("Your question: ")

    # Determine response content based on input
    if "alpha" in question.lower():
        alpha = calculate_alpha(user_performance, sp500_performance)
        response_content = f"Your alpha last week was {alpha}%."
    elif "average" in question.lower() or "performance" in question.lower():
        avg_return = round(sum(user_performance) / len(user_performance), 2)
        response_content = f"Your average return last week was {avg_return}%."
    else:
        response_content = "I couldn't understand your question. Please try asking about alpha or average performance."

    # Use OpenAI Chat Completion
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a trading assistant. You have access to mock performance data for calculations: "
                        "User's daily returns: [0.5, -0.2, 1.0, -0.3, 0.7], "
                        "S&P 500 returns: [0.3, -0.1, 0.8, -0.2, 0.6]. "
                        "Use this data to calculate alpha, average return, or any other trading metrics requested."
                    )
                },
                {"role": "user", "content": question},
                {"role": "assistant", "content": response_content}
            ]
        )

        # Access the response correctly using attributes
        gpt_response = completion.choices[0].message.content.strip()
        print("GPT Response:", gpt_response)
    except Exception as e:
        print(f"Error generating response: {e}")

if __name__ == "__main__":
    main()