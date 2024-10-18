--  SQL script that creates a stored procedure ComputeAverageWeightedScoreForUser
-- that computes and store the average weighted score for a student.

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
DELIMITER ;