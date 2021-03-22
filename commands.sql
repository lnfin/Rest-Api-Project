mysql -u root
CREATE USER 'yandex_app'@'localhost' IDENTIFIED BY 'sup3r_s3cr3t_p4ss';
CREATE DATABASE yandex_db;
GRANT ALL PRIVILEGES ON yandex_db . * TO 'yandex_app'@'localhost';
FLUSH PRIVILEGES;

mysql -u yandex_app -p #sup3r_s3cr3t_p4ss
USE yandex_db;
