
#!/usr/bin/env python

import sys
import warnings
from datetime import datetime

from blog_writing_crew.crew import BlogWritingCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def get_inputs():
    """Collect blog details from the terminal."""

    print("\n======================================")
    print("       INK & ENCHANTMENT")
    print("       AI BLOG WRITING STUDIO")
    print("======================================\n")

    topic = input("Enter your blog topic: ").strip()

    if not topic:
        print("Please enter a valid topic.")
        return None

    target_audience = input(
        "Who is the target audience? (Default: General readers): "
    ).strip() or "General readers"

    tone = input(
        "Choose writing tone (Default: Informative): "
    ).strip() or "Informative"

    length = input(
        "Choose article length (Short/Medium/Long, Default: Medium): "
    ).strip() or "Medium"

    return {
    "topic": topic,
    "target_audience": target_audience,
    "tone": tone,
    "length": length,
    "words": length,
    "current_year": str(datetime.now().year)
}


def run():
    """Run the blog research and writing crew."""

    inputs = get_inputs()

    if inputs is None:
        return

    print("\nResearching your topic...")
    print("Your Researcher and Writer agents are starting.\n")

    try:
        result = BlogWritingCrew().crew().kickoff(inputs=inputs)

        print("\n======================================")
        print("       BLOG GENERATION COMPLETED!")
        print("======================================")
        print("Check blog.md for your generated article.")

        return result

    except Exception as e:
        print("\nBlog generation failed.")
        print(f"Error: {e}")
        raise


def train():
    inputs = get_inputs()

    if inputs is None:
        return

    BlogWritingCrew().crew().train(
        n_iterations=int(sys.argv[1]),
        filename=sys.argv[2],
        inputs=inputs
    )


def replay():
    BlogWritingCrew().crew().replay(task_id=sys.argv[1])


def test():
    inputs = get_inputs()

    if inputs is None:
        return

    BlogWritingCrew().crew().test(
        n_iterations=int(sys.argv[1]),
        eval_llm=sys.argv[2],
        inputs=inputs
    )
