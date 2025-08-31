#!/usr/bin/env python3
"""
Upload workflow to hosted n8n on Render
"""

import requests
import json

def upload_workflow_to_n8n():
    """Upload the workflow to your hosted n8n"""
    
    # Your n8n details
    n8n_url = "https://n8n-latest-rwjr.onrender.com"
    workflow_id = "2m1ocV53Tirgs3eI"
    
    # Load the workflow
    with open('n8n_workflow_render.json', 'r') as f:
        workflow = json.load(f)
    
    print(f"🚀 Uploading workflow to: {n8n_url}")
    
    # Update the workflow to use localhost (since n8n is hosted but bot is local)
    # The hosted n8n will send requests to your local bot
    
    try:
        # Method 1: Try to update existing workflow
        update_url = f"{n8n_url}/rest/workflows/{workflow_id}"
        
        print(f"Attempting to update workflow at: {update_url}")
        
        # Note: This requires authentication which we don't have
        # So let's create instructions instead
        
        print("❌ Direct API upload requires authentication")
        print("\n📋 Manual Upload Instructions:")
        print(f"1. Go to: {n8n_url}")
        print("2. Open your existing workflow")
        print("3. Click 'Settings' → 'Import from file'")
        print("4. Select: n8n_workflow_render.json")
        print("5. Or copy the JSON content and paste it")
        
        return False
        
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        return False

def create_render_instructions():
    """Create instructions for manual upload"""
    
    instructions = """
# Upload Workflow to Render n8n

## Method 1: Import File
1. Go to: https://n8n-latest-rwjr.onrender.com
2. Navigate to your workflow: https://n8n-latest-rwjr.onrender.com/workflow/2m1ocV53Tirgs3eI
3. Click the "..." menu → "Duplicate"
4. In the new workflow, click "..." → "Import from file"
5. Select: n8n_workflow_render.json

## Method 2: Copy JSON
1. Open n8n_workflow_render.json
2. Copy all the JSON content
3. Go to your n8n workflow
4. Click "..." → "Import from clipboard"
5. Paste the JSON

## Method 3: Manual Update
Update the HTTP Request node in your existing workflow:

**URL:** Change to: `http://localhost:5000/n8n/webhook`
**Body:** Update to:
```json
{
  "meeting_link": "{{ $json.hangoutLink }}",
  "auto_join": true,
  "enhanced": true,
  "event_title": "{{ $('Get an event').item.json.summary }}",
  "event_start": "{{ $('Get an event').item.json.start.dateTime }}"
}
```

## Important Notes:
- Your n8n is hosted on Render
- Your bot runs locally (localhost:5000)
- n8n will send HTTP requests from Render to your local machine
- Make sure your local bot is running and accessible

## Testing:
1. Start your local bot: `python app.py`
2. Run the workflow in n8n
3. Check if meetings are sent to your local bot
"""
    
    with open('RENDER_N8N_INSTRUCTIONS.md', 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    print("📝 Instructions saved to: RENDER_N8N_INSTRUCTIONS.md")

if __name__ == "__main__":
    print("🤖 n8n Render Upload Tool")
    
    # Try to upload (will show instructions)
    upload_workflow_to_n8n()
    
    # Create manual instructions
    create_render_instructions()
    
    print("\n✅ Ready to upload to your hosted n8n!")
    print("Check RENDER_N8N_INSTRUCTIONS.md for detailed steps")