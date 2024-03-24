INSERT INTO user (user_id, name) VALUES ('1000', 'Derek');
INSERT INTO user (user_id, name) VALUES ('1001', 'Florence');
INSERT INTO user (user_id, name) VALUES ('1002', 'Sarah');

INSERT INTO user_file (file_id, file_name, user_id ) VALUES ('101', 'derek-health-info.txt', '1000');

INSERT INTO user_file (file_id, file_name, user_id ) VALUES ('103', 'florence-health-info.txt', '1001');

INSERT INTO user_file (file_id, file_name, user_id ) VALUES ('105', 'sarah-health-info.txt', '1002');