## 从开发环境生成运行时代码
0. 在settings.py中设置PROJECT_NAME
1. 从设计系统导入脚本：python manage.py import_design
2. 初始化业务系统：python dev_initial.py
    - 删除原有migrations文件：python delete_initial_migrations.py
    - 生成migrations文件：python manage.py makemigrations
    - 生成数据库：python manage.py migrate
    - loaddata：python manage.py loaddata initial_data.json
    - 初始化业务系统配置：python manage.py init_core_data
    - 恢复业务数据（如果有）: python manage.py loaddata ./backup/backup.json

## Docker部署
### 开发环境
0. python manage.py collectstatic
1. 生成镜像：docker-compose -f docker-compose-build.yml build
2. push: docker push jinniudashu/clinic_app:v1
### 生产环境，使用SSH连接到服务器
1. 进入项目目录：docker-compose down
2. 删除旧镜像：docker rmi jinniudashu/clinic_app:v1
3. 下载镜像：docker pull jinniudashu/clinic_app:v1
4. 启动容器：docker-compose up
5. 进入容器：docker exec -it clinic /bin/sh
6. 创建管理员：python manage.py createsuperuser
7. 退出：exit