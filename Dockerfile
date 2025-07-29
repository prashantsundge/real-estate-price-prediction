
#use official python image
FROM python:3.10-slim

#set working directory
WORKDIR /app
#copy Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


#COPY all project files
COPY . .

#set environment variable 
ENV PYTHONUNBUFFERED=1

#Expose ports
EXPOSE 8000 8501

#Entry Command (override in docker-compose)
CMD ['streamlit' , 'run', 'app.py']
