-- =================================================================================
--  MASTER DATABASE SETUP SCRIPT (All-in-One)
--  Version: No Hashing (for Demo)
--
--  This single file will:
--  1. Create the 'studywelldb' database.
--  2. Drop all old tables for a completely clean and safe re-run.
--  3. Create all tables with the correct structure.
--  4. Insert ALL demo data, including 17+ users and rich, interconnected
--     data for 5 key students to showcase every feature.
--  5. Create all required Functions, Stored Procedures, and Triggers.
-- =================================================================================

-- ---------------------------------------------------------------------------------
--  STEP 1: DATABASE CREATION
-- ---------------------------------------------------------------------------------
CREATE DATABASE IF NOT EXISTS studywelldb;
USE studywelldb;

-- ---------------------------------------------------------------------------------
--  STEP 2: DROP EXISTING OBJECTS FOR A CLEAN SLATE
--  This makes the script 100% safe to re-run at any time.
-- ---------------------------------------------------------------------------------
DROP TABLE IF EXISTS `Notifications`, `StudySessions`, `WellnessLogs`, `Tasks`, `Courses`, `UserSemesters`, `Semesters`, `CampusResources`, `Users`;

-- ---------------------------------------------------------------------------------
--  STEP 3: CREATE ALL TABLES
-- ---------------------------------------------------------------------------------
CREATE TABLE `Users` (
  `UserID` INT AUTO_INCREMENT PRIMARY KEY,
  `Name` VARCHAR(255) NOT NULL,
  `Email` VARCHAR(255) NOT NULL UNIQUE,
  `Password` VARCHAR(255) NOT NULL, -- Storing plain text password for demo
  `Role` ENUM('Student', 'Admin') NOT NULL DEFAULT 'Student',
  `CreatedAt` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE `Semesters` ( `SemesterID` INT AUTO_INCREMENT PRIMARY KEY, `SemesterName` VARCHAR(100) NOT NULL UNIQUE, `StartDate` DATE NOT NULL, `EndDate` DATE NOT NULL );
CREATE TABLE `UserSemesters` ( `UserID` INT NOT NULL, `SemesterID` INT NOT NULL, PRIMARY KEY (`UserID`, `SemesterID`), FOREIGN KEY (`UserID`) REFERENCES `Users`(`UserID`) ON DELETE CASCADE, FOREIGN KEY (`SemesterID`) REFERENCES `Semesters`(`SemesterID`) ON DELETE CASCADE );
CREATE TABLE `Courses` ( `CourseID` INT AUTO_INCREMENT PRIMARY KEY, `UserID` INT NOT NULL, `CourseName` VARCHAR(255) NOT NULL, `CourseCode` VARCHAR(50), FOREIGN KEY (`UserID`) REFERENCES `Users`(`UserID`) ON DELETE CASCADE );
CREATE TABLE `Tasks` ( `TaskID` INT AUTO_INCREMENT PRIMARY KEY, `CourseID` INT NOT NULL, `TaskName` VARCHAR(255) NOT NULL, `DueDate` DATE, `Status` ENUM('Pending', 'Completed') NOT NULL DEFAULT 'Pending', `PrerequisiteTaskID` INT NULL, FOREIGN KEY (`CourseID`) REFERENCES `Courses`(`CourseID`) ON DELETE CASCADE, FOREIGN KEY (`PrerequisiteTaskID`) REFERENCES `Tasks`(`TaskID`) ON DELETE SET NULL );
CREATE TABLE `WellnessLogs` ( `LogID` INT AUTO_INCREMENT PRIMARY KEY, `UserID` INT NOT NULL, `LogDate` DATE NOT NULL, `StressLevel` INT NOT NULL, `Mood` VARCHAR(50), `SleepHours` DECIMAL(4,2), UNIQUE KEY `UserDateLog` (`UserID`, `LogDate`), FOREIGN KEY (`UserID`) REFERENCES `Users`(`UserID`) ON DELETE CASCADE );
CREATE TABLE `StudySessions` ( `SessionID` INT AUTO_INCREMENT PRIMARY KEY, `UserID` INT NOT NULL, `CourseID` INT NOT NULL, `TaskID` INT, `SessionDate` DATE NOT NULL, `DurationMinutes` INT NOT NULL, FOREIGN KEY (`UserID`) REFERENCES `Users`(`UserID`) ON DELETE CASCADE, FOREIGN KEY (`CourseID`) REFERENCES `Courses`(`CourseID`) ON DELETE CASCADE, FOREIGN KEY (`TaskID`) REFERENCES `Tasks`(`TaskID`) ON DELETE SET NULL );
CREATE TABLE `Notifications` ( `NotificationID` INT AUTO_INCREMENT PRIMARY KEY, `UserID` INT NOT NULL, `Message` TEXT NOT NULL, `CreatedAt` TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (`UserID`) REFERENCES `Users`(`UserID`) ON DELETE CASCADE );
CREATE TABLE `CampusResources` ( `ResourceID` INT AUTO_INCREMENT PRIMARY KEY, `ResourceName` VARCHAR(255) NOT NULL, `ResourceType` ENUM('Academic', 'Wellness', 'Financial', 'Career') NOT NULL, `ContactInfo` VARCHAR(255) NOT NULL );

-- ---------------------------------------------------------------------------------
--  STEP 4: INSERT ALL DEMO DATA
-- ---------------------------------------------------------------------------------

-- Part A: Semesters & Resources
INSERT INTO `Semesters` (`SemesterName`, `StartDate`, `EndDate`) VALUES ('Fall 2025', '2025-08-15', '2025-12-20'), ('Spring 2026', '2026-01-10', '2026-05-15');
INSERT INTO `CampusResources` (`ResourceName`, `ResourceType`, `ContactInfo`) VALUES ('University Writing Center', 'Academic', 'writingcenter@university.edu');

-- Part B: All Users with Plain Text Passwords
INSERT INTO `Users` (`Name`, `Email`, `Password`, `Role`) VALUES
('Admin User', 'admin@test.com', 'adminpass', 'Admin'),
('Vanya Sharma', 'vanya@test.com', 'studentpass', 'Student'),
('Aarav Sharma', 'aarav.sharma@test.com', 'demopass', 'Student'),
('Priya Patel', 'priya.patel@test.com', 'demopass', 'Student'),
('Rohan Gupta', 'rohan.gupta@test.com', 'demopass', 'Student'),
('Ananya Singh', 'ananya.singh@test.com', 'demopass', 'Student'),
('Vikram Kumar', 'vikram.kumar@test.com', 'demopass', 'Student'),
('Ishika Reddy', 'ishika.reddy@test.com', 'demopass', 'Student'),
('Arjun Mehta', 'arjun.mehta@test.com', 'demopass', 'Student'),
('Saanvi Joshi', 'saanvi.joshi@test.com', 'demopass', 'Student'),
('Aditya Rao', 'aditya.rao@test.com', 'demopass', 'Student'),
('Diya Nair', 'diya.nair@test.com', 'demopass', 'Student'),
('Kabir Verma', 'kabir.verma@test.com', 'demopass', 'Student'),
('Myra Agarwal', 'myra.agarwal@test.com', 'demopass', 'Student'),
('Vivaan Iyer', 'vivaan.iyer@test.com', 'demopass', 'Student'),
('Zara Khan', 'zara.khan@test.com', 'demopass', 'Student'),
('Reyansh Desai', 'reyansh.desai@test.com', 'demopass', 'Student'),
('Faculty Admin', 'faculty.admin@test.com', 'demopass', 'Admin');

-- Part C: Link Students to Semesters
INSERT INTO `UserSemesters` (`UserID`, `SemesterID`) VALUES (2,1), (3,1), (4,2), (5,1), (6,2), (7,1), (8,2), (9,1), (10,2), (11,1), (12,2), (13,1), (14,2), (15,1), (16,2), (17,1);

-- Part D: Populate Rich Data for 5 Key Users

-- USER 1: Vanya Sharma (UserID=2)
INSERT INTO `Courses` (`UserID`, `CourseName`, `CourseCode`) VALUES (2, 'Database Management Systems', 'CS-301'), (2, 'Software Engineering', 'SE-305'), (2, 'Operating Systems', 'CS-303'), (2, 'Web Development', 'CS-304');
SET @vanya_dbms_id = (SELECT CourseID FROM Courses WHERE UserID=2 AND CourseCode='CS-301');
SET @vanya_se_id = (SELECT CourseID FROM Courses WHERE UserID=2 AND CourseCode='SE-305');
SET @vanya_os_id = (SELECT CourseID FROM Courses WHERE UserID=2 AND CourseCode='CS-303');
SET @vanya_wd_id = (SELECT CourseID FROM Courses WHERE UserID=2 AND CourseCode='CS-304');
INSERT INTO `Tasks` (`CourseID`, `TaskName`, `DueDate`) VALUES (@vanya_se_id, 'Submit Project Proposal', '2025-11-22');
SET @proposal_id = LAST_INSERT_ID();
INSERT INTO `Tasks` (`CourseID`, `TaskName`, `DueDate`, `PrerequisiteTaskID`) VALUES (@vanya_se_id, 'Implement Project Backend', '2025-12-05', @proposal_id);
INSERT INTO `Tasks` (`CourseID`, `TaskName`, `DueDate`) VALUES (@vanya_os_id, 'Lab Assignment 3', '2025-11-25');
INSERT INTO `StudySessions` (`UserID`, `CourseID`, `SessionDate`, `DurationMinutes`) VALUES (2, @vanya_dbms_id, CURDATE() - INTERVAL 5 DAY, 90), (2, @vanya_se_id, CURDATE() - INTERVAL 4 DAY, 75), (2, @vanya_os_id, CURDATE() - INTERVAL 3 DAY, 60), (2, @vanya_wd_id, CURDATE() - INTERVAL 2 DAY, 120);
INSERT INTO `WellnessLogs` (`UserID`, `LogDate`, `StressLevel`, `Mood`, `SleepHours`) VALUES (2, CURDATE()-5, 7, 'Stressed', 6.0), (2, CURDATE()-4, 5, 'Neutral', 7.5), (2, CURDATE()-3, 6, 'Neutral', 7.0), (2, CURDATE()-2, 8, 'Stressed', 5.5), (2, CURDATE()-1, 4, 'Happy', 8.0);

-- USER 2: Aarav Sharma (UserID=3)
INSERT INTO `Courses` (`UserID`, `CourseName`, `CourseCode`) VALUES (3, 'Data Structures', 'CS-201'), (3, 'Computer Networks', 'CS-401');
SET @aarav_ds_id = (SELECT CourseID FROM Courses WHERE UserID=3 AND CourseCode='CS-201');
SET @aarav_cn_id = (SELECT CourseID FROM Courses WHERE UserID=3 AND CourseCode='CS-401');
INSERT INTO `Tasks` (`CourseID`, `TaskName`, `DueDate`, `Status`) VALUES (@aarav_ds_id, 'Implement Linked List', '2025-11-18', 'Completed');
INSERT INTO `Tasks` (`CourseID`, `TaskName`, `DueDate`) VALUES (@aarav_ds_id, 'Implement Binary Search Tree', '2025-11-25'), (@aarav_cn_id, 'Configure Subnet Mask', '2025-12-02');
INSERT INTO `StudySessions` (`UserID`, `CourseID`, `SessionDate`, `DurationMinutes`) VALUES (3, @aarav_ds_id, CURDATE()-2, 60), (3, @aarav_cn_id, CURDATE()-1, 45);
INSERT INTO `WellnessLogs` (`UserID`, `LogDate`, `StressLevel`, `Mood`, `SleepHours`) VALUES (3, CURDATE()-2, 3, 'Happy', 8.0), (3, CURDATE()-1, 4, 'Neutral', 7.5);

-- USER 3: Priya Patel (UserID=4) - High Stress Demo User
INSERT INTO `Courses` (`UserID`, `CourseName`, `CourseCode`) VALUES (4, 'Machine Learning', 'AI-401');
SET @priya_ml_id = (SELECT CourseID FROM Courses WHERE UserID=4 AND CourseCode='AI-401');
INSERT INTO `Tasks` (`CourseID`, `TaskName`, `DueDate`) VALUES (@priya_ml_id, 'Implement K-Means Clustering Algorithm', '2025-12-10');
INSERT INTO `StudySessions` (`UserID`, `CourseID`, `SessionDate`, `DurationMinutes`) VALUES (4, @priya_ml_id, CURDATE()-1, 180);
INSERT INTO `WellnessLogs` (`UserID`, `LogDate`, `StressLevel`, `Mood`, `SleepHours`) VALUES (4, CURDATE()-2, 9, 'Stressed', 5.0), (4, CURDATE()-1, 8, 'Stressed', 6.0);

-- USER 4: Rohan Gupta (UserID=5)
INSERT INTO `Courses` (`UserID`, `CourseName`, `CourseCode`) VALUES (5, 'Intro to Python', 'CS-101'), (5, 'Calculus I', 'MA-101');
SET @rohan_py_id = (SELECT CourseID FROM Courses WHERE UserID=5 AND CourseCode='CS-101');
INSERT INTO `Tasks` (`CourseID`, `TaskName`, `DueDate`) VALUES (@rohan_py_id, 'Complete Chapter 1 Exercises', '2025-11-20');
INSERT INTO `StudySessions` (`UserID`, `CourseID`, `SessionDate`, `DurationMinutes`) VALUES (5, @rohan_py_id, CURDATE()-1, 30);
INSERT INTO `WellnessLogs` (`UserID`, `LogDate`, `StressLevel`, `Mood`, `SleepHours`) VALUES (5, CURDATE()-1, 2, 'Happy', 8.5);

-- USER 5: Ananya Singh (UserID=6)
INSERT INTO `Courses` (`UserID`, `CourseName`, `CourseCode`) VALUES (6, 'Linear Algebra', 'MA-202'), (6, 'Discrete Mathematics', 'MA-205');
SET @ananya_la_id = (SELECT CourseID FROM Courses WHERE UserID=6 AND CourseCode='MA-202');
SET @ananya_dm_id = (SELECT CourseID FROM Courses WHERE UserID=6 AND CourseCode='MA-205');
INSERT INTO `Tasks` (`CourseID`, `TaskName`, `DueDate`) VALUES (@ananya_dm_id, 'Homework 5: Proofs', '2025-11-24'), (@ananya_dm_id, 'Homework 6: Set Theory', '2025-12-01'), (@ananya_la_id, 'Chapter 3 Problem Set', '2025-11-28');
INSERT INTO `StudySessions` (`UserID`, `CourseID`, `SessionDate`, `DurationMinutes`) VALUES (6, @ananya_dm_id, CURDATE()-3, 90), (6, @ananya_la_id, CURDATE()-2, 75), (6, @ananya_dm_id, CURDATE()-1, 60);
INSERT INTO `WellnessLogs` (`UserID`, `LogDate`, `StressLevel`, `Mood`, `SleepHours`) VALUES (6, CURDATE()-2, 4, 'Neutral', 7.0), (6, CURDATE()-1, 3, 'Neutral', 7.0);

-- Part E: Add a final welcome notification for Vanya
INSERT INTO `Notifications` (`UserID`, `Message`) VALUES (2, 'Welcome! Remember to log your wellness and study sessions regularly.');

-- ---------------------------------------------------------------------------------
--  STEP 5: CREATE FUNCTIONS, STORED PROCEDURES, AND TRIGGERS
-- ---------------------------------------------------------------------------------
SET GLOBAL log_bin_trust_function_creators = 1;
DELIMITER $$

CREATE FUNCTION `fn_IsTaskUnlocked`(p_TaskID INT) RETURNS tinyint(1) BEGIN DECLARE v_PrereqID INT; DECLARE v_PrereqStatus VARCHAR(20); SELECT PrerequisiteTaskID INTO v_PrereqID FROM Tasks WHERE TaskID = p_TaskID; IF v_PrereqID IS NULL THEN RETURN 1; END IF; SELECT Status INTO v_PrereqStatus FROM Tasks WHERE TaskID = v_PrereqID; IF v_PrereqStatus = 'Completed' THEN RETURN 1; ELSE RETURN 0; END IF; END$$

CREATE FUNCTION `fn_GetAverageStress`(p_UserID INT, p_DaysAgo INT) RETURNS decimal(10,2) BEGIN DECLARE v_AvgStress DECIMAL(10,2); SELECT AVG(StressLevel) INTO v_AvgStress FROM WellnessLogs WHERE UserID = p_UserID AND LogDate >= CURDATE() - INTERVAL p_DaysAgo DAY; RETURN IFNULL(v_AvgStress, 0.00); END$$

CREATE PROCEDURE `sp_CompleteTask`(IN p_UserID INT, IN p_TaskID INT) BEGIN UPDATE Tasks SET Status = 'Completed' WHERE TaskID = p_TaskID; END$$

CREATE PROCEDURE `sp_RegisterUserWithSemester`(IN p_Name VARCHAR(255), IN p_Email VARCHAR(255), IN p_Password VARCHAR(255), IN p_Role ENUM('Student', 'Admin'), IN p_SemesterID INT, OUT p_NewUserID INT) BEGIN INSERT INTO Users (Name, Email, Password, Role) VALUES (p_Name, p_Email, p_Password, p_Role); SET p_NewUserID = LAST_INSERT_ID(); IF p_Role = 'Student' AND p_SemesterID IS NOT NULL THEN INSERT INTO UserSemesters (UserID, SemesterID) VALUES (p_NewUserID, p_SemesterID); END IF; END$$

CREATE TRIGGER `trg_UnlockDependentTask` AFTER UPDATE ON `Tasks` FOR EACH ROW BEGIN DECLARE v_DependentTaskName VARCHAR(255); DECLARE v_UserID INT; DECLARE v_DependentTaskID INT; IF NEW.Status = 'Completed' AND OLD.Status <> 'Completed' THEN SELECT TaskID, TaskName INTO v_DependentTaskID, v_DependentTaskName FROM Tasks WHERE PrerequisiteTaskID = NEW.TaskID LIMIT 1; IF v_DependentTaskID IS NOT NULL THEN SELECT c.UserID INTO v_UserID FROM Courses c JOIN Tasks t ON c.CourseID = t.CourseID WHERE t.TaskID = v_DependentTaskID; INSERT INTO Notifications (UserID, Message) VALUES (v_UserID, CONCAT('Task Unlocked: You can now start "', v_DependentTaskName, '".')); END IF; END IF; END$$

CREATE TRIGGER `trg_CheckConsecutiveHighStress` AFTER INSERT ON `WellnessLogs` FOR EACH ROW BEGIN DECLARE v_HighStressCount INT; SELECT COUNT(*) INTO v_HighStressCount FROM (SELECT StressLevel FROM WellnessLogs WHERE UserID = NEW.UserID ORDER BY LogDate DESC LIMIT 3) AS LastThreeLogs WHERE StressLevel >= 8; IF v_HighStressCount = 3 THEN INSERT INTO Notifications (UserID, Message) VALUES (NEW.UserID, 'High Stress Alert: You have reported high stress for 3 consecutive logs. Remember to take a break or use campus wellness resources.'); END IF; END$$

DELIMITER ;

SELECT 'MASTER SETUP SCRIPT COMPLETED SUCCESSFULLY!' as `Status`;