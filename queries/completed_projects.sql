CREATE VIEW `completed_projects` AS
SELECT *
FROM projects
WHERE ProjectStatus = 'Closed'
ORDER BY ProjectClosingDate DESC
LIMIT 5;