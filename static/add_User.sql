USE heroku_f959c05b805d118;
CREATE TABLE user (id BIGINT NOT NULL AUTO_INCREMENT, name varchar(225), email varchar(225), number varchar(225), password VARCHAR(225), PRIMARY KEY (id));

DELIMITER $$
CREATE  PROCEDURE add_User( IN p_name varchar(225), IN p_email varchar(225), IN p_number varchar(225), IN p_password varchar(225))
BEGIN
    if ( select exists (select 1 from user where email = p_email) ) THEN
     
        select 'Username Exists !!';
     
    ELSE
     
        insert into user
        (
            name,
            email,
            number,
            password
        )
        values
        (
            p_name,
            p_email,
            p_number,
            p_password
        );
     
    END IF;
END$$
DELIMITER ;