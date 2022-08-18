#FROM public.ecr.aws/lambda/python:3.8
FROM python:3.7
MAINTAINER "vinod.lakk@gmail.com"
RUN mkdir /code
ADD . /code
WORKDIR /code
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["python", "/code/app.py"]
