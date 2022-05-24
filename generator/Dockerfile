FROM python:3.7

# Without this setting, Python never prints anything out.
ENV PYTHONUNBUFFERED=1

# declare the source directory
COPY requirements.txt /
RUN pip install -r /requirements.txt
# copy the file
COPY Generator.py .

# start command
CMD [ "python", "Generator.py" ]