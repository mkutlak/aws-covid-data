FROM debian:10-slim
ENV TERRAFORM_VERSION 0.12.28
ENV PACKAGES="curl git graphviz make python3-pip unzip zip"

RUN apt-get update && \
    apt-get install ${PACKAGES} --yes && \
    apt-get clean all && \
    pip3 install awscli diagrams


RUN cd /usr/local/bin && \
    curl https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip -o terraform_${TERRAFORM_VERSION}_linux_amd64.zip && \
    unzip terraform_${TERRAFORM_VERSION}_linux_amd64.zip && \
    rm -f terraform_${TERRAFORM_VERSION}_linux_amd64.zip && \
    mkdir -p /work && \
    git clone git://github.com/mkutlak/aws-covid-data.git /work

WORKDIR /work
CMD ["/bin/bash"]
