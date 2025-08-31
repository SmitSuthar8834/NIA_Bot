
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
