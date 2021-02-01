FROM frappe/erpnext-worker:v12.16.2

RUN install_app excel_erpnext https://gitlab.com/castlecraft/excel_erpnext version-12
RUN sed -i -e "s/Your verification code/আপনার লগইন কোড/g" /home/frappe/frappe-bench/apps/frappe/frappe/twofactor.py
