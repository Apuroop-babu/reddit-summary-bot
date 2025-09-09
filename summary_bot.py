import praw
from transformers import pipeline
import time

reddit = praw.Reddit(
    client_id="gGzR1mwB5LC__YxTYKyhQQ",
    client_secret="a1oYwbozBweeo1kOEZ5MXXHLconNzA",
    username="Tldr_bot_1 ",
    password="apuroop@123",
    user_agent="PostSummarizerBot v1.0"
)

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def make_tldr(text, max_len=120, min_len=40):
    try:
        summary = summarizer(text, max_length=max_len, min_length=min_len, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        print("Error summarizing:", e)
        return None

subreddit = reddit.subreddit("test")  

print("🤖 TL;DR bot running...")

for comment in subreddit.stream.comments(skip_existing=True):
    body = comment.body.lower().strip()
    
    if "tldr" in body:
        submission = comment.submission
        content = (submission.title or "") + " " + (submission.selftext or "")
        
        if len(content.split()) < 50:  
            reply = "Post is already short enough, no TL;DR needed 🙂"
        else:
            tldr = make_tldr(content)
            reply = f"**TL;DR:** {tldr}" if tldr else "Sorry, I couldn't generate a summary 😔"
        
        try:
            comment.reply(reply)
            print(f"✅ Replied to comment {comment.id} with TL;DR")
        except Exception as e:
            print("❌ Failed to reply:", e)
        
        time.sleep(20)
