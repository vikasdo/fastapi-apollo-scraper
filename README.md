# fastapi-apollo-scraper
python3 -m venv env

source env/bin/activate
curl -X POST "http://localhost:8000/scrape?name=John&organization_name=Example%20Inc."

uvicorn main:app --reload

4w_TZeuO80DgSRdjkS4wBg