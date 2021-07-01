FROM node:14-buster-slim
ARG FRAPPE_BRANCH=version-12
ARG BUILD_BRANCH=${FRAPPE_BRANCH}

COPY install_app.sh /install_app

RUN apt-get update && apt-get install git -y && \
  /install_app excel_erpnext https://gitlab.com/castlecraft/excel_erpnext.git ${BUILD_BRANCH} ${FRAPPE_BRANCH}

FROM frappe/erpnext-nginx:v12.20.0

COPY --from=0 /home/frappe/frappe-bench/sites/ /var/www/html/
COPY --from=0 /rsync /rsync
RUN echo -n "\nexcel_erpnext" >> /var/www/html/apps.txt

VOLUME [ "/assets" ]

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]
