import requests
import csv
import time

API_TOKEN = 'ASK FOR CODE!'
LIST_ID = '901306528316'
HEADERS = {'Authorization': API_TOKEN}

# ---- Safe API GET with retry on 429 ----
def safe_api_get(url, max_retries=5):
    delay = 1  # Start with 1 second
    for attempt in range(max_retries):
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 429:
            print(f"⚠️ Hit rate limit (429). Retrying in {delay} seconds...")
            time.sleep(delay)
            delay *= 2  # Exponential backoff
        else:
            response.raise_for_status()
            return response
    raise Exception(f"❌ Failed after {max_retries} retries due to rate limiting.")

# ---- Step 1: Get all tasks ----
def get_all_tasks(list_id):
    tasks = []
    page = 0
    while True:
        url = f'https://api.clickup.com/api/v2/list/{list_id}/task?archived=false&page={page}'
        response = safe_api_get(url)
        data = response.json()
        tasks += data.get('tasks', [])
        if not data.get('tasks') or len(data.get('tasks')) < 100:
            break
        page += 1
    return tasks

# ---- Step 2: Get task comments ----
def get_task_comments(task_id):
    url = f'https://api.clickup.com/api/v2/task/{task_id}/comment'
    response = safe_api_get(url)
    data = response.json()
    return data.get('comments', [])

# ---- Step 3: CSV Export ----
def export_comments_to_csv(task_comments):
    with open('clickup_comments_export.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
            'Task ID', 'Task Name', 'Assignees', 'Task Status', 'Priority',
            'Comment Text', 'Comment Author', 'Comment Date'
        ])
        for entry in task_comments:
            writer.writerow(entry)

# ---- Main logic ----
def main():
    tasks = get_all_tasks(LIST_ID)
    all_comments = []

    for task in tasks:
        task_id = task['id']
        task_name = task['name']
        assignees = ', '.join([user['username'] for user in task.get('assignees', [])])
        status = task['status']['status']
        priority = task['priority']['priority'] if task.get('priority') else 'None'

        comments = get_task_comments(task_id)
        if not comments:
            all_comments.append([
                task_id, task_name, assignees, status, priority,
                '', '', ''
            ])
        else:
            for comment in comments:
                comment_text = comment.get('comment_text', '').replace('\n', ' ').strip()
                author = comment['user']['username'] if comment.get('user') else 'Unknown'
                date = comment['date']
                all_comments.append([
                    task_id, task_name, assignees, status, priority,
                    comment_text, author, date
                ])
        time.sleep(0.5)  # Light throttle to avoid rate limit buildup

    export_comments_to_csv(all_comments)
    print("✅ Export completed! File: clickup_comments_export.csv")

if __name__ == "__main__":
    main()
