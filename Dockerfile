#the first line is telling we gonna build a container with an image of python 3
FROM python:3

#this where all the app code will be in the container
WORKDIR /usr/src/app 

#copy is an instruccion to copy that file from this directory
COPY requirements.txt ./  

#run this command in the container
RUN pip install --no-cache-dir -r requirements.txt 

#copy all the code in the container
COPY . .  

#run this command in the container 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]