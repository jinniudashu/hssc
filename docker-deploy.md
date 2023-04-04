## Docker部署
### 开发环境
1. 生成镜像：docker-compose -f docker-compose-build.yml build
2. tag: docker tag clinic_app:v1 jinniudashu/clinic_app:v1
3. push: docker push jinniudashu/clinic_app:v1
### 生产环境
1. 进入项目目录：cd clinic-test
2. 查看容器：docker ps
3. 停止容器：docker stop clinic_app 等4个容器
4. 删除容器：docker rm clinic_app 等4个容器
5. 查看镜像：docker images
6. 删除镜像：docker rmi clinic_app
7. 查看volume：docker volume ls
8. 删除volume：docker volume rm clinic-test_clinic-pgdata
9. 下载镜像：docker pull jinniudashu/clinic_app:v1
10. 启动容器：docker-compose -f docker-compose-init-up.yml up
11. 进入容器：docker exec -it clinic-test-app-1 /bin/sh
12. 创建管理员：python manage.py createsuperuser
13. 退出：exit