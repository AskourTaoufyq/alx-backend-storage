-- SQL script that creates a stored procedure ComputeAverageWeightedScoreForUsers
-- that computes and store the average weighted score for all students.

DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN p_user_id INT)
BEGIN
    DECLARE scoreSum DECIMAL(10, 2);
    DECLARE weightSum INT;

    SELECT SUM(c.score * p.weight), SUM(p.weight)
    INTO scoreSum, weightSum
    FROM corrections c
    JOIN projects p ON p.id = c.project_id
    WHERE c.user_id = p_user_id;

    UPDATE users
    SET average_score = scoreSum / weightSum
    WHERE id = p_user_id;

END //


CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE numberOfStudents INT;
    DECLARE count INT DEFAULT 1;

    SELECT COUNT(id)
    INTO numberOfStudents
    FROM users;

    WHILE count <= numberOfStudents DO
        CALL ComputeAverageWeightedScoreForUser(count);
        SET count = count + 1;
    END WHILE;

END //
DELIMITER ;