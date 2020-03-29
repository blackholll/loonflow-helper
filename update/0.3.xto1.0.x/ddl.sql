-- LoonUser 新增字段is_workflow_admin
alter table account_loonuser add is_workflow_admin TINYINT(1) UNSIGNED NOT NULL default 0 comment '工作流管理员';

-- CustomNotice 字段修改， 去掉script，title_template， content_template  新增hook_url， hook_token 执行sql:
alter table workflow_customnotice add hook_url varchar(100) not null default '' comment 'hook_url';
alter table workflow_customnotice add hook_token varchar(100) not null default '' comment 'hook_token';
alter table workflow_customnotice drop column title_template;
alter table workflow_customnotice drop column content_template;
alter table workflow_customnotice drop column script;



-- Workflow表新增 title_template， content_template
alter table workflow_workflow add title_template varchar(100) not null default '' comment '标题模板';
alter table workflow_workflow add content_template varchar(1000) not null default '' comment '内容模板';

-- 新增WorkflowAdmin表，用于保存工作流管理员
CREATE TABLE `workflow_workflowadmin` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `creator` varchar(50) NOT NULL DEFAULT 'admin' COMMENT '创建人',
  `gmt_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `gmt_modified` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '已删除',
  `username` varchar(100) NOT NULL DEFAULT '' COMMENT '用户名',
  `workflow_id` int(11) NOT NULL DEFAULT '0' COMMENT '工作流id',
  PRIMARY KEY (`id`),
  KEY `idx_workflow_id` (`workflow_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 删除workflow表中的flowchart字段
alter table workflow_workflow drop column flowchart;

-- state表中删除sub_workflow_id字段
alter table workflow_state drop column sub_workflow_id;
alter table workflow_state add column enable_retreat TINYINT(1) UNSIGNED NOT NULL default 0 COMMENT '允许撤回';

-- 工单基础表中 删除is_end、 is_rejected字段
alter table ticket_ticketrecord drop column is_end;
alter table ticket_ticketrecord drop column is_rejected;

-- 工单基础表中新增act_state_id int类型， 分别为草稿中0 进行中1 被拒绝2  被撤回3 已完成4
ALTER TABLE `ticket_ticketrecord`
	ADD COLUMN `act_state_id` INT NOT NULL DEFAULT '0' COMMENT '进行状态' AFTER `script_run_last_result`;

-- 工单关系人表
CREATE TABLE `ticket_ticketuser` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `creator` varchar(50) NOT NULL DEFAULT 'admin' COMMENT '创建人',
  `gmt_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `gmt_modified` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '已删除',
  `username` varchar(100) NOT NULL DEFAULT '' COMMENT '用户名',
  `in_process` tinyint(1) NOT NULL DEFAULT '0' COMMENT '处理中',
  `worked` tinyint(1) NOT NULL DEFAULT '0' COMMENT '处理过的',
  `ticket_id` int(11) NOT NULL DEFAULT '0' COMMENT '工单id',
  PRIMARY KEY (`id`),
  KEY `idx_ticket_id` (`ticket_id`),
  KEY `idx_username_in_process` (`username`,`in_process`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
