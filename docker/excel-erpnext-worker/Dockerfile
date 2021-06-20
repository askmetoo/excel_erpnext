FROM frappe/erpnext-worker:v13.4.1

RUN install_app excel_erpnext https://gitlab.com/castlecraft/excel_erpnext version-13
RUN sed -i -e "s/Your verification code is/আর্কঅ্যাপস এর জন্য ব্যবহার করুন -/g" /home/frappe/frappe-bench/apps/frappe/frappe/twofactor.py
