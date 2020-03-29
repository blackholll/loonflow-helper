import MySQLdb

# 数据修改
DB_HOST = '127.0.0.1'
DB_NAME = 'loonflownew1'
DB_PORT = 3306
DB_USER = 'loonflownew1'
DB_PASSWORD = '123456'

COUNT_PER_TIME = 1000  # 每次处理1000条数据

# 当前处理人、历史处理人迁移
# 查询总行数

db = MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD, db=DB_NAME, port=DB_PORT, charset='utf8' )
cursor = db.cursor()

cursor.execute("select count(*) from ticket_ticketrecord")

count_query = cursor.fetchone()
count_result = count_query[0]
print('共{}条记录'.format(count_result))
# 获取relation记录插入， 然后获取当前处理人(个人或者多人的情况)来更新relation记录

if count_result % COUNT_PER_TIME:
    total_time = int((count_result/COUNT_PER_TIME)) + 1
else:
    total_time = int(count_result/COUNT_PER_TIME)

for i in range(total_time):
    limit_start = i
    limit_end = i + COUNT_PER_TIME
    raw_sql0 = "select id, relation,participant_type_id, participant, gmt_created, state_id, creator from ticket_ticketrecord " \
               "limit {},{}".format(limit_start, limit_end)
    cursor.execute(raw_sql0)
    result = cursor.fetchall()

    # 插入relation记录
    insert_relation_sql_list = []
    update_relation_sql_list = []
    update_ticket_sql_list = []
    update_ticket_worked_sql_list = []

    for result0 in result:
        ticket_id, relation, participant_type_id, participant, gmt_created, state_id, creator = result0
        if relation:
            for relation0 in relation.split(','):
                insert_relation_sql_list.append(
                    "insert into ticket_ticketuser (ticket_id, gmt_created, gmt_modified,creator, username, in_process,"
                    "is_deleted) value ({},'{}','{}','{}','{}', 0, 0)".format(ticket_id, gmt_created, gmt_created,
                                                                              'admin', relation0))
        if participant_type_id == 1:
            update_relation_sql_list.append(
                "update ticket_ticketuser set in_process=1 where ticket_id={} and username='{}' and is_deleted=0"
                    .format(ticket_id, participant))
        if participant_type_id == 2:
            for participant0 in participant.split(','):
                if participant0:
                    update_relation_sql_list.append(
                        "update ticket_ticketuser set in_process=1 where ticket_id={} and username='{}' and "
                        "is_deleted=0".format(ticket_id, participant0))
        worked_sql = "select participant from ticket_ticketflowlog where ticket_id={} and transition_id!=0".format(ticket_id)
        cursor.execute(worked_sql)
        worked_sql_result = cursor.fetchall()
        for worked_sql_result0 in worked_sql_result:
            if worked_sql_result0[0] != creator:
                # 排除工单创建人
                update_ticket_worked_sql_list.append("update ticket_ticketuser set worked=1 where ticket_id={} and username='{}'".format(ticket_id,worked_sql_result0[0]))

        # ticket record中attr_state_id变更， 需要查询flow_log以及当前state_id来做处理 草稿中0 进行中1 被拒绝2  被撤回3 已完成4
        # 0.3版本不支持保存到初始状态，所以不会有草稿中， 如果最后一次操作是拒绝类型的，那么attr_state_id为被拒绝， 如果最后一次操作非拒绝，且状态非结束状态，那么attr_state_id为进行中，
        # 如果当前状态为已经结束，那么attr_state_id为已完成
        print(ticket_id)
        last_transition_query_sql = "select transition_type_id from workflow_transition where id =(select transition_id from ticket_ticketflowlog where id =(select max(id) from ticket_ticketflowlog where ticket_id={}))".format(ticket_id)
        cursor.execute(last_transition_query_sql)
        last_transition_result = cursor.fetchone()
        if last_transition_result:
            last_transition_type_id = last_transition_result[0]
            if last_transition_type_id == 2:  # 被拒绝
                attr_state_id = 2  # 工单的进行状态为:被退回
            else:
                ticket_state_query_sql = "select type_id from workflow_state where id={}".format(state_id)
                cursor.execute(ticket_state_query_sql)
                ticket_state_type_id = cursor.fetchone()[0]
                if ticket_state_type_id == 0:  # 非结束状态
                    attr_state_id = 1  # 工单的进行状态为:进行中
                else:
                    attr_state_id = 4  # 工单的进行状态为已完成
        else:
            attr_state_id = 1
        update_ticket_sql_list.append("update ticket_ticketrecord set act_state_id={} where id={}".format(attr_state_id, ticket_id))

    insert_relation_sql = ';'.join(insert_relation_sql_list)
    update_relation_sql = ';'.join(update_relation_sql_list)
    update_ticket_sql = ';'.join(update_ticket_sql_list)
    update_ticket_worked_sql = ';'.join(update_ticket_worked_sql_list)
    # print(insert_relation_sql)
    # print(update_relation_sql)
    # print(update_ticket_sql)
    # print(update_ticket_worked_sql)
    cursor.execute(insert_relation_sql)
    cursor.execute(update_relation_sql)
    cursor.execute(update_ticket_sql)
    cursor.execute(update_ticket_worked_sql)

db.close()



