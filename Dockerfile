FROM ubuntu:22.04

ARG USERNAME=ubuntu
ARG PW=1234


ARG PYTHON_VERSION=3.9.4
ARG NODE_VERSION=16.20.0

## 환경 변수 설정
ENV HOME /root
ENV PYENV_ROOT $HOME/.pyenv
ENV PATH $PYENV_ROOT/bin:$PATH


RUN apt-get update && apt-get install -y \
    wget curl git vim nano nginx \
    openssh-server \
    make build-essential libssl-dev zlib1g-dev \
    libffi-dev libbz2-dev libreadline-dev llvm libncurses5-dev \ 
    libncursesw5-dev xz-utils liblzma-dev postgresql-server-dev-all libc-dev libc6-dev \
    supervisor
    #  tk-dev  \
    
# Create a directory for SSH daemon to run
RUN mkdir /var/run/sshd

# optional 둘중하나 선택 또는 모두
# root 암호 설정 
RUN echo "root:${PW}" | chpasswd

# 새로운 사용자 생성
RUN useradd -m -s /bin/bash ${USERNAME}
RUN echo "${USERNAME}:${PW}" | chpasswd 
RUN usermod -aG sudo,${USERNAME} ${USERNAME}

# python 설치 및 설정
## pyenv 설치
RUN curl https://pyenv.run | bash

## pyenv 초기화 설정
RUN echo 'export PYENV_ROOT="$HOME/.pyenv"' >> $HOME/.bashrc \
    && echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> $HOME/.bashrc \
    && echo 'eval "$(pyenv init --path)"' >> $HOME/.bashrc \
    && echo 'eval "$(pyenv init -)"' >> $HOME/.bashrc \
    && echo 'eval "$(pyenv virtualenv-init -)"' >> $HOME/.bashrc

## pyenv를 사용하여 Python 설치 (예: Python 3.7.9)
RUN bash -c "source $HOME/.bashrc && pyenv install ${PYTHON_VERSION}"

## pyenv 글로벌 Python 버전 설정
RUN bash -c "pyenv global ${PYTHON_VERSION}"

# ssh 서버 설정
## sed 커맨를 이용한 문자열 변경.
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

# SSH PORT
EXPOSE 22

# Start SSH service
RUN /usr/sbin/sshd


# project settings
WORKDIR /app/airbnb-clone
COPY . .

# node 셋팅
## node 설치
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash
RUN /bin/bash -c "source $HOME/.nvm/nvm.sh \
    && nvm install ${NODE_VERSION} \
    && nvm use ${NODE_VERSION} \
    && npm install"



# # 프로젝트 폴더 생성 및 권한 설정
# RUN chown -R ${USERNAME}:${USERNAME} /app

# venv 설정
## Docker 이미지 빌드 과정에서 사용하는 쉘은 이미지 빌드를 위한 임시 쉘이라서 
## .bashrc 파일은 로드되지 않아서 pyenv로 설치한 python 으로 정상적으로 추가되지 않아서
## pyenv 로 설정한 python -m venv 안먹힘.
RUN /root/.pyenv/shims/python -m venv /app/myvenv
RUN echo "cd /app" >> $HOME/.bashrc \
    && echo 'source myvenv/bin/activate' >> $HOME/.bashrc \
    && echo 'cd airbnb-clone' >> $HOME/.bashrc 


RUN /app/myvenv/bin/pip install --upgrade pip 
RUN /app/myvenv/bin/pip install -r requirements.txt

# uwsgi, daphne 셋팅
RUN /app/myvenv/bin/pip install uwsgi && /app/myvenv/bin/pip install daphne
RUN mkdir -p /var/log/service
RUN chown  -R ${USERNAME}:${USERNAME} /var/log/service/

# RUN bash -c "/app/myvenv/bin/uwsgi -i /app/airbnb-clone/.config/uwsgi.ini"


# nginx 셋팅
COPY .config/nginx/my.conf /etc/nginx/sites-enabled/default
# COPY .config/nginx/my.conf /etc/nginx/conf.d/my.conf
# RUN /usr/sbin/nginx


#supervisor 설정
COPY .config/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
# RUN /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf

# Supervisor를 포그라운드 모드로 실행하도록 CMD 설정
CMD ["/usr/bin/supervisord", "-n"]
# CMD /usr/bin/supervisord -n 


# RUN supervisorctl start uwsgi
# RUN supervisorctl start uwsgi

# service 설정
## uwsgi 및 daphne 서비스 파일 복사
# COPY .config/uwsgi /etc/init.d/uwsgi
# COPY .config/daphne /etc/init.d/daphne

## 서비스 스크립트에 실행 권한 부여
# RUN chmod +x /etc/init.d/uwsgi /etc/init.d/daphne

## init 시스템 실행
# RUN /sbin/init
# CMD ["/sbin/init"]

