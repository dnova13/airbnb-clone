FROM ubuntu:22.04

ARG USERNAME=ubuntu
ARG PW=1234

ARG PROJECT_NAME=airbnb-clone


ARG PYTHON_VERSION=3.9.4
ARG NODE_VERSION=16.20.0

## 환경 변수 설정
ENV HOME /root
ENV PYENV_ROOT $HOME/.pyenv
ENV PATH $PYENV_ROOT/bin:$PATH


RUN apt-get update && apt-get install -y \
    wget curl git vim nano nginx \
    openssh-server make build-essential \
    libssl-dev zlib1g-dev libffi-dev libbz2-dev libreadline-dev \
    supervisor postgresql-server-dev-all gettext
    # llvm libncurses5-dev \ 
    # libncursesw5-dev xz-utils liblzma-dev libc-dev libc6-dev \
    
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
WORKDIR /app/${PROJECT_NAME}
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
    && echo 'cd ${PROJECT_NAME}' >> $HOME/.bashrc 


RUN /app/myvenv/bin/pip install --upgrade pip 
RUN /app/myvenv/bin/pip install -r requirements.txt



# uwsgi, daphne 셋팅
RUN /app/myvenv/bin/pip install uwsgi && /app/myvenv/bin/pip install daphne
RUN mkdir -p /var/log/service
RUN chown  -R ${USERNAME}:${USERNAME} /var/log/service/

# source /var/app/venv/*/bin/activate
# RUN bash -c "/app/myvenv/bin/uwsgi -i /app/${PROJECT_NAME}/.config/uwsgi.ini"


# nginx 셋팅
COPY .config/nginx/my.conf /etc/nginx/sites-enabled/default
# COPY .config/nginx/my.conf /etc/nginx/conf.d/my.conf
# RUN /usr/sbin/nginx


#supervisor 설정
COPY .config/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
# RUN /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf

# Supervisor를 포그라운드 모드로 실행하도록 CMD 설정
# 관리자 아이디 생성(만약 관리자 아이디 생성시, db 먼저 생성후 실행) & 전 static 폴더 설정. 
CMD ["/bin/bash", "-c", "source /app/myvenv/bin/activate && python manage.py createsu && python manage.py collectstatic --noinput && python manage.py compilemessages && python manage.py migrate && /usr/bin/supervisord -n"]