-- Drop the database if it exists
DROP DATABASE IF EXISTS `schedulebot`;

-- Create the schedulebot database
CREATE DATABASE `schedulebot` DEFAULT CHARACTER SET = 'utf8mb4';

-- Use the schedulebot database
USE `schedulebot`;

-- Drop the event_types table if it exists
DROP TABLE IF EXISTS `event_types`;

-- Create the event_types table
CREATE TABLE `event_types` (
    `id` int NOT NULL AUTO_INCREMENT COMMENT 'Primary Key',
    `event_type` varchar(255) DEFAULT NULL COMMENT 'Event Type',
    `start_time` datetime DEFAULT NULL COMMENT 'Start Time',
    `end_time` datetime DEFAULT NULL COMMENT 'End Time',
    `user_id` bigint DEFAULT NULL COMMENT 'User ID',
    PRIMARY KEY (`id`)
) COMMENT = 'Table to store event types';

-- Drop the EVENT table if it exists
DROP TABLE IF EXISTS `EVENT`;

-- Create the EVENT table
CREATE TABLE `EVENT` (
    `id` int NOT NULL AUTO_INCREMENT COMMENT 'Primary Key',
    `name` varchar(255) DEFAULT NULL,
    `start_date` date DEFAULT NULL,
    `end_date` date DEFAULT NULL,
    `priority` int DEFAULT NULL,
    `type` varchar(255) DEFAULT NULL,
    `notes` text,
    `location` varchar(255) DEFAULT NULL,
    `user_id` bigint DEFAULT NULL,
    PRIMARY KEY (`id`)
) COMMENT = 'Table to store events';
