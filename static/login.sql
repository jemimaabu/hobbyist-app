use heroku_f959c05b805d118;
delimiter //
CREATE PROCEDURE login(IN p_email varchar(225),IN p_password varchar(225))
BEGIN
	select * from user where email = p_email and password = p_password;
END//
delimiter ;