"""Create and publish a batch of Chat requests using xai_sdk.

This mirrors the snippet you provided and publishes the batch.
"""
from xai_sdk import Client
from xai_sdk.chat import system, user
import uuid


def main():
    client = Client()

    # Sample data to process
    feedback_items = [
        {"id": "feedback_001", "text": "The product exceeded my expectations!"},
        {"id": "feedback_002", "text": "Shipping took way too long."},
        {"id": "feedback_003", "text": "It works as described, nothing special."},
    ]

    # Create a batch (use a generated id if you don't have one)
    batch_id = str(uuid.uuid4())
    batch = client.batch.create(batch_id=batch_id)

    # Build batch requests using Chat objects
    batch_requests = []
    for item in feedback_items:
        chat = client.chat.create(
            model="grok-4-1-fast-reasoning",
            batch_request_id=item["id"],
        )
        chat.append(system("Classify the sentiment as positive, negative, or neutral."))
        chat.append(user(item["text"]))
        batch_requests.append(chat)

    # Add requests to the batch and publish
    client.batch.add(batch_id=batch.batch_id, batch_requests=batch_requests)
    client.batch.publish(batch_id=batch.batch_id)

    print(f"Added {len(batch_requests)} requests to batch {batch.batch_id} and published it")


if __name__ == "__main__":
    main()
