FROM python:3-slim
WORKDIR /app
COPY app.py .
# FIXED: Explicitly pinning templates/rendering dependencies to protect the boot run
RUN pip install flask jinja2
EXPOSE 5000
CMD ["python", "app.py"]
