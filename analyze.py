import time
import json
import csv
from mistralai import Mistral

# --- CONFIGURATION ---
API_KEY = "mistral-experimental-key"  # <--- PASTE KEY HERE
MODEL_NAME = "mistral-small-latest"

CATEGORIES = ["Lecturer/Professor", "Homework", "Course Content", "Facilities", "Grading & Exams", "Project", "Schedule", "Other"]

# Sample data (You can replace this with real data later)
comments = [
    "The lectures were fantastic and really kept my attention.",
    "I felt completely lost during the second half of the semester.", 
    "The workload was way too heavy for an introductory course. ",
    "It was okay, but I wish the slides were posted online sooner.",
    "The group project was a nightmare because my partners didn't do anything.", 
    "Best professor I've had so far, very understanding and kind.",
    "Please stop reading directly off the PowerPoint slides.",
    "I really appreciated the detailed feedback on my essay.",
    "The textbook was incredibly expensive and we barely opened it.",
    "Solid class, I learned exactly what I expected to.",
    "The exam questions had nothing to do with what we covered in class.",
    "I loved the guest speakers, they brought a cool perspective.",
    "The room is always freezing cold, which makes it hard to focus.",
    "Grading takes way too long, I didn't know my standing until the final week.",
    "The content is fascinating, but the 8:00 AM slot is brutal.",
    "I think the prerequisites for this course need to be updated." ,
    "The TAs were actually more helpful than the main lectures.",
    "Easy A if you just show up and turn things in on time.",
    "The syllabus was confusing and dates kept changing without notice.",
    "I would definitely take another class with this instructor.",
    "The labs were fun, but the equipment is really outdated.",
    "I didn't feel like my grade reflected the effort I put in.",
    "Great course, but there was too much required reading.",
    "The pacing was weird; we rushed through the most important topics at the end.",
    "I usually hate this subject, but this class made it bearable.",
    "The instructions for the final project were extremely vague.",
    "Nothing special, just a standard requirement filler.",
    "I really liked how the course connected theory to real-world events.",
    "Please offer more office hours, the current times conflict with other classes.",
    "I felt very supported throughout the entire term.",
    "The recorded lectures saved my life when I got sick, thank you for providing them.",
    "I still don't understand the grading criteria for the final paper.",
    "This course changed my career path, I absolutely loved it.",
    "The classroom was too small for the number of students enrolled.",
    "Please provide more examples when explaining the math concepts.",
    "I felt like the professor was condescending when answering questions.",
    "The textbook was actually really helpful and easy to read.",
    "Assignments were spaced out well so I never felt overwhelmed.",
    "I wish we had more opportunities for class discussion instead of just listening.",
    "The final exam was fair and covered exactly what was on the study guide.",
    "It felt like two different courses mashed into one.",
    "I would not recommend this class to anyone who isn't a major.",
    "The instructor's enthusiasm made 8 AM lectures worth waking up for.",
    "There was way too much homework for a 2-credit class.",
    "I liked the material, but the disorganized Moodle page made it hard to find things.",
    "The peer review sessions were a waste of time because nobody took them seriously.",
    "Great refresher on the basics, but I was hoping for more advanced topics.",
    "The professor needs to learn how to use the microphone properly.",
    "I appreciated the flexibility with deadlines.",
    "The quizzes were tricky, but they forced me to actually do the reading.",
    "I felt like a number in this class, not a student.",
    "The TA was harsh and graded totally differently than the professor.",
    "Honestly, this was the easiest A I’ve ever gotten.",
    "The software we had to use was buggy and frustrated everyone.",
    "I loved the variety of media used in the lectures, like the videos and podcasts.",
    "The syllabus said one thing, but we did something completely different.",
    "Please post the slides before class so we can take notes on them.",
    "I really struggled with the pace of this course.",
    "The feedback on my assignments was generic and didn't help me improve.",
    "This class gave me practical skills I can actually put on my resume.",
    "The professor cancelled class way too often.",
    "I wish the attendance policy wasn't so strict.",
    "The midterm was brutal, but the curve saved me.",
    "I enjoyed the group work more than I thought I would.",
    "The lectures were repetitive and could have been summarized in an email.",
    "I didn't learn much new information, but it was a good review.",
    "The professor was very accessible and helpful during office hours.",
    "I hate that we had to pay extra for the online homework platform.",
    "The connection between the lectures and the lab work was seamless.",
    "I felt unprepared for the final based on the homework assignments.",
    "This was a waste of tuition money.",
    "The guest lecturer in week 5 was the highlight of the semester.",
    "I think the course description needs to be updated to match what we actually did.",
    "Very organized and well-structured course.",
    "I was intimidated at first, but the supportive environment helped me succeed."
]

def get_analysis(client, text):
    """Asks Mistral for both Category and Sentiment in JSON format."""
    
    # Strict prompt for JSON output
    prompt = (
        f"Analyze this text: '{text}'. "
        f"1. Classify it into one of these categories: {CATEGORIES}. "
        "2. Determine sentiment: 'Positive', 'Negative', or 'Neutral'. "
        "3. Return ONLY a valid JSON object like: "
        '{"category": "...", "sentiment": "..."}'
    )

    try:
        response = client.chat.complete(
            model=MODEL_NAME,
            messages=[
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"} # Forces JSON mode
        )
        
        # Parse the string response into a real Python dictionary
        content = response.choices[0].message.content
        return json.loads(content)
        
    except Exception as e:
        print(f"Error: {e}")
        return {"category": "Error", "sentiment": "Error"}

def analyze_all():
    if "YOUR_MISTRAL" in API_KEY:
        print("❌ Error: Please put your actual API Key in analyze.py")
        return []

    client = Mistral(api_key=API_KEY)
    results = []

    print("🚀 Starting analysis...")
    
    for i, comment in enumerate(comments):
        print(f"Processing {i+1}/{len(comments)}: {comment[:30]}...")
        data = get_analysis(client, comment)
        
        # Combine the comment with the AI's answer
        row = {
            "id": i + 1,
            "text": comment,
            "category": data.get("category", "Unknown"),
            "sentiment": data.get("sentiment", "Neutral")
        }
        results.append(row)
        time.sleep(1) # Sleep to avoid rate limits

    # Save to a file so app.py can read it
    with open("data.json", "w") as f:
        json.dump(results, f, indent=4)
    
    print("✅ Analysis complete! Saved to data.json")
    return results

if __name__ == "__main__":
    analyze_all()