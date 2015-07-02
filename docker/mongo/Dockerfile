FROM mongo:3.0
MAINTAINER songjiao@cyou-inc.com

ENV AUTH yes
ENV STORAGE_ENGINE wiredTiger
ENV JOURNALING yes

ADD run.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ADD set_mongodb_password.sh /set_mongodb_password.sh
RUN chmod +x /set_mongodb_password.sh
EXPOSE 27017 28017

CMD ["/entrypoint.sh"]
