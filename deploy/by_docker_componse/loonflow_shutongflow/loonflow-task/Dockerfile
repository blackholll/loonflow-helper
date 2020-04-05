FROM centos:7
LABEL maintainer blackholll@163.com
# 安装基础包
RUN yum install -y mysql-devel gcc gcc-devel python3 python3-pip python3-dev python3-devel mysql-devel zlib-devel openssl-devel openssl-devel git nginx
RUN mkdir -p /var/log/loonflow
WORKDIR /opt
# RUN git clone https://github.com/blackholll/loonflow.git
RUN git clone https://gitee.com/shihowcom/loonflow_ro
WORKDIR /opt/loonflow_ro
RUN git checkout r1.0.1
WORKDIR /opt
RUN mv loonflow_ro loonflow
WORKDIR /opt/loonflow/requirements
RUN pip3 install -r pro.txt -i http://pypi.douban.com/simple/ --trusted-host=pypi.douban.com
# 复制config.py文件
WORKDIR /opt/loonflow/settings
RUN cp pro.py.simple config.py
# 修改redis配置
RUN sed -i "/REDIS_HOST = '127.0.0.1'/cREDIS_HOST = 'loonflow-redis'" /opt/loonflow/settings/config.py
RUN sed -i "/REDIS_PASSWORD = ''/cREDIS_HOST = 'loonflow123'" /opt/loonflow/settings/config.py

# 修改数据库配置
RUN sed -i "/'NAME': 'loonflownew1'/c'NAME': 'loonflow'" /opt/loonflow/settings/config.py
RUN sed -i "/'USER': 'loonflownew1'/c'USER': 'loonflow'" /opt/loonflow/settings/config.py
RUN sed -i "/'PASSWORD': '123456'/c'PASSWORD': 'loonflow123,.Ly'" /opt/loonflow/settings/config.py
RUN sed -i "/'HOST': '127.0.0.1'/c'HOST': 'loonflow-db'" /opt/loonflow/settings/config.py

# 修改日志路径
# RUN sed -i "/'filename': HOMEPATH + '/loonflow.log'/c'filename': '/var/log/loonflow/loonflow.log'" /opt/loonflow/settings/common.py
RUN sed -i "/HOMEPATH = os.environ['HOMEPATH']/cHOMEPATH = '/var/log/loonflow'" /opt/loonflow/settings/common.py
RUN sed -i "/HOMEPATH = os.environ['HOME']/cHOMEPATH = '/var/log/loonflow'" /opt/loonflow/settings/common.py
