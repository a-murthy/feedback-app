FROM python:3-slim
WORKDIR /app
COPY app.py .
# 🟢 Added 'requests' to ensure outbound connectivity to your Add-On endpoint functions flawlessly
RUN pip install flask jinja2 requests
EXPOSE 5000
CMD ["python", "app.py"]
