DELIMITER ;
USE Hobbies;
DROP PROCEDURE IF EXISTS showHobby;

DELIMITER $$
CREATE PROCEDURE showHobby(IN p_user_id bigint)
BEGIN
    select * from userhobbies where user_id = p_user_id;
END$$

DELIMITER ;