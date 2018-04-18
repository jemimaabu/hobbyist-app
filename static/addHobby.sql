DELIMITER ;
USE heroku_f959c05b805d118;
DROP PROCEDURE IF EXISTS addHobby;

DELIMITER $$
CREATE PROCEDURE addHobby( IN p_hobby varchar(225), IN p_user_id bigint)
BEGIN
        insert into userhobbies
        (
            hobby, 
            user_id
        )
        values
        (
            p_hobby, 
            p_user_id
        );
END$$
DELIMITER ;