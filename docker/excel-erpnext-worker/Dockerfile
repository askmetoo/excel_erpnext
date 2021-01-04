FROM frappe/erpnext-worker:v12.10.1

RUN sed -i 's/^PASS_MAX_DAYS.*/PASS_MAX_DAYS    -1/' /etc/login.defs && \
    sed -i 's/^PASS_MIN_DAYS.*/PASS_MIN_DAYS    -1/' /etc/login.defs

RUN install_app excel_erpnext https://gitlab.com/castlecraft/excel_erpnext version-12
