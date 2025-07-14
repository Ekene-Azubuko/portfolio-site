#!/bin/bash

echo "Creating a new post..."
POST_RESPONSE=$(curl -s -X POST http://127.0.0.1:5000/api/timeline_post -d "name=test&email=test@gmail.com&content=testing one two three")


POST_ID=$(echo $POST_RESPONSE | jq -r '.id')

echo "Created post with ID: $POST_ID"

# Get all posts
echo "Getting all posts..."
curl http://127.0.0.1:5000/api/timeline_post

# Delete the post using the extracted ID
echo "Deleting post with ID: $POST_ID"
curl -X DELETE http://127.0.0.1:5000/api/timeline_post/$POST_ID
