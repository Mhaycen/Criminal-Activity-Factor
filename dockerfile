FROM puckel/docker-airflow:1.10.9

WORKDIR /airflow
RUN pip3 install gdelt
