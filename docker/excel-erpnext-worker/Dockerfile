FROM frappe/erpnext-worker:v12.25.0

RUN install_app excel_erpnext https://gitlab.com/castlecraft/excel_erpnext version-12
RUN sed -i -e "s/Your verification code is/আর্কঅ্যাপস এর জন্য ব্যবহার করুন -/g" /home/frappe/frappe-bench/apps/frappe/frappe/twofactor.py
