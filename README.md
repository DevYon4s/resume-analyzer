## n8n-Driven Resume Analyzer (Secure & AI-Powered)

This project is a secure, AI-powered resume analyzer using FastAPI, n8n, PostgreSQL, and pgAdmin. It allows users to upload resumes in PDF format, which are then processed to extract key information using Gemini API. The extracted data is stored in a PostgreSQL database.

### steps to run the Project:

1. **Clone the Repository:**
   ```bash
    git clone https://github.com/DevYon4s/resume-analyzer.git
   ```
2. **Navigate to the Project Directory:**
   ```bash
   cd resume-analyzer
   ```
3. **Create a `.env` file:**

   ```bash
    touch .env

   ```

4. **Add Environment Variables:**
   Open the `.env` file and add the following variables:
   ```plaintext
   GEMINI_API_KEY=your_gemini_api_key
   ```
5. **Install Docker and Docker Compose:**
   Ensure you have Docker and Docker Compose installed on your machine.
6. **Run the Application:**
   Use Docker Compose to build and run the application:
   ```bash
   docker-compose up --build
   ```

### Backend:

- Runs on http://localhost:8000
- Swagger Docs: http://localhost:8000/docs

### Endpoints:

- `POST /auth/login` - Get JWT token hardcoded user

```plaintext

       username: admin
       password: password123

```

- `POST /upload` - Upload PDF (JWT protected)

### Docker Services:

- FastAPI Backend (port 8000)
- n8n Automation (port 5678)
- PostgreSQL (port 5432)
- pgAdmin (port 5050)

### n8n Setup:

- Open http://localhost:5678 and login to n8n.
- Create a new workflow and use import from file option and import the provided `workflows/resume_workflow.json` file.:
  -this will create a workflow that automates the resume upload and processing and has the following nodes:
  - **Webhook Trigger**: Set to listen on `/webhook/resume-upload`.
  - **Tika**: to parse the uploaded PDF file.
  - **Http Node**: this calls Gemini API for extracting resume data.
  - **PostgreSQL Node**: Insert the extracted data into the `resumes` table.

### pgAdmin Setup:

- Open http://localhost:5050
- Login: `admin@admin.com` / `admin`
- Create New Server:

```plaintext
  - Name: `ResumeDB`
  - Connection:
    - Host: `postgres`
    - Port: `5432`
    - Username: `resume`
    - Password: `resume123`
    - Database: `resumes`
```

-make sure you use the above options in the postgres node of n8n .

### Create Table SQL (inside pgAdmin Query Tool) in the `resumes` database:

```sql
CREATE TABLE resumes (
id SERIAL PRIMARY KEY,
filename TEXT,
full_name TEXT,
email TEXT,
phone TEXT,
skills TEXT[],
experience_years FLOAT,
last_job_title TEXT,
uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

# Example n8n Workflow (High Level Description)

1. Webhook Trigger (POST /webhook/resume-upload)
2. Tika Node (recvies binary data from read binary node)
   - Parses the PDF file to extract text content.
3. Call Geminiapi (prompt to extract: full_name, email, phone, skills, experience_years, last_job_title)
4. PostgreSQL Node: Insert the extracted data into `resumes` table
