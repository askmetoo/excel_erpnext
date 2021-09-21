FROM node:12-buster-slim

COPY install_app.sh /install_app

RUN apt-get update && apt-get install git -y && \
  /install_app excel_erpnext https://gitlab.com/castlecraft/excel_erpnext.git version-12

FROM frappe/erpnext-nginx:v12.25.0

COPY --from=0 /home/frappe/frappe-bench/sites/ /var/www/html/
COPY --from=0 /rsync /rsync
RUN echo -n "\nexcel_erpnext" >> /var/www/html/apps.txt

VOLUME [ "/assets" ]

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]
