pipeline {
    agent {
        label 'agent-in-docker'
        //  label 'agent-in-django'
        
    }
    // triggers {
    //     // 5분 마다 git 에 새로운 코드가 있으면 빌드를 실행함.
    //     pollSCM '*/5 * * * *'
    // }
    environment {
        // RDS_TEST_HOST = credentials('RDS_TEST_HOST')
        // RDS_TEST_HOST = "postgres"
        RDS_TEST_NAME = credentials('RDS_TEST_NAME')
        RDS_TEST_USER = credentials('RDS_TEST_USER')
        RDS_TEST_PASSWORD = credentials('RDS_TEST_PASSWORD')
        
        RDS_NAME = credentials('RDS_TEST_NAME')
        RDS_USER = credentials('RDS_TEST_USER')
        RDS_PW = credentials('RDS_TEST_PASSWORD')
        
        TIME_ZONE="Asia/Seoul"

        DOCKER_ID = credentials('DOCKER_ID')
        DOCKER_ACC_KEY = credentials('DOCKER_ACC_KEY')
        
        JENKINS_PROJECT="${env.JOB_NAME}"
        PROJECT_NAME="airbnb-clone"

    }
    stages {
        stage('Git Clone') {
            steps {
                git branch: 'master',
                url: 'https://github.com/dnova13/airbnb-clone', 
                // 레포지토리가 private 일경우, credentials 에 설정한 git 계정 정보를 설정
                credentialsId: 'git-signin'

            }
            
            post {
                success { 
                    sh '##################### echo "Successfully Cloned Repository"'
                }
                failure {
                    sh '##################### echo "Fail Cloned Repository"'
                }
            }    
        }

        stage('Generate .env file') {
            steps {

                // echo "RDS_TEST_HOST=postgres" >> .env
                sh '''
                echo "RDS_TEST_NAME=${RDS_TEST_NAME}" >> .env
                echo "RDS_TEST_USER=${RDS_TEST_USER}" >> .env
                echo "RDS_TEST_PASSWORD=${RDS_TEST_PASSWORD}" >> .env
                
                echo "RDS_NAME=${RDS_TEST_NAME}" >> .env
                echo "RDS_USER=${RDS_TEST_USER}" >> .env
                echo "RDS_PW=${RDS_TEST_PASSWORD}" >> .env
                echo "TIME_ZONE=Asia/Seoul" >> .env
                '''
                sh 'cat .env '
            }
        }

        stage('postgres test') {
            steps {

                // sh 'docker rm -f postgres'
                sh'docker-compose -f docker-compose.test-postgres.yml up postgres -d --build'
                
                sh'''
                docker cp ./.postgresql/init/ testDB:/docker-entrypoint-initdb.d/
                docker exec -i testDB psql --version
                docker exec -i testDB ls -l /docker-entrypoint-initdb.d/init
                '''
                
                // SQL 실행
                sh'docker exec -u root -i testDB psql -U postgres -f /docker-entrypoint-initdb.d/init/postgres_dump202407092055_freetier_back.sql'
            }
            post {
                success {
                    echo '##################### postgres build success'
                }

                failure {
                    echo '##################### postgres build failed'
                }
            }
        }

        // postgres docker container 를 agent 에 연결된 jenkins docker network에 연결
        stage("docker network connect") {
            steps {
                script {
                    echo "postgres connnect to jenkins docker network."
                    // 이미 연결됐다고 에러나도 그냥 넘김.
                    sh(
                        script: 'docker network connect jenkins testDB',
                        returnStatus: true
                        )
                }
            }
        }
        
        stage('django server test') {
            steps {
                script {
                	// postgresip 추출
                	// def postgresIP = sh(script: "docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' postgres-test", returnStdout: true).trim()
                    // echo "A Container IP: ${postgresIP}"
                    
                    // groov 에서 정의된 변수 쓰고 싶다면 "" 가 아닌  """ 한다.
                    // sh """echo 'RDS_TEST_HOST=${postgresIP}' >> .env"""
                    sh """echo 'RDS_TEST_HOST=testDB' >> .env"""
                    
                    sh 'cat .env'
                    sh 'docker network inspect jenkins'
                    sh 'cat test_settings.py'
                    sh 'sleep 10'

                	
                    sh '''
                    # 가상환경 셋팅 및 패키지 설치
                    python3 -m venv ./myvenv
                    . myvenv/bin/activate
                    pip install --upgrade pip 
                    pip install -r requirements.txt
                    
                    # 실행 테스트
                    docker ps 
                    python manage.py test --settings='config.test_settings'
                    '''
                }
            }
            post {
                success {
                    echo '##################### django test success'
                }

                failure {
                    echo '##################### django test failed'
                    sh'docker rm -f testDB'
                }
            }
        }
        stage('Build Docker Push') {
            steps {
                sh 'docker login -u $DOCKER_ID -p $DOCKER_ACC_KEY'
                sh '''

                echo "The project name is $PROJECT_NAME"

                
                # 나머지 compose 이미지 빌드
                docker-compose build redis
                docker-compose build postgres
                docker-compose build django

                # docker tag
                docker tag $JENKINS_PROJECT-django $DOCKER_ID/$PROJECT_NAME-django:latest
                docker tag $JENKINS_PROJECT-postgres $DOCKER_ID/$PROJECT_NAME-postgres:latest
                docker tag $JENKINS_PROJECT-redis $DOCKER_ID/$PROJECT_NAME-redis:latest
                # docker tag $JENKINS_PROJECT-webserver $DOCKER_ID/$PROJECT_NAME-webserver:latest

                # docker push
                docker push $DOCKER_ID/$PROJECT_NAME-django
                docker push $DOCKER_ID/$PROJECT_NAME-postgres
                docker push $DOCKER_ID/$PROJECT_NAME-redis
                # docker push $DOCKER_ID/$PROJECT_NAME-webserver
                '''
            }
            post {
                success {
                    echo '##################### docker push success'
                }
                failure {
                    echo '##################### docker push failed'
                }
                always {
                    sh'docker rm -f testDB'
                }
            }
        }
        stage('SSH Deploy') {
            steps {        
                // sshagent (credentials: ['ec3-test']) {
                sshagent (credentials: ['local-server']) {
                sh """
                    # ssh -o StrictHostKeyChecking=no ubuntu@3.39.6.193 '
                    ssh -o StrictHostKeyChecking=no test@36.38.247.69 '
                        # 도커 허브 로그인
                        docker login -u $DOCKER_ID -p $DOCKER_ACC_KEY

                        mkdir -p ~/project/$PROJECT_NAME

                        # Docker Compose로 애플리케이션 빌드 및 실행
                        cd ~/project/$PROJECT_NAME

                        sudo docker pull $DOCKER_ID/$PROJECT_NAME-django:latest
                        sudo docker pull $DOCKER_ID/$PROJECT_NAME-postgres:latest
                        sudo docker pull $DOCKER_ID/$PROJECT_NAME-redis:latest

                        sudo docker network create django-network

                        # postgres 도커 실행
                        sudo docker run -d \
                            --name postgres \
                            --memory=128m \
                            --restart=unless-stopped \
                            -v ./.postgresql/postgres_data/:/var/lib/postgresql/data/ \
                            -v ./.postgresql/init/:/docker-entrypoint-initdb.d/ \
                            -e POSTGRES_PASSWORD=$RDS_PW \
                            -e POSTGRES_DB=$RDS_NAME \
                            -e POSTGRES_USER=$RDS_USER \
                            -e TZ=$TIME_ZONE \
                            -p 5432:5432 \
                            --expose=5432 \
                            --network=django-network \
                            $DOCKER_ID/$PROJECT_NAME-postgres


                        # redis 도커 실행
                        sudo docker rm -f redis
                        sudo docker run -d \
                        --name redis \
                        --memory=256m \
                        --restart=on-failure \
                        -v ./.redis/redis_data/:/data/ \
                        -v ./.redis/my-redis.conf:/usr/local/etc/redis/redis.conf \
                        --network=django-network \
                        $DOCKER_ID/$PROJECT_NAME-redis

                        # django 백업 실행
                        echo "-------------------------- django backup rebuild ------------------------------"
                        sudo docker run -d \
                            --name django-backup \
                            --restart=on-failure \
                            -v ./uploads/:/app/airbnb-clone/uploads/:rw \
                            -v ./.config/nginx/my.conf:/etc/nginx/sites-enabled/default \
                            -v ./.config/supervisord.conf:/etc/supervisor/conf.d/supervisord.conf \
                            -v ./.log/service/:/var/log/service/ \
                            -v ./.log/nginx/:/var/log/nginx/ \
                            -v ./local_settings.py:/app/airbnb-clone/local_settings.py \
                            -v ./.env:/app/airbnb-clone/.env \
                            --expose=80 \
                            --expose=2000 \
                            --network=django-network \
                            $DOCKER_ID/$PROJECT_NAME-django

                        # webserver 백업 실행
                        echo "-------------------------- webserver backup exec ------------------------------"
                        sudo docker rm -f webserver  
                        sudo docker run -d \
                            --name webserver-backup \
                            --memory=256m \
                            --restart=always \
                            -v ./.webserver/default_backup.conf:/etc/nginx/conf.d/default.conf \
                            -v ./.webserver/logs:/var/log/nginx \
                            -p 80:80 \
                            -p 443:443 \
                            --network=django-network \
                            nginx:latest

                        # django 실행
                        echo "-------------------------- django rebuild ------------------------------"
                        sudo docker rm -f django
                        sudo docker run -d \
                            --name django \
                            --restart=on-failure \
                            -v ./uploads/:/app/airbnb-clone/uploads/:rw \
                            -v ./.config/nginx/my.conf:/etc/nginx/sites-enabled/default \
                            -v ./.config/supervisord.conf:/etc/supervisor/conf.d/supervisord.conf \
                            -v ./.log/service/:/var/log/service/ \
                            -v ./.log/nginx/:/var/log/nginx/ \
                            -v ./local_settings.py:/app/airbnb-clone/local_settings.py \
                            -v ./.env:/app/airbnb-clone/.env \
                            --expose=80 \
                            --expose=2000 \
                            --network=django-network \
                            $DOCKER_ID/$PROJECT_NAME-django

                        echo "-------------------------- backup clear ------------------------------"
                        sudo docker rm -f django-backup
                        sudo docker rm -f webserver-backup   

                        echo "-------------------------- webserver exec ------------------------------"
                        sudo docker run -d \
                            --name webserver \
                            --memory=256m \
                            --restart=always \
                            -v ./.webserver/default.conf:/etc/nginx/conf.d/default.conf \
                            -v ./.webserver/logs:/var/log/nginx \
                            -p 80:80 \
                            -p 443:443 \
                            --network=django-network \
                            nginx:latest

                    '
                """
                }
            }
        }
    }
    
    post {
        always {
            script {
                // sh 'docker-compose down -v --rmi all'
                sh 'docker system prune -f'
                // sh 'docker volume prune -f'
            }
        }
    }
}