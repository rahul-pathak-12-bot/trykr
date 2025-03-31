# TDS Solver

An API that automatically answers questions from IIT Madras' Online Degree in Data Science graded assignments.

## Features

- Accepts questions and optional file attachments
- Processes various file types including CSVs and ZIP files
- Returns accurate answers for graded assignments

## API Usage

### Endpoint

`POST https://your-deployed-url.vercel.app/api/`

### Request Format

Send a `multipart/form-data` request with:
- `question`: The assignment question text
- `file`: (Optional) Any file attachment mentioned in the question

### Example

```bash
curl -X POST "https://your-deployed-url.vercel.app/api/" \
  -H "Content-Type: multipart/form-data" \
  -F "question=Download and unzip file abcd.zip which has a single extract.csv file inside. What is the value in the \"answer\" column of the CSV file?" \
  -F "file=@abcd.zip"