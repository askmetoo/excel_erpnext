FROM frappe/erpnext-worker:v12.20.0

ARG BUILD_BRANCH=version-12
RUN install_app excel_erpnext https://gitlab.com/castlecraft/excel_erpnext ${BUILD_BRANCH}
RUN sed -i -e "s/Your verification code is/আর্কঅ্যাপস এর জন্য ব্যবহার করুন -/g" /home/frappe/frappe-bench/apps/frappe/frappe/twofactor.py
