-- SQL script that creates a stored procedure ComputeAverageScoreForUser
DELIMETER $;
CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
	DECLARE avg_score FLOAT;
	SELECT AVG(score) INTO avg_score FROM corrections
	WHERE user_id = corrections.user_id;
	UPDATE users
	SET average_score = avg_score
	WHERE id = user_id;
END;
$
