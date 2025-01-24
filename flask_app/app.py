from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

class ChatAssistant:
    def __init__(self, user_name):
        self.user_name = user_name
        self.projects = []

    def create_project(self, project_name, description):
        project = {
            "name": project_name,
            "description": description,
            "tasks": []
        }
        self.projects.append(project)
        return f"Project '{project_name}' created successfully!"

    def add_task(self, project_name, task_name, status="pending"):
        for project in self.projects:
            if project["name"] == project_name:
                project["tasks"].append({"task_name": task_name, "status": status})
                return f"Task '{task_name}' added to project '{project_name}'."
        return f"Project '{project_name}' not found."

    def view_projects(self, page=1, per_page=5):
        start = (page - 1) * per_page
        end = start + per_page
        paginated_projects = self.projects[start:end]
        return {
            "projects": paginated_projects,
            "total_projects": len(self.projects),
            "current_page": page,
            "total_pages": (len(self.projects) + per_page - 1) // per_page
        }

    def update_task_status(self, project_name, task_name, status):
        for project in self.projects:
            if project["name"] == project_name:
                for task in project["tasks"]:
                    if task["task_name"] == task_name:
                        task["status"] = status
                        return f"Task '{task_name}' status updated to '{status}' in project '{project_name}'."
        return f"Task '{task_name}' not found in project '{project_name}'."

    def delete_project(self, project_name):
        for project in self.projects:
            if project["name"] == project_name:
                self.projects.remove(project)
                return f"Project '{project_name}' deleted successfully."
        return f"Project '{project_name}' not found."

assistant = ChatAssistant("Talha")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/create_project_form')
def create_project_form():
    return render_template('create_project.html')

@app.route('/add_task_form')
def add_task_form():
    return render_template('add_task.html')

@app.route('/update_task_form')
def update_task_form():
    return render_template('update_task.html')

@app.route('/delete_project_form')
def delete_project_form():
    return render_template('delete_project.html')

@app.route('/create_project', methods=['POST'])
def create_project():
    data = request.form
    project_name = data.get('project_name')
    description = data.get('description')
    return jsonify({"message": assistant.create_project(project_name, description)})

@app.route('/add_task', methods=['POST'])
def add_task():
    data = request.form
    project_name = data.get('project_name')
    task_name = data.get('task_name')
    status = data.get('status', 'pending')
    return jsonify({"message": assistant.add_task(project_name, task_name, status)})

@app.route('/view_projects', methods=['GET'])
def view_projects():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 5))
    return jsonify(assistant.view_projects(page, per_page))

@app.route('/update_task_status', methods=['POST'])
def update_task_status():
    data = request.form
    project_name = data.get('project_name')
    task_name = data.get('task_name')
    status = data.get('status')
    return jsonify({"message": assistant.update_task_status(project_name, task_name, status)})

@app.route('/delete_project', methods=['POST'])
def delete_project():
    data = request.form
    project_name = data.get('project_name')
    return jsonify({"message": assistant.delete_project(project_name)})

if __name__ == '__main__':
    app.run(debug=True)
